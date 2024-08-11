import sqlite3
from egresso import Egresso
from linkedin import Linkedin
from lattes import Lattes

class Database:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
    
    def criarTabelas(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Criação da tabela Usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                ID INTEGER PRIMARY KEY,
                Nome TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                Senha TEXT NOT NULL
            )
        ''')

        # Criação da tabela Linkedin
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Linkedin (
                ID INTEGER PRIMARY KEY,
                Nome TEXT NOT NULL,
                Url TEXT NOT NULL UNIQUE,
                Resumo TEXT
            )
        ''')

        # Criação da tabela Lattes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Lattes (
                ID INTEGER PRIMARY KEY,
                Nome TEXT NOT NULL,
                Url TEXT NOT NULL UNIQUE,
                Resumo TEXT
            )
        ''')

        # Criação da tabela Egresso
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Egresso (
                ID INTEGER PRIMARY KEY,
                Nome TEXT NOT NULL,
                anoFormacao TEXT,
                Linkedin INTEGER,
                Lattes INTEGER,
                FOREIGN KEY (Linkedin) REFERENCES Linkedin(ID),
                FOREIGN KEY (Lattes) REFERENCES Lattes(ID)
            )
        ''')

        conn.commit()
        conn.close()

    def criarUsuario(self, nome, email, senha):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO Usuario (Nome, Email, Senha)
                VALUES (?, ?, ?)
            ''', (nome, email, senha))

            conn.commit()
            conn.close()
            return cursor.lastrowid
        
        except sqlite3.IntegrityError as e:
            print(f"Erro ao criar usuário: {e}")
            conn.close()
            return None    


    def login(self, email, senha):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT ID, Nome, Email, Senha
            FROM Usuario 
            WHERE Email = ? AND Senha = ?
        ''', (email, senha))

        user = cursor.fetchone()
        conn.close()

        return user
        
    def criarLinkedin(self, linkedin):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Verificar se o registro com o mesmo URL já existe
            cursor.execute('SELECT ID FROM Linkedin WHERE Url = ?', (linkedin.url,))
            existing_record = cursor.fetchone()

            if existing_record is not None:
                linkedin_id = existing_record[0]
                return linkedin_id

            # Inserir um novo registro na tabela Linkedin
            cursor.execute('''
                INSERT INTO Linkedin (Nome, Url, Resumo)
                VALUES (?, ?, ?)
            ''', (linkedin.nome, linkedin.url, linkedin.resumo))
            conn.commit()

            # Obter o ID do registro recém-criado
            linkedin_id = cursor.lastrowid
            return linkedin_id

        except sqlite3.Error as e:
            print(f"Erro ao criar Linkedin: {e}")
            return None
        finally:
            conn.close()

    
    def criarLattes(self, lattes):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Verificar se o registro com o mesmo URL já existe
            cursor.execute('SELECT ID FROM Lattes WHERE Url = ?', (lattes.url,))
            existing_record = cursor.fetchone()

            if existing_record is not None:
                lattes_id = existing_record[0]
                return lattes_id

            # Inserir um novo registro na tabela Lattes
            cursor.execute('''
                INSERT INTO Lattes (Nome, Url, Resumo)
                VALUES (?, ?, ?)
            ''', (lattes.nome, lattes.url, lattes.resumo))
            conn.commit()

            # Obter o ID do registro recém-criado
            lattes_id = cursor.lastrowid
            return lattes_id

        except sqlite3.Error as e:
            print(f"Erro ao criar Lattes: {e}")
            return None
        finally:
            conn.close()

    def deleteEgressos(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM Egresso')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao deletar egressos: {e}")
        finally:
            conn.close()
            
    def getEgressos(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT ID, Nome, anoFormacao, Linkedin, Lattes FROM Egresso')
            consulta = cursor.fetchall()

            egressos = []
            for e in consulta:
                cursor.execute('SELECT ID, Nome, Url, Resumo FROM Linkedin WHERE ID = ?', (e[3],))
                linkedin = cursor.fetchone()
                linkedinObj = None
                if linkedin is not None:
                     linkedinObj = Linkedin(id = linkedin[0], nome = linkedin[1], url = linkedin[2], resumo = linkedin[3])

                cursor.execute('SELECT ID, Nome, Url, Resumo FROM Lattes WHERE ID = ?', (e[4],))
                lattes = cursor.fetchone()
                lattesObj = None
                if lattes is not None:
                    lattesObj = Lattes(id = lattes[0], nome = lattes[1], url = lattes[2], resumo = lattes[3])
                   

                egresso = Egresso(id = e[0], lattes = lattesObj, linkedin = linkedinObj, nome = e[1], anoFormacao = e[2], db = self)
                egressos.append(egresso)
                
            return egressos

        except sqlite3.Error as e:
            print(f"Erro ao recuperar egressos: {e}")
            return None
        finally:
            conn.close()

    def criarEgresso(self, nome, ano_formacao, linkedin_id=None, lattes_id=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Verificar se o Linkedin ID e Lattes ID existem (se fornecidos)
            if linkedin_id is not None:
                cursor.execute('SELECT ID FROM Linkedin WHERE ID = ?', (linkedin_id,))
                if cursor.fetchone() is None:
                    raise ValueError("Linkedin ID não encontrado.")
            
            if lattes_id is not None:
                cursor.execute('SELECT ID FROM Lattes WHERE ID = ?', (lattes_id,))
                if cursor.fetchone() is None:
                    raise ValueError("Lattes ID não encontrado.")
            
            # Inserir um novo registro na tabela Egresso, ignorando se o Nome já existir
            cursor.execute('''
                INSERT OR IGNORE INTO Egresso (Nome, anoFormacao, Linkedin, Lattes)
                VALUES (?, ?, ?, ?)
            ''', (nome, ano_formacao, linkedin_id, lattes_id))

            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Erro ao criar egresso: {e}")
        except ValueError as ve:
            print(f"Erro de validação: {ve}")
        finally:
            conn.close()


    def editarEgresso(self, egresso_id, novo_linkedin_id=None, novo_lattes_id=None):
        # Conexão ao banco de dados SQLite
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Verificar se o egresso existe
            cursor.execute('SELECT ID FROM Egresso WHERE ID = ?', (egresso_id,))
            if cursor.fetchone() is None:
                raise ValueError("Egresso ID não encontrado.")
            
            # Verificar se o novo Linkedin ID existe (se fornecido)
            if novo_linkedin_id is not None:
                cursor.execute('SELECT ID FROM Linkedin WHERE ID = ?', (novo_linkedin_id,))
                if cursor.fetchone() is None:
                    raise ValueError("Linkedin ID não encontrado.")
            
            # Verificar se o novo Lattes ID existe (se fornecido)
            if novo_lattes_id is not None:
                cursor.execute('SELECT ID FROM Lattes WHERE ID = ?', (novo_lattes_id,))
                if cursor.fetchone() is None:
                    raise ValueError("Lattes ID não encontrado.")
            
            # Atualizar os campos Linkedin e Lattes do egresso
            cursor.execute('''
                UPDATE Egresso
                SET Linkedin = ?, Lattes = ?
                WHERE ID = ?
            ''', (novo_linkedin_id, novo_lattes_id, egresso_id))

            # Commit da transação
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Erro ao atualizar egresso: {e}")
        except ValueError as ve:
            print(f"Erro de validação: {ve}")
        finally:
            # Fechar a conexão
            conn.close()


