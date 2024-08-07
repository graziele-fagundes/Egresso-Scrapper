from datetime import date
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import get_url_in_string
from lattes import Lattes

class Varredura:
    def __init__(self, egresso):
        self.data = date.today()
        self.egresso = egresso
        self.status = "Não Iniciada"
        self.linkedin = []
        self.lattes = []    
    
    def filtrarVarreduraLattes(self, index):
        self.egresso.atualizarLattes(self.lattes[index])

    def filtrarVarreduraLinkedin(self, index):
        self.egresso.atualizarLinkedin(self.linkedin[index])

    def iniciarVarredura(self, driver):
        print(f'Iniciando varredura para {self.egresso.nome}')

        try:
            self.data = date.today()
            self.status = "Iniciada"
            self.varreduraLattes(driver)
            self.varreduraLinkedin(driver)
            self.status = "Concluída"
        except Exception as e:
            self.status = "Erro"
            print(f"Erro na varredura: {e}")
        
        print(f'Varredura para {self.egresso.nome} concluída')
        return
    
    def varreduraLinkedin(self, driver):
        # Falta varredura do linkedin (precisa de login, pegar perfil do chrome logado)
        return

    def varreduraLattes(self, driver):
        query = self.egresso.nome

        driver.get('https://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar')
        search_box = driver.find_element(By.NAME, 'textoBusca')
        search_box.send_keys(query)
        demaisCheckBox = driver.find_element(By.ID, 'buscarDemais')
        demaisCheckBox.click()
        search_box.send_keys(Keys.RETURN)

        time.sleep(2) 

        resultado_div = driver.find_element(By.XPATH, '/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]')
        links = resultado_div.find_elements(By.TAG_NAME, 'a')

        for link in links[:3]:
            name = link.text
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
            self.lattes.append(lattes)

            time.sleep(1)

