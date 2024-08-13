import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_driver(headless):
    CHROMEDRIVER_PATH = 'chrome/chromedriver.exe' 
    
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_url_in_string(text):
    url = re.search("(?P<url>https?://[^\\s]+)", text)
    if url is None:
        return None
    return url.group("url")