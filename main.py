from auth import Auth
from egresso import Egresso
from varredura import Varredura

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = 'chrome/chromedriver.exe' 

def setup_driver(headless):
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_egressos():
    driver = setup_driver(True)

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
        egressos.append(Egresso(name, 'anoFormacao'))

    print(f"Found {len(egressos)} egressos.")
    driver.quit()
    return egressos


def main():
    # Login
    auth = Auth()
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    usuario = auth.login(email, senha)

    if usuario is None:
        print("Usuário não encontrado.")
        return
    else:
        print(f"Usuário logado: {usuario}")

    # Scrappe egressos
    egressos = get_egressos()

    # Varredura de egressos
    teste = egressos[0]
    print(teste)

    varredura = Varredura(teste)
    varredura.iniciarVarredura(setup_driver(False))

    varredura.filtrarVarreduraLattes(0)
    print(teste)

if __name__ == "__main__":
    main()
