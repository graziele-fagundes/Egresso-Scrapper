import time
from lattes import Lattes

class Egresso:
    def __init__(self, nome, email: None, curso: None, anoFormacao: None):
        #Inserir no banco de dados
        self.nome = nome
        self.email = email
        self.curso = curso
        self.anoFormacao = anoFormacao
        self.lattes = None
        self.linkedin = None

    def atualizarLinkedin(self,linkedin):
        # Atualizar no banco de dados
        self.linkedin = linkedin

    def atualizarLattes(self,lattes):
        # Atualizar no banco de dados
        self.lattes = lattes

    def __str__(self):
        return f"Nome: {self.nome} \n Lattes: {self.lattes} \n Linkedin: {self.linkedin}"