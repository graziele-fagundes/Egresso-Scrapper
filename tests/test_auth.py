import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock
from faker import Faker
from usuario import Usuario
from db.main import Database
from auth import Auth 

class TestAuthComFaker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    def setUp(self):
        self.mock_db = MagicMock(spec=Database)
        self.auth = Auth(db=self.mock_db)

    def test_criarUsuario_sucesso(self):
        random_nome = self.faker.name()
        random_email = self.faker.email()
        random_senha = self.faker.password()

        usuario = self.auth.criarUsuario(random_nome, random_email, random_senha)
        
        self.assertIsNotNone(usuario)
        self.assertIsInstance(usuario, Usuario)
        self.assertEqual(usuario.nome, random_nome)
        self.assertEqual(usuario.email, random_email)
        self.assertEqual(usuario.senha, random_senha)

    def test_login_sucesso(self):
        random_email = self.faker.email()
        random_senha = self.faker.password()

        usuario = self.auth.login(random_email, random_senha)

        self.assertIsNotNone(usuario)
        self.assertIsInstance(usuario, Usuario)

    def test_login_falha(self):
        self.mock_db.login.return_value = None

        random_email = self.faker.email()
        random_senha = self.faker.password()

        usuario = self.auth.login(random_email, random_senha)

        self.assertIsNone(usuario)

if __name__ == '__main__':
    unittest.main()
