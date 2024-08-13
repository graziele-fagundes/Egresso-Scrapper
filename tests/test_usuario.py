import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from faker import Faker
from usuario import Usuario  

class TestUsuarioComFaker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    def test_init_com_faker(self):
        random_id = self.faker.random_int(min=1, max=1000)
        random_nome = self.faker.name()
        random_email = self.faker.email()
        random_senha = self.faker.password()
        
        usuario = Usuario(id=random_id, nome=random_nome, email=random_email, senha=random_senha)
        
        self.assertEqual(usuario.id, random_id)
        self.assertEqual(usuario.nome, random_nome)
        self.assertEqual(usuario.email, random_email)
        self.assertEqual(usuario.senha, random_senha)
    
    def test_str_com_faker(self):
        random_id = self.faker.random_int(min=1, max=1000)
        random_nome = self.faker.name()
        random_email = self.faker.email()
        random_senha = self.faker.password()
        
        usuario = Usuario(id=random_id, nome=random_nome, email=random_email, senha=random_senha)
        
        expected_str = f"ID: {random_id}, Nome: {random_nome}, Email: {random_email}, Senha: {random_senha}"
        self.assertEqual(str(usuario), expected_str)

if __name__ == '__main__':
    unittest.main()
