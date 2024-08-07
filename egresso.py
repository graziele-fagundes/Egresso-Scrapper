from lattes import Lattes
from linkedin import Linkedin

class Egresso:
    def __init__(self, nome, anoFormacao, db, id = None, lattes = None, linkedin = None):
        if id is None:
            self.id = db.criarEgresso(nome, anoFormacao)
        else:
            self.id = id
        self.nome = nome
        self.anoFormacao = anoFormacao
        self.lattes = lattes
        self.linkedin = linkedin
        self.db = db

    def atualizarLinkedin(self, linkedin: Linkedin):
        idLinkedin = self.db.criarLinkedin(linkedin)
        linkedin.id = idLinkedin
        self.db.editarEgresso(egresso_id = self.id, novo_linkedin_id = linkedin.id)
        self.linkedin = linkedin

    def atualizarLattes(self, lattes: Lattes):
        idLattes = self.db.criarLattes(lattes)
        lattes.id = idLattes
        self.db.editarEgresso(egresso_id = self.id, novo_lattes_id = lattes.id)
        self.lattes = lattes

    def __str__(self):
        return f"ID: {self.id} Nome: {self.nome} \n Lattes: \n{self.lattes} \n Linkedin: \n{self.linkedin}"