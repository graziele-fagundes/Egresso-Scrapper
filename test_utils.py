import unittest
from unittest.mock import patch
from faker import Faker
from utils import setup_driver, get_url_in_string  

class TestUtils(unittest.TestCase):

    def test_get_url_in_string(self):
        faker = Faker()
        url_faker = faker.url()
        text = f"Aqui está um link: {url_faker}"
        
        url = get_url_in_string(text)
        self.assertEqual(url, url_faker)  

        no_url_text = "Não há link aqui."
        url = get_url_in_string(no_url_text)
        self.assertIsNone(url) 

if __name__ == '__main__':
    unittest.main()
