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
        self.egresso = Egresso(nome=self.nome, anoFormacao=self.anoFormacao, db=self.mock_db)

    def test_criacao_egresso(self):
        self.mock_db.criarEgresso.assert_called_once_with(self.nome, self.anoFormacao)
        self.assertIsNotNone(self.egresso.id)
        self.assertEqual(self.egresso.nome, self.nome)
        self.assertEqual(self.egresso.anoFormacao, self.anoFormacao)

    def test_atualizar_linkedin(self):
        random_linkedin_nome = self.faker.name()
        random_linkedin_url = self.faker.url()
        random_linkedin_resumo = self.faker.text(max_nb_chars=200)

        linkedin = Linkedin(nome=random_linkedin_nome, url=random_linkedin_url, resumo=random_linkedin_resumo)
        
        self.mock_db.criarLinkedin.return_value = 1

        self.egresso.atualizarLinkedin(linkedin)

        self.mock_db.criarLinkedin.assert_called_once_with(linkedin)
        self.mock_db.editarEgresso.assert_called_once_with(egresso_id=self.egresso.id, novo_linkedin_id=1)
        self.assertEqual(self.egresso.linkedin, linkedin)
        self.assertEqual(linkedin.id, 1)

    def test_atualizar_lattes(self):
        random_lattes_nome = self.faker.name()
        random_lattes_url = self.faker.url()
        random_lattes_resumo = self.faker.text(max_nb_chars=200)

        lattes = Lattes(nome=random_lattes_nome, url=random_lattes_url, resumo=random_lattes_resumo)
        
        self.mock_db.criarLattes.return_value = 1

        self.egresso.atualizarLattes(lattes)

        self.mock_db.criarLattes.assert_called_once_with(lattes)
        self.mock_db.editarEgresso.assert_called_once_with(egresso_id=self.egresso.id, novo_lattes_id=1)
        self.assertEqual(self.egresso.lattes, lattes)
        self.assertEqual(lattes.id, 1)

    def test_str(self):
        self.assertEqual(str(self.egresso), f"ID: {self.egresso.id} Nome: {self.nome} \n Lattes: \nNone \n Linkedin: \nNone")

if __name__ == '__main__':
    unittest.main()
