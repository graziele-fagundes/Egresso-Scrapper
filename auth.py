from usuario import Usuario
from db.main import Database

class Auth:
    def __init__(self, db: Database):
        self.db = db
        pass

    def criarUsuario(self, nome, email, senha):
        id = self.db.criarUsuario(nome, email, senha)
         
        if id is None:
            return None
 
        return Usuario(id, nome, email, senha)
    
    def login(self, email, senha):
        user = self.db.login(email, senha)

        if user is None:
            return None
        
        return Usuario(user[0], user[1], user[2], user[3])
