import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk #usar o pillow
import webbrowser   
import requests
import json
import os

def abrir_github():
    url = "https://github.com/guerra14git" #mudar o repo para o atualizado
    webbrowser.open(url)

#class da janela principal
class App(tk.Tk): 
    def __init__(self): #construtor da classe 
        super().__init__() #inicializa a janela do tkinter dentro da classe App
        self.geometry("860x620")
        self.title("Planeamento de Refeições")
        self.iconbitmap("trabalho_lab_2\icon_circle.ico") #icon
#temas tkinter: https://github.com/rdbende/Forest-ttk-theme.git
        self.tk.call('source', r'trabalho_lab_2\Forest-ttk-theme-master\forest-light.tcl')
        ttk.Style().theme_use('forest-light')
        self.tema_atual = "light" ##usar ttk para theme e tk para tkinter original theme
#telas ou frames
        self.tela_home = TelaHome(self)
        self.tela_refeicoes = TelaRefeicoes(self)
        self.tela_ingredientes = TelaIngredientes(self)
        self.tela_receitas = TelaReceitas(self)
        self.tela_receitas_favoritas = TelaFavoritas(self)
        self.tela_lista = TelaListaCompras(self)
        self.tela_cozinhas = TelaCozinhas(self)

        style = ttk.Style()
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(10, 6),              
        )

#este for coloca os 3 frames na mesma posicao, para quando tivermos de envocar cada tela
        for tela in (self.tela_home, self.tela_ingredientes,self.tela_receitas, self.tela_receitas_favoritas, self.tela_lista, self.tela_restaurantes):
            tela.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(self.tela_home)
    def mostrar_tela(self, tela):
        tela.tkraise() #para iniciar com a tela home

icone = Image.open(r"trabalho_lab_2\iconhome.png")
icone = icone.resize((15, 15))

class TelaHome(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #tk.Label(self, text="Planeamento de Refeições", font=("Segoe UI", 25,)).grid(row=0, column=0, columnspan=5, pady=(20, 60), padx=(80,0))
        ttk.Button(self, width=85, style='Accent.TButton', text="Planeamento das Refeições", command=lambda: master.mostrar_tela(master.tela_refeicoes)).grid(row=1, column=0, columnspan=5, sticky="n", pady=(0,40), padx=(20, 0))
        ttk.Button(self, width=40 ,style='Accent.TButton', text="Pesquisar Receitas", command=lambda: master.mostrar_tela(master.tela_ingredientes)).grid(row=2, column=0, columnspan=2, sticky="w", padx=(20,0), pady=(0,40)) # command=lambda: master.mostrar_tela(master.tela_ingredientes) para a funcao so executar quando clicarmos no botao e n qd este for criado
        ttk.Button(self, width=40 ,style='Accent.TButton', text="Receitas Favoritas", command=lambda: master.mostrar_tela(master.tela_receitas_favoritas)).grid(row=2, column=2, columnspan=2, sticky="e", padx=(20,0), pady=(0,40))
        ttk.Button(self, width=40 ,style='Accent.TButton', text="Lista de Compras  ", command=lambda: master.mostrar_tela(master.tela_lista)).grid(row=3, column=0, columnspan=2, sticky="w", padx=(20,0), pady=(0))
        ttk.Button(self, width=40 ,style='Accent.TButton', text="Descobrir Cozinhas", command=lambda: master.mostrar_tela(master.tela_cozinhas)).grid(row=3, column=2, columnspan=2, sticky="e", padx=(20, 0),  pady=0)
        imagem = Image.open(r"trabalho_lab_2\imagem.png")
        imagem = imagem.resize((550, 350))
        self.imagem_tk = ImageTk.PhotoImage(imagem)

        icongit = Image.open(r"trabalho_lab_2\github.png")
        icongit = icongit.resize((40, 40))
        self.icongit = ImageTk.PhotoImage(icongit)

        labelimg = tk.Label(self, image=self.imagem_tk).grid(row=0, column=0, sticky="n", columnspan=5, padx=(60,0))
        tk.Label(self, text="made by: Ricardo Guerra, Mariana Parente, Tiago Garcia, Guilherme Costa.", font=("Segoe UI", 8)).grid(row=5, column=3, columnspan=3,sticky="se", pady=(90,0))
        tk.Button(self, image=self.icongit, width=0, borderwidth=0, highlightthickness=0, cursor="hand2", bg="#FFFFFF", activebackground="#FFFFFF", command=abrir_github).grid(row=0, column=5, sticky="ne")

class TelaIngredientes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #  ttk.Button(self, text='Accent button', style='Accent.TButton').pack(pady=20)
    #label principal
        tk.Label(self, text="Planear Receitas/Dietas", font=("Segoe UI", 30, "bold")).grid(row=0, column=0, columnspan=5, pady=(100, 60), padx=(90,0))
    #ingredientes
        tk.Label(self, text="Ingredientes: ", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="e", padx=(50,0))
        ttk.Entry(self, width=30).grid(row=1, column=1, sticky="w")
    #dieta
        tk.Label(self, text="Dieta: ", font=("Segoe UI", 12, "bold")).grid(row=1, column=2, sticky="e", padx=(100, 0))
        #menu flutuante, guarda a opcao na variavel opcao_dieta
        opcao_dieta = tk.StringVar()
        combobox = ttk.Combobox(self, width=30, textvariable=opcao_dieta)
        combobox['values'] = ("Perder peso", "Manter peso", "Ganhar peso")
        combobox.grid(row=1, column=4, sticky="e")
    #alergias
        tk.Label(self, text="Alergias: ", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="e", pady=30)
        ttk.Entry(self, width=30).grid(row=2, column=1, sticky="w", pady=50)
    #botoes
        #funcoes dos botoes; lambda serve para chamar a funcao quando o botao for clicado
        ttk.Button(self, width=30 ,style='Accent.TButton', text="Pesquisar", command=lambda: master.mostrar_tela(master.tela_receitas)).grid(row=2, column=2, columnspan=3, sticky="e")#ao clicar no pesquisar ele puxa a tela receitas
        ttk.Button(self,width=70 ,style='Accent.TButton' ,text="Receitas Favoritas", command=lambda: master.mostrar_tela(master.tela_receitas_favoritas)).grid(row=3, column=0, columnspan=5, padx=(55,0), pady=(30))
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

class TelaReceitas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Receitas por Ingredientes", font=("Segoe UI", 30, "bold")).grid(row=0, column=0, columnspan=5, pady=(100, 60), padx=(180,0))
        ttk.Frame(self, style='Card').grid(row=1, column=0, columnspan=5)

        self.arquivo_favoritos = "favoritos.json"
        self.receitas = ["ola", "ola", "ola", "ola"] ##trocar dps
        self.receitas_favoritas = self.carregar_favoritos()

    def salvar_favoritos(self):
        with open(self.arquivo_favoritos, "w") as f:
            json.dump(self.receitas_favoritas, f)

    def carregar_favoritos(self):
        if os.path.exists(self.arquivo_favoritos):
            with open(self.arquivo_favoritos, "r") as f:
                return json.load(f)
        return []
        
    def marcar_favorito(self, receita):
        if receita not in self.receitas_favoritas:
            self.receitas_favoritas.append(receita)
            self.salvar_favoritos()
            tk.messagebox.showinfo(title="info", message="Receita salva com sucesso!")
        else:
            print(f"Receita '{receita}' já está nos favoritos")
        

        card_frame = ttk.Frame(self, width=100,style='Card').grid(row=1, column=3, columnspan=3, padx=20, pady=20, sticky="n")

        for i, receita in enumerate(self.receitas):
            label = ttk.Label(card_frame, text=receita, font=("Segoe UI", 16))
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            btn = ttk.Button(card_frame, text="❤", width=3, command=lambda r=receita: self.marcar_favorito(r))
            btn.grid(row=i, column=1, padx=5, pady=5)
        
"""
        tree = ttk.Treeview(self, columns=("item",), show="headings", height=5)
        tree.heading("item", text="Itens")

        # Lista de exemplo
        itens = ["Maçã", "Banana", "Laranja", "Uva"]

        # Inserir itens na treeview
        for item in itens:
            tree.insert("", tk.END, values=(item,))

        tree.grid(padx=10, pady=10)

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")
"""

class TelaRefeicoes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)


class TelaFavoritas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Receitas", font=("Arial", 25))
        tk.Label(self, text="Receitas:", font=("Arial", 10))

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

class TelaListaCompras(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

class TelaCozinhas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

app = App()
app.mainloop()