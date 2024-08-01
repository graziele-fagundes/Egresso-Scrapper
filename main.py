from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Egresso:
    def __init__(self, name):
        self.name = name
        self.linkedin_scrappes = []
        self.lattes_scrappes = []

    def __str__(self):
        s = f"Nome: {self.name}\n"
        s += "Lattes:\n"
        for lattes in self.lattes_scrappes:
            s += f"{lattes}\n"

        return s
    
class Lattes:
    def __init__(self, name, url, summary):
        self.name = name
        self.lattes_url = url
        self.lattes_summary = summary

    def __str__(self):
        return f"Nome: {self.name}\nURL: {self.lattes_url}\nResumo: {self.lattes_summary}"

CHROMEDRIVER_PATH = 'chromedriver.exe' 
LINKEDIN_USERNAME = 'teciii529@gmail.com'
LINKEDIN_PASSWORD = 'tec3patricia'

def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Runs Chrome in headless mode (without a GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def linkedin_login(driver):
    driver.get('https://www.linkedin.com/login')
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
    
    username_field.send_keys(LINKEDIN_USERNAME)
    password_field.send_keys(LINKEDIN_PASSWORD)
    login_button.click()
    time.sleep(20)

def perform_google_search(driver, query):
    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query + Keys.RETURN)
    time.sleep(3)
    return driver.page_source

def perform_lattes_search(driver, query):
    print("Searching Lattes...")

    driver.get('https://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar')
    search_box = driver.find_element(By.NAME, 'textoBusca')
    search_box.send_keys(query)
    demaisCheckBox = driver.find_element(By.ID, 'buscarDemais')
    demaisCheckBox.click()
    search_box.send_keys(Keys.RETURN)

    time.sleep(5) 

    resultado_div = driver.find_element(By.CLASS_NAME, 'resultado')
    links = resultado_div.find_elements(By.TAG_NAME, 'a')

    scrape = []
    for link in links:
        name = link.text
        print(f'Getting: {name}')
        link.click()
        time.sleep(3) 
        
        btnAbrirCurriculo = driver.find_element(By.ID, 'idbtnabrircurriculo')
        btnAbrirCurriculo.click()
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[1])
        
        summary = driver.find_element(By.CLASS_NAME, 'resumo').text
        link = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div[1]/ul/li[1]')
        linkedin_url = get_url_in_string(link.text)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        btnfechar = driver.find_element(By.ID, 'idbtnfechar')
        btnfechar.click()

        lattes = Lattes(name, linkedin_url, summary)
        scrape.append(lattes)

        time.sleep(1)

    return scrape

def get_url_in_string(text):
    url = re.search("(?P<url>https?://[^\s]+)", text)
    if url is None:
        return None
    return url.group("url")

def extract_linkedin_urls(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    urls = set()
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        if 'linkedin.com' in href:
            clean_url = re.sub(r'\?.*', '', href)
            urls.add(clean_url)
    
    return list(urls)

def is_linkedin_url(url):
    return 'linkedin.com/in' in url

def scrape_profile_name(driver, linkedin_url):
    driver.get(linkedin_url)
    time.sleep(3)

    try:
        profile_name = driver.find_element(By.XPATH, '//*[@id="ember254"]/h1').text
        return profile_name.strip()
    except Exception as e:
        return None

def main():
    egressos = []

    name = input("Enter the name to search: ")
    query = f"{name}"
    egresso = Egresso(name)

    driver = setup_driver()
    
    try:
        scrape = perform_lattes_search(driver, query)
        for s in scrape:
            egresso.lattes_scrappes.append(s)
            egressos.append(egresso)

    except Exception as e:
        print(f"Error during search: {e}")
        return
    
    for e in egressos:
        print(e)
        print()

if __name__ == "__main__":
    main()
