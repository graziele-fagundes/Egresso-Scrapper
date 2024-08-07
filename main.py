from usuario import Usuario
from egresso import Egresso
from varredura import Varredura

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
    egressosInfo = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1"]/tbody')
    egressosInfo = egressosInfo.find_elements(By.TAG_NAME, 'tr')

    egressos = []
    for egresso in egressosInfo:
        name = ' '.join([word for word in egresso.text.split() if not word.isdigit()])
        egressos.append(Egresso(name, 'email', 'curso', 'anoFormacao'))

    print(f"Found {len(egressos)} egressos.")
    driver.quit()
    return egressos


def main():
    # Login
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    usuario = Usuario()
    if not usuario.logar(email, senha):
        print("Falha ao logar.")
        return

    # Scrappe egressos names
    egressos = get_egressos()

    # Varredura
    teste = egressos[0]
    print(teste)

    varredura = Varredura(teste)
    varredura.iniciarVarredura(setup_driver())

    varredura.filtrarVarreduraLattes(0)
    print(teste)
if __name__ == "__main__":
    main()
