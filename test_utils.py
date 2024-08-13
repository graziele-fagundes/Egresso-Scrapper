import unittest
from unittest.mock import patch
from faker import Faker
from utils import setup_driver, get_url_in_string  

class TestUtils(unittest.TestCase):

    @patch('your_module.webdriver.Chrome')  
    def test_setup_driver(self, mock_chrome):
        driver = setup_driver(headless=True)
        mock_chrome.assert_called_once()  
        self.assertIsNotNone(driver) 

    def test_get_url_in_string(self):
        faker = Faker()
        text = f"Aqui está um link: {faker.url()}"
        url = get_url_in_string(text)
        self.assertEqual(url, faker.url())  

        no_url_text = "Não há link aqui."
        url = get_url_in_string(no_url_text)
        self.assertIsNone(url) 

if __name__ == '__main__':
    unittest.main()
