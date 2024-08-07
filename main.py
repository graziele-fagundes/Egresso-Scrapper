from auth import Auth
from egresso import Egresso
from varredura import Varredura
from db.main import Database

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

    print("Inicializando varredura de egressos")

    driver.get('https://institucional.ufpel.edu.br/es/cursos/cod/3900')
    # time.sleep(2)
    egressos_tab = driver.find_element(By.ID, 'egre-sup')
    egressos_tab.click()
    # time.sleep(2)
    show_all = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1_length"]/label/select/option[5]')
    show_all.click()
    egressosInfo = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1"]/tbody')
    egressosInfo = egressosInfo.find_elements(By.TAG_NAME, 'tr')

    # Para testes pegar apenas os 10 primeiros
    egressos = []
    for egresso in egressosInfo[:10]:
        name = ' '.join([word for word in egresso.text.split() if not word.isdigit()])
        egressos.append(Egresso(name, 'anoFormacao', db))

    print("Varredura de egressos concluída")
    driver.quit()
    return egressos

db = Database()
def main():
    # --- Database ---
    db.criarTabelas()


    # --- Auth ---
    auth = Auth(db)
    choice = input("1 - Logar\n2 - Criar Usuário\n")
    if choice == '1':
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        usuario = auth.login(email, senha)
    elif choice == '2':
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        usuario = auth.criarUsuario(nome, email, senha)
    else:
        print("Opção inválida")
        return
    
    if usuario is None:
        print("Usuário não encontrado/criado")
        return
    else:
        print(f"Usuário logado: {usuario}")


    # --- Egressos ---
    egressos = db.getEgressos()
    if not egressos:
        egressos = get_egressos()
    else:
        print("\nEgressos encontrados no banco de dados")

    # --- Varredura Teste ---
    teste = egressos[0]
    print("\nEgresso selecionado:")
    print(teste)

    varredura = Varredura(teste)
    varredura.iniciarVarredura(setup_driver(False))

    varredura.filtrarVarreduraLattes(0)
    print("\nEgresso após varredura e filtragem:")
    print(teste)

if __name__ == "__main__":
    main()
