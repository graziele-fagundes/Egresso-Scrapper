class Usuario:
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Email: {self.email}, Senha: {self.senha}"

