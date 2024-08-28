import time
from threading import Thread

import tkinter as tk
from tkinter import messagebox

from selenium.webdriver.common.by import By

from auth import Auth
from egresso import Egresso
from varredura import Varredura
from db.main import Database
from utils import setup_driver
from PIL import Image, ImageTk


def get_egressos():
    driver = setup_driver(True)

    print("Inicializando varredura de egressos")

    driver.get('https://institucional.ufpel.edu.br/es/cursos/cod/3900')
    # time.sleep(2)
    egressos_tab = driver.find_element(By.ID, 'egre-sup')
    egressos_tab.click()
    # time.sleep(2)
    show_all = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1_length"]/label/select/option[5]')
    show_all.click()
    egressosInfo = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1"]/tbody')
    egressosInfo = egressosInfo.find_elements(By.TAG_NAME, 'tr')

    # Para testes pegar apenas os 10 primeiros
    egressos = []
    for egresso in egressosInfo[:10]:
        name = ' '.join([word for word in egresso.text.split() if not word.isdigit()])
        anoFormacao = egresso.text.split()[-1]
        egressos.append(Egresso(name, anoFormacao, db))

    print("Varredura de egressos concluída")
    driver.quit()
    return egressos

db = Database()
auth = Auth(db)
usuario = None

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Egressos")
        self.root.geometry("400x400") 
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.setup_screen("Login", "250x170")
        
        tk.Label(self.root, text="Email:").grid(row=0, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
        self.senha_entry = tk.Entry(self.root, show="*")
        self.senha_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Login", command=self.validate_login).grid(row=2, columnspan=2, pady=5)
        tk.Button(self.root, text="Registrar", command=self.create_register_screen).grid(row=3, columnspan=2, pady=5)

    def create_register_screen(self):
        self.clear_screen()
        self.setup_screen("Registrar", "250x170")
        
        tk.Label(self.root, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
        self.nome_entry = tk.Entry(self.root)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Senha:").grid(row=2, column=0, padx=10, pady=10)
        self.senha_entry = tk.Entry(self.root, show="*")
        self.senha_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Cancelar", command=self.create_login_screen).grid(row=3, column=0, pady=10, padx=20)
        tk.Button(self.root, text="Registrar", command=self.validate_register).grid(row=3, column=1, pady=10)

    def validate_register(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        try:
            auth.criarUsuario(nome, email, senha)
            self.create_login_screen()
        except:
            messagebox.showerror("Erro", "Erro ao criar usuário")

    def validate_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        usuario = auth.login(email, senha)

        if usuario:
            self.create_egressos_screen()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def center_other_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_screen(self, title, geometry):
        self.root.title(title)
        self.root.geometry(geometry)
        self.center_window()

    def create_egressos_screen(self):
        self.clear_screen()
        self.setup_screen("Egresso Scrapper", "650x600")
        
        tk.Button(self.root, text="Buscar Egressos", command=self.buscar_egressos).pack(pady=10)

        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.egressos_list_frame = tk.Frame(canvas)

        self.egressos_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.egressos_list_frame, anchor="nw")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        self.egressos = db.getEgressos()
        if self.egressos:
            print("\nEgressos encontrados no banco de dados")
        self.display_egressos()

    def buscar_egressos(self):
        self.root.config(cursor="watch")
        self.root.update_idletasks()
        db.deleteEgressos()
        self.egressos = get_egressos()
        self.display_egressos()
        self.root.config(cursor="")
        
    def display_egressos(self):
        for widget in self.egressos_list_frame.winfo_children():
            widget.destroy()

        for i, egresso in enumerate(self.egressos):
            frame = tk.Frame(self.egressos_list_frame, borderwidth=1, relief="solid", pady=5)
            frame.pack(fill=tk.X, padx=10, pady=5)

            label_text = f"{egresso.nome} ({egresso.anoFormacao})\nLattes: "
            if egresso.lattes:
                label_text += f"{egresso.lattes.nome} - {egresso.lattes.url}"
            label_text += "\nLinkedin: "
            if egresso.linkedin:
                label_text += f"{egresso.linkedin.nome} - {egresso.linkedin.url}"

            # Cria o Label e o posiciona na grid com a expansão adequada
            # Cria o Button e o posiciona na grid
            tk.Label(frame, text=label_text, anchor="w", justify="left").grid(row=0, column=0, sticky="w", padx=10)
            tk.Button(frame, text="Varredura", command=lambda e=egresso: self.varrer_egresso(e)).grid(row=0, column=1, padx=10, sticky="e")

            # Configura as colunas para ajustar o layout
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=0)

    def varrer_egresso(self, egresso):
        # Cria a janela de progresso
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Progresso da Varredura")
        self.progress_window.geometry("300x300")
        self.center_other_window(self.progress_window)

        # Define o tamanho máximo da imagem
        max_width, max_height = 100, 200  # Defina as dimensões desejadas

        # Carrega a imagem original e redimensiona
        original_image = Image.open("images/broom.png")
        original_image = original_image.resize((max_width, max_height))  # Redimensiona a imagem

        mirrored_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)  # Cria a versão espelhada da imagem

        # Converte as imagens para PhotoImage do Tkinter
        original_photo = ImageTk.PhotoImage(original_image)
        mirrored_photo = ImageTk.PhotoImage(mirrored_image)

        # Label para exibir a imagem
        self.image_label = tk.Label(self.progress_window)
        self.image_label.pack(pady=10)

        # Função para alternar a imagem
        def update_image(mirrored):
            if mirrored:
                self.image_label.configure(image=mirrored_photo)
            else:
                self.image_label.configure(image=original_photo)
            self.progress_window.after(500, update_image, not mirrored)  # Alterna a cada 500 ms

        # Inicia a alternância da imagem
        self.progress_window.after(0, update_image, False)

        # Mensagem de varredura em andamento
        tk.Label(self.progress_window, text="Varredura em andamento...").pack(pady=10)

        # Define a função de varredura em uma thread separada
        def tarefa_varredura():
            self.root.config(cursor="watch")
            varredura = Varredura(egresso)
            varredura.iniciarVarredura(setup_driver(True))
            self.show_varredura_results(varredura, varredura.lattes, varredura.linkedin)
            self.root.config(cursor="")
            self.progress_window.destroy()

        # Inicia a thread para executar a tarefa de varredura
        Thread(target=tarefa_varredura).start()

    def show_varredura_results(self, varredura, resultados_lattes, resultados_linkedin):          
        varredura_window = tk.Toplevel(self.root)
        varredura_window.title("Resultados da Varredura para " + varredura.egresso.nome)
        varredura_window.geometry("500x300")
        self.center_other_window(varredura_window)

        tk.Label(varredura_window, text="Lattes (double click):").pack(pady=5)

        listbox = tk.Listbox(varredura_window, height=4)
        listbox.pack(fill=tk.X, expand=True, padx=10, pady=0)

        for i, resultado in enumerate(resultados_lattes):
            listbox.insert(tk.END, f"{resultado.nome} - {resultado.url} - {resultado.resumo}")

        def on_select_lattes(event):
            selected_index = listbox.curselection()
            if selected_index:
                index = selected_index[0] 
                varredura.filtrarVarreduraLattes(index)
                for i in range(len(resultados_lattes)):
                    if i != index:
                        listbox.itemconfig(i, fg="black", bg="white", selectbackground="white", selectforeground="black")
                listbox.itemconfig(index, fg="red", bg="yellow", selectbackground="yellow", selectforeground="red")
                
        listbox.bind("<Double-1>", on_select_lattes)

        def copy_lattes_selection():
            selected_index = listbox.curselection()
            if selected_index:
                index = selected_index[0]
                selected_text = listbox.get(index)
                _, url, _ = selected_text.split(' - ', 2)
                varredura_window.clipboard_clear()
                varredura_window.clipboard_append(url)
                varredura_window.update()

        copy_button_lattes = tk.Button(varredura_window, text="Copiar Seleção Lattes", command=copy_lattes_selection)
        copy_button_lattes.pack(pady=5)

        divisor = tk.Frame(varredura_window, height=2, bd=1, relief=tk.SUNKEN)
        divisor.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(varredura_window, text="Linkedin (double click):").pack(pady=5)

        listbox2 = tk.Listbox(varredura_window, height=4)
        listbox2.pack(fill=tk.X, expand=True, padx=10, pady=0)

        for i, resultado in enumerate(resultados_linkedin):
            listbox2.insert(tk.END, f"{resultado.nome} - {resultado.url} - {resultado.resumo}")
        
        def on_select_linkedin(event):
            selected_index = listbox2.curselection()
            if selected_index:
                index = selected_index[0] 
                varredura.filtrarVarreduraLinkedin(index)
                for i in range(len(resultados_linkedin)):
                    if i != index:
                        listbox2.itemconfig(i, fg="black", bg="white", selectbackground="white", selectforeground="black")
                listbox2.itemconfig(index, fg="red", bg="yellow", selectbackground="yellow", selectforeground="red")
        
        listbox2.bind("<Double-1>", on_select_linkedin)

        def copy_linkedin_selection():
            selected_index = listbox2.curselection()
            if selected_index:
                index = selected_index[0]
                selected_text = listbox2.get(index)
                _, url, _ = selected_text.split(' - ', 2)
                varredura_window.clipboard_clear()
                varredura_window.clipboard_append(url)
                varredura_window.update()

        copy_button_linkedin = tk.Button(varredura_window, text="Copiar Seleção Linkedin", command=copy_linkedin_selection)
        copy_button_linkedin.pack(pady=5)

        def on_close():
            varredura_window.destroy()
            self.display_egressos()

        varredura_window.protocol("WM_DELETE_WINDOW", on_close)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    db.criarTabelas()

    root = tk.Tk()
    app = App(root)
    root.mainloop()
    
