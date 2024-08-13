import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock
from faker import Faker
from lattes import Lattes
from linkedin import Linkedin
from egresso import Egresso  
class TestEgressoComFaker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    def setUp(self):
        self.mock_db = MagicMock()
        self.nome = self.faker.name()
        self.anoFormacao = self.faker.year()

    def test_criacao_egresso(self):
        egresso = Egresso(nome=self.nome, anoFormacao=self.anoFormacao, db=self.mock_db)
        
        self.assertIsNotNone(egresso)
        self.assertIsInstance(egresso, Egresso)
        self.assertEqual(egresso.nome, self.nome)
        self.assertEqual(egresso.anoFormacao, self.anoFormacao)

    def test_atualizar_linkedin(self):
        egresso = Egresso(nome=self.nome, anoFormacao=self.anoFormacao, db=self.mock_db)

        random_linkedin_nome = self.faker.name()
        random_linkedin_url = self.faker.url()
        random_linkedin_resumo = self.faker.text(max_nb_chars=200)

        linkedin = Linkedin(nome=random_linkedin_nome, url=random_linkedin_url, resumo=random_linkedin_resumo)
    
        egresso.atualizarLinkedin(linkedin)

        self.assertEqual(egresso.linkedin, linkedin)

    def test_atualizar_lattes(self):
        egresso = Egresso(nome=self.nome, anoFormacao=self.anoFormacao, db=self.mock_db)

        random_lattes_nome = self.faker.name()
        random_lattes_url = self.faker.url()
        random_lattes_resumo = self.faker.text(max_nb_chars=200)

        lattes = Lattes(nome=random_lattes_nome, url=random_lattes_url, resumo=random_lattes_resumo)
        egresso.atualizarLattes(lattes)

        self.assertEqual(egresso.lattes, lattes)
        
if __name__ == '__main__':
    unittest.main()
