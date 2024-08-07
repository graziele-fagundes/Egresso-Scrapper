class Usuario:
    def __init__(self):
        self.nome = ""
        self.email = ""
        self.senha = ""

    def criar(self, nome, email, senha):
        # Inserir no banco de dados
        self.nome = nome
        self.email = email
        self.senha = senha

        return True
    
    def logar(self, email, senha):
        # Verificar banco de dados
        self.email = email
        self.senha = senha

        return True
    
    def deslogar(self):
        return True

    def __str__(self):
        return f"Nome: {self.nome}, Email: {self.email}"

