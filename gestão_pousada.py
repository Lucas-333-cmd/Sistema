import tkinter as tk
from tkinter import messagebox
import sqlite3

#-----------------------------BANCO DE DADOS SQLITE2------------------------------
class SistemaGestaoHoteleira:
    def __init__(self, arquivo_banco_dados):
        self.arquivo_banco_dados = arquivo_banco_dados
        self.conexao = sqlite3.connect(self.arquivo_banco_dados)
        self.c = self.conexao.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS hospedes
                         (id INTEGER PRIMARY KEY,
                          nome TEXT,
                          sobrenome TEXT,
                          cpf INTEGER,  
                          email TEXT,
                          ddd INTEGER,
                          telefone INTEGER, 
                          idade INTEGER,
                          quantidade_adultos INTEGER,
                          quantidade_criancas INTEGER,
                          dependentes INTEGER,
                          data_checkin TEXT,
                          data_checkout TEXT)''')
        self.conexao.commit()

#função para fazer a reserva
    def fazer_reserva(self, dados_reserva):
        try:
            self.c.execute('''INSERT INTO hospedes (nome, sobrenome, cpf, email, ddd, telefone, idade, 
                           quantidade_adultos, quantidade_criancas, data_checkin, data_checkout)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (dados_reserva['nome'],
                                                             dados_reserva['sobrenome'],
                                                             dados_reserva['cpf'],
                                                             dados_reserva['email'],
                                                             dados_reserva['ddd'], 
                                                             dados_reserva['telefone'],
                                                             dados_reserva['idade'],
                                                             dados_reserva['quantidade_adultos'],
                                                             dados_reserva['quantidade_criancas'],
                                                             dados_reserva['data_checkin'], 
                                                             dados_reserva['data_checkout']))
            self.conexao.commit()
            return True
        except sqlite3.Error as e:
            print("Erro ao fazer reserva:", e)
            return False
        
#-----------------------------FORMATAÇÕES DE DADOS------------------------------
        
# Classe para formatar a data
class DateEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.format_date)

    def format_date(self, event):
        current_text = self.get()

        if len(current_text) > 10:
            current_text = current_text[:10]

        self.delete(0, tk.END)
        
        if len(current_text) >= 3:
            if current_text[2] != '/':
                current_text = current_text[:2] + '/' + current_text[2]
            if len(current_text) >= 6:
                if current_text[5] != '/':
                    current_text = current_text[:5] + '/' + current_text[5:]
        
        self.insert(0, current_text)

#Classe para formatar CPF
class cpfEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.format_cpf)

    def format_cpf(self, event):
        current_text = self.get()

        if len(current_text) > 14:
            current_text = current_text[:14]

        self.delete(0, tk.END)
        
        if len(current_text) >= 4:
            if current_text[3] != '.':
                current_text = current_text[:3] + '.' + current_text[3]
        if len(current_text) >= 8:
            if current_text[7] != '.':
                current_text = current_text[:7] + '.' + current_text[7]
        if len(current_text) >= 12:
            if current_text[11] != '-':
                current_text = current_text[:11] + '-' + current_text[11:]
        
        self.insert(0, current_text)

#Classe para formatar telefone
class telefoneEntry(tk.Entry):
    def __init__(self, master =None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.format_telefone)

    def format_telefone(self, event):
        current_text = self.get()

        if len(current_text) > 13:
            current_text = current_text[:13]

        self.delete(0, tk.END)
        
        if len(current_text) >= 3:
            if current_text[2] != ' ':
                current_text = current_text[:2] + ' ' + current_text[2]
        if len(current_text) >= 9:
            if current_text[8] != '-':
                current_text = current_text[:8] + '-' + current_text[8]

        self.insert(0, current_text)

#Classe para formatar nome e sobrenome em letras MAIUSCULAS
class nomeEntry(tk.Entry):
    def __init__(self, master =None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.format_nome)

    def format_nome(self, event):
        current_text = self.get()
        current_text = current_text.upper()
        self.delete(0, tk.END)
        self.insert(0, current_text)

#------------------------------INTERFACE GRÁFICA---------------------------------
        
class AplicacaoGUI:
    def __init__(self, master, arquivo_banco_dados):
        self.master = master
        self.arquivo_banco_dados = arquivo_banco_dados
        self.sistema = SistemaGestaoHoteleira(arquivo_banco_dados)
        master.title("Sistema de Gestão Hoteleira")

        tk.Label(master, text="Nome:").grid(row=0, column=0, sticky="e")
        self.entry_nome = nomeEntry(master)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(master, text="Sobrenome:").grid(row=0, column=2, sticky="e")
        self.entry_sobrenome = nomeEntry(master)
        self.entry_sobrenome.grid(row=0, column=3)

        tk.Label(master, text="CPF:").grid(row=2, column=0, sticky="e")
        self.entry_cpf = cpfEntry(master)
        self.entry_cpf.grid(row=2, column=1)

        tk.Label(master, text="Email:").grid(row=2, column=2, sticky="e")
        self.entry_email = tk.Entry(master)
        self.entry_email.grid(row=2, column=3)

        tk.Label(master, text="Telefone:").grid(row=4, column=0, sticky="e")
        self.entry_telefone = telefoneEntry(master)
        self.entry_telefone.grid(row=4, column=1)

        tk.Label(master, text="idade:").grid(row=4, column=2, sticky="e")
        self.entry_ddd = tk.Entry(master)
        self.entry_ddd.grid(row=4, column=3)

        tk.Label(master, text="Quantidade de Adultos:").grid(row=5, column=0, sticky="w")
        self.entry_adultos = tk.Entry(master)
        self.entry_adultos.grid(row=5, column=1)

        tk.Label(master, text="Quantidade de Criancas:").grid(row=5, column=2, sticky="e")
        self.entry_criancas = tk.Entry(master)
        self.entry_criancas.grid(row=5, column=3)

        tk.Label(master, text="Data de Check-in:").grid(row=6, column=0, sticky="e")
        self.entry_data_checkin = DateEntry(master)
        self.entry_data_checkin.grid(row=6, column=1)

        tk.Label(master, text="Data de Check-out:").grid(row=6, column=2, sticky="e")
        self.entry_data_checkout = DateEntry(master)
        self.entry_data_checkout.grid(row=6, column=3)

        tk.Button(master, 
                  text="Fazer Reserva", 
                  bg = "green",
                  fg = "white",
                  command=self.fazer_reserva).grid(row=8, column=3, columnspan=1)
        tk.Button(master, 
                  text="Apagar Dados",
                  bg="red", 
                  fg = "white",
                  command=self.limpar_campos).grid(row=8, column=0, columnspan=1)

    def fazer_reserva(self):
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        cpf = self.entry_cpf.get()
        email = self.entry_email.get()
        ddd = self.entry_telefone.get()[:2]
        idade = self.entry_ddd.get()
        adultos = self.entry_adultos.get()
        criancas = self.entry_criancas.get()
        telefone = self.entry_telefone.get()
        checkin = self.entry_data_checkin.get()
        checkout = self.entry_data_checkout.get()

        if not nome or not cpf or not email or not telefone or not checkin or not checkout:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return
        
        dados_reserva = {
            "nome": nome.upper(),
            "sobrenome": sobrenome.upper(),
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "ddd": ddd,
            "idade": idade,
            "quantidade_adultos": adultos,
            "quantidade_criancas": criancas,
            "data_checkin": checkin,
            "data_checkout": checkout
        }

        sucesso = self.sistema.fazer_reserva(dados_reserva)

        if sucesso:
            messagebox.showinfo("Reserva Efetuada", "Reserva feita com sucesso!")
        else:
            messagebox.showerror("Erro", "Erro ao fazer reserva")

#função que limpa os campos digitados ao comando do botão de limpar
    def limpar_campos(self):
        campos = [self.entry_nome,
                self.entry_sobrenome,   
                self.entry_cpf, 
                self.entry_email,
                self.entry_ddd, 
                self.entry_telefone,
                self.entry_adultos,
                self.entry_criancas,
                self.entry_data_checkin, 
                self.entry_data_checkout]

        for campo in campos:
            campo.delete(0, tk.END)

arquivo_banco_dados = 'banco_de_dados_hotel.db'

root = tk.Tk()
app = AplicacaoGUI(root, arquivo_banco_dados)
root.mainloop()
