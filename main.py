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
        s += "Resultados Lattes:\n"
        for lattes in self.lattes_scrappes:
            s += f"{lattes}\n"
            s += "\n"

        return s
    
    def scrape_lattes(self, driver):
        query = self.name

        print("Searching Lattes...")

        driver.get('https://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar')
        search_box = driver.find_element(By.NAME, 'textoBusca')
        search_box.send_keys(query)
        demaisCheckBox = driver.find_element(By.ID, 'buscarDemais')
        demaisCheckBox.click()
        search_box.send_keys(Keys.RETURN)

        time.sleep(2) 

        # resultado_div = driver.find_element(By.CLASS_NAME, 'resultado')
        resultado_div = driver.find_element(By.XPATH, '/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]')
        links = resultado_div.find_elements(By.TAG_NAME, 'a')

        for link in links[:3]:
            name = link.text
            print(f'Getting: {name}')
            link.click()
            time.sleep(2) 
            
            btnAbrirCurriculo = driver.find_element(By.ID, 'idbtnabrircurriculo')
            btnAbrirCurriculo.click()
            time.sleep(2)

            driver.switch_to.window(driver.window_handles[1])
            
            summary = driver.find_element(By.CLASS_NAME, 'resumo').text
            link = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div[1]/ul/li[1]')
            linkedin_url = get_url_in_string(link.text)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            btnfechar = driver.find_element(By.ID, 'idbtnfechar')
            btnfechar.click()

            lattes = Lattes(name, linkedin_url, summary)
            self.lattes_scrappes.append(lattes)

            time.sleep(1)

        print("Lattes done.")
        return
    
class Lattes:
    def __init__(self, name, url, summary):
        self.name = name
        self.lattes_url = url
        self.lattes_summary = summary

    def __str__(self):
        return f"Nome: {self.name}\nURL: {self.lattes_url}\nResumo: {self.lattes_summary}"

CHROMEDRIVER_PATH = 'chromedriver.exe' 

def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Runs Chrome in headless mode (without a GUI)
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


def get_egressos():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode (without a GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("Getting egressos...")

    driver.get('https://institucional.ufpel.edu.br/es/cursos/cod/3900')
    # time.sleep(2)
    egressos_tab = driver.find_element(By.ID, 'egre-sup')
    egressos_tab.click()
    # time.sleep(2)
    show_all = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1_length"]/label/select/option[5]')
    show_all.click()
    egressos = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1"]/tbody')
    egressos = egressos.find_elements(By.TAG_NAME, 'tr')

    names = []
    for egresso in egressos:
        name = ' '.join([word for word in egresso.text.split() if not word.isdigit()])
        names.append(name)

    print(f"Found {len(names)} egressos.")
    driver.quit()
    return names


def main():
    names = get_egressos()
    limit = int(input("Quantos egressos deseja buscar? "))

    egressos = []
    driver = setup_driver()
    try:
        for name in names[:limit]:
            egresso = Egresso(name)
            egresso.scrape_lattes(driver)
            egressos.append(egresso)
    except Exception as e:
        print(f"Error during search: {e}")
        return
    
    print()
    print("-----------------------------------------------------------------------------------------")
    for e in egressos:
        print(e)
        print("-----------------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
