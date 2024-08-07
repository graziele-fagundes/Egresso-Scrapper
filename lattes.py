class Lattes:
    def __init__(self, nome, url, resumo):
        self.nome = nome
        self.url = url
        self.resumo = resumo

    def __str__(self):
        return f"Nome: {self.nome}\nURL: {self.url}\nResumo: {self.resumo}"
