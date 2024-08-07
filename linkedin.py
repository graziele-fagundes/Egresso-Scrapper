class Linkedin:
    def __init__(self, nome, url, resumo, id = None):
        self.id = id
        self.nome = nome
        self.url = url
        self.resumo = resumo

    def __str__(self):
        return f"ID: {self.id} Nome: {self.nome}\nURL: {self.url}\nResumo: {self.resumo}"
