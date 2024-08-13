import unittest
from utils import setup_driver
from lattes import Lattes
from linkedin import Linkedin
from lattes import Lattes
from linkedin import Linkedin
from unittest.mock import MagicMock
from faker import Faker
from varredura import Varredura  
from egresso import Egresso

class TestVarredura(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    def setUp(self):
        self.mock_egresso = MagicMock(spec=Egresso)
        self.mock_egresso.nome = self.faker.name()
        self.varredura = Varredura(egresso=self.mock_egresso)
        self.mock_driver = setup_driver(False)
 
    def test_iniciar_varredura(self):
        self.varredura.iniciarVarredura(self.mock_driver)

        self.assertEqual(self.varredura.status, "Concluída")
        self.assertTrue(all(isinstance(link, Linkedin) for link in self.varredura.linkedin))
        self.assertTrue(all(isinstance(lattes, Lattes) for lattes in self.varredura.lattes))

if __name__ == '__main__':
    unittest.main()
