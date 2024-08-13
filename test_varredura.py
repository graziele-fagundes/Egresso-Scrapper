import unittest
from utils import get_url_in_string
from lattes import Lattes
from linkedin import Linkedinfrom
from lattes import Lattes
from linkedin import Linkedin
from unittest.mock import MagicMock, patch
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

        self.mock_driver = MagicMock()

    @patch('time.sleep', return_value=None)  
    def test_iniciar_varredura(self, _):
        self.varredura.iniciarVarredura(self.mock_driver)

        self.assertEqual(self.varredura.status, "Concluída")

    @patch('time.sleep', return_value=None)  
    def test_varredura_linkedin(self, _):
        self.mock_driver.find_element.return_value = MagicMock()
        self.mock_driver.find_elements.return_value = [MagicMock() for _ in range(3)]
        self.mock_driver.find_elements.return_value[0].get_attribute.return_value = "https://www.linkedin.com/in/teste"
        self.mock_driver.find_elements.return_value[0].text = f"{self.mock_egresso.nome} - LinkedIn Brasil"

        self.varredura.varreduraLinkedin(self.mock_driver)

        self.assertEqual(len(self.varredura.linkedin), 3)  
        self.assertTrue(all(isinstance(link, Linkedin) for link in self.varredura.linkedin))

    @patch('time.sleep', return_value=None)  
    def test_varredura_lattes(self, _):
        self.mock_driver.find_element.return_value = MagicMock()
        self.mock_driver.find_elements.return_value = [MagicMock() for _ in range(3)]
        self.mock_driver.find_elements.return_value[0].text = self.faker.name()
        
        self.mock_driver.find_elements.return_value[0].click.return_value = None

        self.varredura.varreduraLattes(self.mock_driver)

        self.assertEqual(len(self.varredura.lattes), 3)  
        self.assertTrue(all(isinstance(lattes, Lattes) for lattes in self.varredura.lattes))

if __name__ == '__main__':
    unittest.main()
