from usuario import Usuario

class Auth:
    def __init__(self):
        pass

    def criarUsuario(self, nome, email, senha):
        # Consulta banco de dados para verificar se o usuário já existe
        # Se não existir, cria o usuário
        usuario = Usuario(nome, email, senha)
        return usuario
    
    def login(self, email, senha):
        # Consulta banco de dados para verificar se o usuário existe
        # Se existir, retorna o usuário
        usuario = Usuario("Nome", email, senha)
        return usuario
