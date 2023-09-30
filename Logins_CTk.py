import customtkinter as ctk
from tkinter import *
import sqlite3 
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk

class BackEnd():
    def conecta_db(self):
        self.conexao = sqlite3.connect("Sistema_Cadastros.db")
        self.cursor = self.conexao.cursor()
    
    def desconect_db(self):
        self.conexao.close()
    
    def criar_tabela(self):
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );                
        """)
        self.conexao.commit()
        self.desconect_db()
    
    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.password_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirmar_senha_entry.get()

        self.conecta_db()

        self.cursor.execute("""
            INSERT INTO Usuarios(Username, Email, Senha, Confirma_Senha)
            VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
        
        try:
            if (self.username_cadastro == "" or 
                self.email_cadastro == "" or
                self.senha_cadastro == "" or
                self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de Login", message="ERRO!!! \nPor favor, Preencha todos os campos!")
            elif (len(self.username_cadastro) < 4):  # Corrigido o erro aqui
                messagebox.showwarning(title="Sistema de Login", message="O Nome de Usuário deve conter pelo menos 4 caracteres.")
            elif (len(self.senha_cadastro) < 8):  # Corrigido o erro aqui
                messagebox.showwarning(title="Sistema de Login", message="A Senha de Usuário deve conter pelo menos 8 dígitos.")
            elif (self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Sistema de Login", message="ERRO!!! \nAs Senhas não Correspondem, Por Favor Insira Senhas Iguais.")
            else:
                self.conexao.commit()
                messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_cadastro}\nOs Seus Dados Foram Cadastrados com Sucesso!")
                self.desconect_db()
                self.limpar_entry_cadastro()
        except:
            messagebox.showerror(title="Sistema de Login", message="Erro no Processamento do Seu Cadastro! \nPor Favor, Tente Novamente!")
            self.desconect_db()
    
    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.password_login_entry.get()

        self.limpar_entry_login()
        self.conecta_db()

        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", (self.username_login, self.senha_login))

        self.verifica_dados = self.cursor.fetchone() 

        try:
            if (self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_login}\nLogin Realizado com Sucesso!")
                self.desconect_db()
                self.limpar_entry_login()
        except:
            messagebox.showerror(title="Sistema de Login", message="ERRO!!!\nDados Não Encontrados No Sistema!\nPor Favor, Verifique Os Seus Dados ou Cadastra-se no Nosso Sistema!")
            self.desconect_db()

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.config_janela_inicial()
        self.tela_de_login()
        self.criar_tabela()

    def config_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.resizable(False, False)

    def tela_de_login(self):
        # Trabalhando com Imagens
        self.img = Image.open("logi-img.png")
        self.img = ImageTk.PhotoImage(self.img)
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)

        self.title = ctk.CTkLabel(self, text="Faça o seu login ou Cadastre-se\nna nossa plataforma para acessar \nos nossos serviços!", font=("Century Gothic bold", 20))
        self.title.grid(row=0, column=0, pady=10, padx=10)

        self.frame_login = ctk.CTkFrame(self, width=350, height=350)
        self.frame_login.place(x=350, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça seu Login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuário",  font=("Century Gothic bold", 16), corner_radius=15, border_color="#1866a5")
        self.username_login_entry.grid(row=1 ,column=0, pady=10, padx=10)

        self.password_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Sua senha de usuário",  font=("Century Gothic bold", 16), corner_radius=15, show="*",border_color="#1866a5")
        self.password_login_entry.grid(row=2 ,column=0, pady=10, padx=10)

        # Checkbox para Verificar a Senha
        self.mostrar_senha_var = IntVar()
        self.ver_senha_login = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha", font=("Century Gothic bold", 14), variable=self.mostrar_senha_var)
        self.ver_senha_login.grid(row=3, column=0, pady=10, padx=10)
        self.mostrar_senha_var.set(0)  # Define o valor inicial da variável como 0 (caixa de seleção desmarcada)
        self.ver_senha_login.configure(command=self.mostrar_senha_login)

        self.botao_login = ctk.CTkButton(self.frame_login, width=300, text="Fazer Login",  font=("Century Gothic bold", 16), corner_radius=15, command=self.verifica_login)
        self.botao_login.grid(row=4 ,column=0, pady=10, padx=10)

        self.span = ctk.CTkLabel(self.frame_login, text="Não tem uma conta? \nRealize o cadastro no botão abaixo", font=("Century Gothic", 12))
        self.span.grid(row=5 ,column=0 , pady=10, padx=10)

        self.botao_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050" ,text="Cadastrar-se",  font=("Century Gothic bold", 16), corner_radius=15, command=self.tela_de_cadastro)
        self.botao_cadastro.grid(row=6 ,column=0, pady=10, padx=10)

    def mostrar_senha_login(self):
        if self.mostrar_senha_var.get() == 1:
            self.password_login_entry.configure(show="")
        else:
            self.password_login_entry.configure(show="*")

    def tela_de_cadastro(self):
        self.frame_login.place_forget()
        
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=350)
        self.frame_cadastro.place(x=350, y=10)
        
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça seu Login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=5)

        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuário..",  font=("Century Gothic bold", 16), corner_radius=15, border_color="#1866a5")
        self.username_cadastro_entry.grid(row=1 ,column=0, pady=5, padx=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email de usuário..",  font=("Century Gothic bold", 16), corner_radius=15, border_color="#1866a5")
        self.email_cadastro_entry.grid(row=2 ,column=0, pady=5, padx=10)

        self.password_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha de usuário..",  font=("Century Gothic bold", 16), corner_radius=15, show="*",border_color="#1866a5")
        self.password_cadastro_entry.grid(row=3 ,column=0, pady=5, padx=10)

        self.confirmar_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirmar senha de usuário..",  font=("Century Gothic bold", 16), corner_radius=15, show="*", border_color="#1866a5")
        self.confirmar_senha_entry.grid(row=4 ,column=0, pady=5, padx=10)

        self.mostrar_senha_cadastro_var = IntVar()
        self.ver_senha_cadastro = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("Century Gothic bold", 14), variable=self.mostrar_senha_cadastro_var)
        self.ver_senha_cadastro.grid(row=5, column=0, pady=10)
        self.mostrar_senha_cadastro_var.set(0)  # Define o valor inicial da variável como 0 (caixa de seleção desmarcada)
        self.ver_senha_cadastro.configure(command=self.mostrar_senha_cadastro)

        self.botao_cadastrar_usuario = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", hover_color="#050" ,text="Cadastrar-se",  font=("Century Gothic bold", 16), corner_radius=15, command=self.cadastrar_usuario)
        self.botao_cadastrar_usuario.grid(row=6 ,column=0, pady=10, padx=10)

        self.botao_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar a Tela de Login",  font=("Century Gothic bold", 16), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.botao_login_back.grid(row=7 ,column=0, pady=10, padx=10)

    def limpar_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.password_cadastro_entry.delete(0, END)
        self.confirmar_senha_entry.delete(0, END)

    def limpar_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

    def mostrar_senha_cadastro(self):
        if self.mostrar_senha_cadastro_var.get() == 1:
            self.password_cadastro_entry.configure(show="")
            self.confirmar_senha_entry.configure(show="")
        else:
            self.password_cadastro_entry.configure(show="*")
            self.confirmar_senha_entry.configure(show="*")

if __name__ == "__main__":
    app = App()
    app.mainloop()