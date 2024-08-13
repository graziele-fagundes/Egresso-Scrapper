import unittest
from faker import Faker
from linkedin import Linkedin  

class TestLinkedinComFaker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    def test_init_com_faker(self):
        random_id = self.faker.random_int(min=1, max=1000)
        random_nome = self.faker.name()
        random_url = self.faker.url()
        random_resumo = self.faker.text(max_nb_chars=200)
        
        linkedin = Linkedin(nome=random_nome, url=random_url, resumo=random_resumo, id=random_id)
        
        self.assertEqual(linkedin.id, random_id)
        self.assertEqual(linkedin.nome, random_nome)
        self.assertEqual(linkedin.url, random_url)
        self.assertEqual(linkedin.resumo, random_resumo)
    
    def test_str_com_faker(self):
        random_id = self.faker.random_int(min=1, max=1000)
        random_nome = self.faker.name()
        random_url = self.faker.url()
        random_resumo = self.faker.text(max_nb_chars=200)
        
        linkedin = Linkedin(nome=random_nome, url=random_url, resumo=random_resumo, id=random_id)
        
        expected_str = f"ID: {random_id} Nome: {random_nome}\nURL: {random_url}\nResumo: {random_resumo}"
        self.assertEqual(str(linkedin), expected_str)

if __name__ == '__main__':
    unittest.main()
