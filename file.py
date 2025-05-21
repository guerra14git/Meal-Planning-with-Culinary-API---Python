import tkinter as tk
#import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk #usar o pillow
import webbrowser   
import requests
import json
import os
import utils

def abrir_github():
    url = "https://github.com/guerra14git/Meal-Planning-with-Culinary-API---Python.git" #mudar o repo para o atualizado
    webbrowser.open(url)

def itens_por_virgulas(texto):
    return [item.strip() for item in texto.split(",") if item.strip()] #divide a string por ",", remove espacos em branco

def ler_ficheiro_txt(caminho_file):
    with open(caminho_file, 'r', encoding='utf-8') as file:
        items = file.readlines()
        items = [linha.strip() for linha in items if linha.strip()]
        return items

#class da janela principal
class App(tk.Tk): 
    def __init__(self): #construtor da classe 
        super().__init__() #inicializa a janela do tkinter dentro da classe App
        self.geometry("860x620")
        self.title("Planeamento de Refeições")
        self.iconbitmap(r"trabalho_lab_2\icon_circle.ico") #icon
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
        for tela in (self.tela_home, self.tela_ingredientes,self.tela_receitas, self.tela_receitas_favoritas, self.tela_lista, self.tela_cozinhas):
            tela.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(self.tela_home)

    def mostrar_tela(self, tela):
        if tela == self.tela_receitas_favoritas:
            tela.atualizar_receitas_favoritas()
        tela.tkraise()
"""
    def mostrar_tela(self, tela):
        if tela == self.tela_receitas_favoritas: #para atualizar as receitas favoritas sempre que mostramos a tela de guardar as receita, assim da para guardar receitas e ver logo sem fechar a app
            receitas_favoritas = ler_ficheiro_txt(r"trabalho_lab_2\favoritos.txt")
            texto_favoritas = "\n".join(receitas_favoritas) if receitas_favoritas else "Nenhuma receita favorita guardada"
            tela.label_receitas_favoritas.config(text=texto_favoritas)
        tela.tkraise() #para iniciar com a tela home
"""
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
        tk.Label(self, text="made by: Ricardo Guerra, Mariana Parente, Tiago Garcia, Guilherme Costa.", font=("Segoe UI", 8)).grid(row=4, column=3, columnspan=3,sticky="se", pady=(40,0))
        tk.Button(self, image=self.icongit, width=0, borderwidth=0, highlightthickness=0, cursor="hand2", bg="#FFFFFF", activebackground="#FFFFFF", command=abrir_github).grid(row=0, column=5, sticky="ne")

class TelaIngredientes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Planear Receitas/Dietas", fg="#696969",font=("Segoe UI", 36, "bold")).grid(row=0, column=0, columnspan=6, pady=(100, 30), padx=(90,0))
        
        tk.Label(self, text="Ingredientes(ex. tuna): ", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", padx=(10,0))
        self.ingredientes = ttk.Entry(self, width=85)
        self.ingredientes.grid(row=1, column=1, sticky="w", columnspan=4, pady=30)

        tk.Label(self, text="Receita(ex. pasta): ", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="e", padx=(10,0))
        self.tipo_receita = ttk.Entry(self, width=25)
        self.tipo_receita.grid(row=2, column=1, sticky="w")
        #ingredientes_separados = itens_por_virgulas(ingredientes)

        tk.Label(self, text="Dieta(ex. vegetarian): ", font=("Segoe UI", 12, "bold")).grid(row=2, column=2, sticky="e", padx=(50, 0))
        self.dieta = ttk.Entry(self, width=25)
        self.dieta.grid(row=2, column=4, sticky="w")

        tk.Label(self, text="Cozinha(ex. italian): ", font=("Segoe UI", 12, "bold")).grid(row=3, column=2,  sticky="e", padx=(50,0))
        self.cozinha = ttk.Entry(self, width=25)
        self.cozinha.grid(row=3, column=4, sticky="w")

        tk.Label(self, text="Alergias(ex. gluten): ", font=("Segoe UI", 12, "bold")).grid(row=3, column=0, sticky="e", pady=30, padx=(10,0))
        self.alergias = ttk.Entry(self, width=25)
        self.alergias.grid(row=3, column=1, sticky="w", pady=30)


        #funcoes dos botoes; lambda serve para chamar a funcao quando o botao for clicado
        ttk.Button(self, width=80 ,style='Accent.TButton', text="Pesquisar", command=lambda: [master.tela_receitas.pegar_valores(), master.mostrar_tela(master.tela_receitas)]).grid(row=4, column=0, columnspan=6, padx=(55,0), pady=(20))#ao clicar no pesquisar ele puxa a tela receitas
        ttk.Button(self,width=80 ,style='Accent.TButton' ,text="Receitas Favoritas", command=lambda: master.mostrar_tela(master.tela_receitas_favoritas)).grid(row=5, column=0, columnspan=6, padx=(55,0))
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

class TelaReceitas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.receitas = []
        self.frame_borda = tk.Frame(self, background="#9ad9bb", padx=1, pady=1)
        self.frame_borda.grid(row=1, column=0, padx=(60, 0), pady=20, sticky="w", columnspan=5)

        self.receita_labels = []
        self.botoes_favoritos = []

        for i in range(10):
            label = tk.Label(self.frame_borda, text="", font=("Segoe UI", 14), anchor="w", bg="white", width=60)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            self.receita_labels.append(label)

            botao = tk.Button(self.frame_borda, text="⭐", command=lambda indice=i: self.salvar_favorito_indice(indice))
            botao.grid(row=i, column=1, sticky="e", padx=5)
            self.botoes_favoritos.append(botao)

        tk.Label(self, text="Receitas por Ingredientes", fg="#696969",font=("Segoe UI", 36, "bold")).grid(row=0, column=0, columnspan=5, pady=(90, 20), padx=(45,0))

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

    def pegar_valores(self):
        ingredientes = self.master.tela_ingredientes.ingredientes.get()
        dieta = self.master.tela_ingredientes.dieta.get()
        cozinha = self.master.tela_ingredientes.cozinha.get()
        alergias = self.master.tela_ingredientes.alergias.get()

        url = "https://api.spoonacular.com/recipes/complexSearch"
        dicionario = {
            "apiKey": "0aac92641e5d488192ee8acb1498cc4d",
            "includeIngredients": ingredientes,
            "diet": dieta,
            "cuisine": cozinha,
            "intolerances": alergias,
            "number": 10
        }
        resposta = requests.get(url, params=dicionario)
        dados = resposta.json()

        self.receitas = [r['title'] for r in dados.get("results", [])]
        texto_receitas = "\n".join(self.receitas) if self.receitas else "Nenhuma receita encontrada."

        for label in self.receita_labels:
            label.config(text="")

        for i, receita in enumerate(self.receitas):
            if i < len(self.receita_labels):
                self.receita_labels[i].config(text=receita)

    def salvar_favorito_indice(self, indice):
        if 0 <= indice < len(self.receitas):
            receita = self.receitas[indice]
            with open(r"trabalho_lab_2\favoritos.txt", "a", encoding="utf-8") as f:
                f.write(receita + "\n")
            messagebox.showinfo("Sucesso", f"Receita '{receita}' salva com sucesso!")
class TelaRefeicoes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Refeições Obtidas").grid(row=0, column=0, columnspan=5, sticky="n")

class TelaFavoritas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.receita_labels = []
        self.botoes_eliminar = []

        self.receitas_favoritas = ler_ficheiro_txt(r"trabalho_lab_2\favoritos.txt") #vai buscar as receitas 

        self.frame_borda = tk.Frame(self, background="#9ad9bb", padx=1, pady=1)
        self.frame_borda.grid(row=1, column=0, padx=(60, 0), pady=20, sticky="w", columnspan=5)

        tk.Label(self, text="Receitas Favoritas", font=("Segoe UI", 36, "bold"), fg="#696969").grid(row=0, column=0, columnspan=5, pady=(90, 10), padx=(85,0))
        self.label_receitas()
       
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

    def atualizar_receitas_favoritas(self):
        self.receitas_favoritas = ler_ficheiro_txt(r"trabalho_lab_2\favoritos.txt")
        for widget in self.frame_borda.winfo_children():
            widget.destroy()    
        self.receita_labels.clear()
        self.botoes_eliminar.clear()
        self.label_receitas()

    def label_receitas(self):
        if not self.receitas_favoritas:
            label = tk.Label(self.frame_borda, text="Não tens receitas guardadas :/", font=("Segoe UI", 14, "italic"), bg="white", width=70, anchor="center")
            label.grid(row=0, column=0, padx=5, pady=5)
            self.receita_labels.append(label)
            return
        for i in range(len(self.receitas_favoritas)):
            receita = self.receitas_favoritas[i]
            label = tk.Label(self.frame_borda, text=receita, font=("Segoe UI", 14), anchor="w", bg="white", width=60)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=1)

            self.receita_labels.append(label) #para guardar os labels
            btn = tk.Button(self.frame_borda, text="❌", command=lambda indice=i: self.eliminar_receita(indice)) #command=lambda indice=i: self.eliminar_receita(indice) ==> fixa o valor do indice no i e guarda esse valor caso queiramos editar dps ou apagar
            btn.grid(row=i, column=1, sticky="e", padx=5)
            self.botoes_eliminar.append(btn)

    def eliminar_receita(self, indice):
        if indice >= 0 and indice < len(self.receitas_favoritas):
            del self.receitas_favoritas[indice]
            utils.write_ficheiro_txt(r"trabalho_lab_2\favoritos.txt", self.receitas_favoritas)
            self.atualizar_receitas_favoritas()


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