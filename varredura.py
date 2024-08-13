from datetime import date
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
from utils import get_url_in_string
from lattes import Lattes
from linkedin import Linkedin

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

            self.varreduraLinkedin(driver)
            self.varreduraLattes(driver)
            driver.quit()
            
            self.status = "Concluída"
        except Exception as e:
            self.status = "Erro"
            print(f"Erro na varredura: {e}")
        
        print(f'Varredura para {self.egresso.nome} concluída')
        return
    
    def varreduraLinkedin(self, driver):
        query = self.egresso.nome + ' linkedin'

        driver.get('https://www.google.com/')
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        linkedin_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'linkedin.com/in')]")
        
        for link in linkedin_links[:3]:
            url_text = link.text
            url = link.get_attribute('href')
 
            parts = url_text.split("LinkedIn Brasil")[0].strip()
            parts = parts.split("-")

            name = ""
            if len(parts) > 1:
                name = parts[0].strip()

            summary = ""
            for part in parts[1:]:
                summary += part.strip() + " "

            time.sleep(1)
            driver.execute_script("window.open('about:blank', '_blank')")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
            time.sleep(2)
            
            if driver.current_url != url:
                linkedin = Linkedin(name, url, summary)
                self.linkedin.append(linkedin)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            try:
                signin_modal = driver.find_element(By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div')
                if signin_modal:
                    close_btn = driver.find_element(By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/button')
                    if close_btn:
                        close_btn.click()
                    time.sleep(1)
            except:
                pass

            try:
                name = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div/button/h1').text 
            except:
                pass

            try:
                summary_section = driver.find_element(By.XPATH, '/html/body/main/section[1]/div/section/section[2]/div/p/text()[1]')
                summary = summary_section.text
            except:
                pass

            linkedin = Linkedin(name, url, summary)
            self.linkedin.append(linkedin)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
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
