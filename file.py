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

def ler_blocos_txt(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
        blocos = [bloco.strip() for bloco in conteudo.split("===") if bloco.strip()]
        return blocos

#class da janela principal
class App(tk.Tk): 
    def __init__(self): #construtor da classe 
        super().__init__() #inicializa a janela do tkinter dentro da classe App
        self.geometry("860x620")
        self.title("Planeamento de Refeições")
        self.iconbitmap(r"trabalho_lab_2\icons\icon_circle.ico") #icon
#temas tkinter: https://github.com/rdbende/Forest-ttk-theme.git
        self.tk.call('source', r'trabalho_lab_2\Forest-ttk-theme-master\forest-light.tcl')
        ttk.Style().theme_use('forest-light')
        self.tema_atual = "light" ##usar ttk para theme e tk para tkinter original theme
#telas ou frames
        self.tela_home = TelaHome(self)
        self.tela_refeicoes = TelaRefeicoes(self)
        self.tela_refeicoes_criar = TelaRefeicoesCriar(self)
        self.tela_refeicoes_favoritas = TelaRefeicoesFavoritas(self)
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
        for tela in (self.tela_home, self.tela_ingredientes,self.tela_receitas, self.tela_receitas_favoritas, self.tela_lista, self.tela_cozinhas, self.tela_refeicoes, self.tela_refeicoes_criar, self.tela_refeicoes_favoritas):
            tela.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(self.tela_home)

    def mostrar_tela(self, tela):
        if tela == self.tela_receitas_favoritas:
            tela.atualizar_receitas_favoritas()
        tela.tkraise()

icone = Image.open(r"trabalho_lab_2\icons\iconhome.png")
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
        imagem = Image.open(r"trabalho_lab_2\icons\imagem.png")
        imagem = imagem.resize((550, 350))
        self.imagem_tk = ImageTk.PhotoImage(imagem)

        icongit = Image.open(r"trabalho_lab_2\icons\github.png")
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
            with open(r"trabalho_lab_2\files\favoritos.txt", "a", encoding="utf-8") as f:
                f.write(receita + "\n")
            messagebox.showinfo("Sucesso", f"Receita '{receita}' salva com sucesso!")

class TelaRefeicoes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Planeamento de Refeições", fg="#696969",font=("Segoe UI", 36, "bold")).grid(row=0, column=0, columnspan=5, sticky="n", pady=(100, 50), padx=(80,0))

        tk.Label(self, text="Tipo de plano(day/week):", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="E", padx=(20,0))
        self.tipo_plano = ttk.Entry(self, width=25)
        self.tipo_plano.grid(row=1, column=1, sticky="w")
        
        tk.Label(self, text="Total de calorias: ", font=("Segoe UI", 12, "bold")).grid(row=1, column=3, sticky="e", padx=(30, 0), pady=40)
        self.calorias = ttk.Entry(self, width=25)
        self.calorias.grid(row=1, column=4, sticky="w")

        tk.Label(self, text="Tipo Dieta(ex. vegan):", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="e", padx=(20,0))
        self.tipo_dieta = ttk.Entry(self, width=25)
        self.tipo_dieta.grid(row=2, column=1, sticky="w")

        tk.Label(self, text="A excluir(ex. olives):", font=("Segoe UI", 12, "bold")).grid(row=2, column=3, sticky="e", padx=(30, 0))
        self.tipo_comida = ttk.Entry(self, width=25)
        self.tipo_comida.grid(row=2, column=4, sticky="w")

        ttk.Button(self, width=80 ,style='Accent.TButton', text="Criar Plano de Refeições", command=lambda: [master.tela_refeicoes_criar.gerar_refeicoes(), master.mostrar_tela(master.tela_refeicoes_criar)]).grid(row=3, column=0, columnspan=6, padx=(55,0), pady=(50, 20))
        ttk.Button(self, width=80 ,style='Accent.TButton', text="Ver Planos Guardados", command=lambda: master.mostrar_tela(master.tela_refeicoes_favoritas)).grid(row=4, column=0, columnspan=6, padx=(55,0))

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

class TelaRefeicoesCriar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Refeição Obtida", fg="#696969", font=("Segoe UI", 36, "bold")).grid(row=0, column=0, columnspan=5, sticky="n", pady=(60, 50), padx=(20,0))

        self.resultados_labels = []
        self.botoes_favoritos = []
        self.refeicoes = []

        self.frame_resultados = tk.Frame(self)
        self.frame_resultados.grid(row=1, column=0, columnspan=5)

        for i in range(5):
            label = tk.Label(self.frame_resultados, text="", font=("Segoe UI", 14), anchor="w", wraplength=800)
            label.grid(row=i, column=0, sticky="w", padx=40, pady=5)
            self.resultados_labels.append(label)

        botao = ttk.Button(self.frame_resultados, width=95, text="⭐ Guardar Refeicao", command=self.salvar_favorito_refeicao)
        botao.grid(row=6, column=0, sticky="w", padx=(90,0), columnspan=5)
        self.botoes_favoritos.append(botao)

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

    def gerar_refeicoes(self):
        tela_anterior = self.master.tela_refeicoes
        tipo_plano = tela_anterior.tipo_plano.get()
        calorias = tela_anterior.calorias.get()
        tipo_dieta = tela_anterior.tipo_dieta.get()
        excluir = tela_anterior.tipo_comida.get()

        url = "https://api.spoonacular.com/mealplanner/generate"
        parametros = {
            "apiKey": "0aac92641e5d488192ee8acb1498cc4d",
            "timeFrame": tipo_plano,
            "targetCalories": calorias,
            "diet": tipo_dieta,
            "exclude": excluir
        }

        resposta = requests.get(url, params=parametros)
        dados = resposta.json()
    
        for label in self.resultados_labels:
            label.config(text="")

        if "meals" not in dados:
            self.resultados_labels[0].config(text="sem resultados")
            return

        for i, refeicao in enumerate(dados["meals"]):
            texto = f"{refeicao['title']} - {refeicao['readyInMinutes']} min | {refeicao['servings']} porções"
            self.resultados_labels[i].config(text=texto)

        nutrientes = dados.get("nutrients", {})
        if nutrientes:
            info_nutri = (
                f"Nutrição Total: {nutrientes.get('calories', 0)} kcal | "
                f"Proteína: {nutrientes.get('protein', 0)}g | "
                f"Gordura: {nutrientes.get('fat', 0)}g | "
                f"Hidratos de carbono: {nutrientes.get('carbohydrates', 0)}g"
            )
            self.resultados_labels[len(dados['meals'])].config(text=info_nutri)

    def salvar_favorito_refeicao(self):
        refeicoes = [label.cget("text") for label in self.resultados_labels if label.cget("text")]
        if not refeicoes:
            messagebox.showinfo("Aviso", "Nenhuma refeição para guardar.")
            return

        bloco = "\n".join(refeicoes) + "\n===\n"  
        with open(r"trabalho_lab_2\files\refeicoes_favoritos.txt", "a", encoding="utf-8") as f:
            f.write(bloco)

        if hasattr(self.master, "tela_refeicoes_favoritas"):
            self.master.tela_refeicoes_favoritas.atualizar_refeicoes_favoritas()

        messagebox.showinfo("Sucesso", "Refeição guardada com sucesso!")

class TelaRefeicoesFavoritas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.refeicao_labels = []
        self.botoes_eliminar = []

        self.refeicoes_favoritas = ler_ficheiro_txt(r"trabalho_lab_2\files\refeicoes_favoritos.txt")

        self.frame_borda = tk.Frame(self, background="#9ad9bb", padx=1, pady=1)
        self.frame_borda.grid(row=1, column=0, padx=(15, 0), pady=20, sticky="w", columnspan=5)

        tk.Label(self, text="Refeições Favoritas", font=("Segoe UI", 36, "bold"), fg="#696969").grid(row=0, column=0, columnspan=5, pady=(90, 10), padx=(85, 0))
        
        self.label_refeicoes()

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2, image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")


    def atualizar_refeicoes_favoritas(self):
        self.refeicoes_favoritas = ler_blocos_txt(r"trabalho_lab_2\files\refeicoes_favoritos.txt")
        for widget in self.frame_borda.winfo_children():
            widget.destroy()
        self.refeicao_labels.clear()
        self.botoes_eliminar.clear()
        self.label_refeicoes()


    def label_refeicoes(self):
        if not self.refeicoes_favoritas:
            label = tk.Label(self.frame_borda, text="Não tens refeições guardadas :(", font=("Segoe UI", 14, "italic"), bg="white", width=70, anchor="center")
            label.grid(row=0, column=0, padx=5, pady=5)
            self.refeicao_labels.append(label)
            return

        for i, bloco in enumerate(self.refeicoes_favoritas):
            label = tk.Label(self.frame_borda, text=bloco, font=("Segoe UI", 14), anchor="w", justify="left", bg="white", width=71)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            self.refeicao_labels.append(label)

            btn = tk.Button(self.frame_borda, text="❌", command=lambda indice=i: self.eliminar_refeicao(indice))
            btn.grid(row=i, column=1, sticky="e", padx=5)
            self.botoes_eliminar.append(btn)


    def eliminar_refeicao(self, indice):
        if 0 <= indice < len(self.refeicoes_favoritas):
            del self.refeicoes_favoritas[indice]
            with open(r"trabalho_lab_2\files\refeicoes_favoritos.txt", "w", encoding="utf-8") as f:
                for bloco in self.refeicoes_favoritas:
                    f.write(bloco + "\n===\n")
            self.atualizar_refeicoes_favoritas()

class TelaFavoritas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.receita_labels = []
        self.botoes_eliminar = []

        self.receitas_favoritas = ler_ficheiro_txt(r"trabalho_lab_2\files\favoritos.txt")

        self.frame_borda = tk.Frame(self, background="#9ad9bb", padx=1, pady=1)
        self.frame_borda.grid(row=1, column=0, padx=(60, 0), pady=20, sticky="w", columnspan=5)

        tk.Label(self, text="Receitas Favoritas", font=("Segoe UI", 36, "bold"), fg="#696969").grid(row=0, column=0, columnspan=5, pady=(90, 10), padx=(85,0))
        self.label_receitas()
       
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

    def atualizar_receitas_favoritas(self):
        self.receitas_favoritas = ler_ficheiro_txt(r"trabalho_lab_2\files\favoritos.txt")
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
            utils.write_ficheiro_txt(r"trabalho_lab_2\files\favoritos.txt", self.receitas_favoritas)
            self.atualizar_receitas_favoritas()

class TelaListaCompras(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.api_key = "0aac92641e5d488192ee8acb1498cc4d"
        self.ingredientes = set()

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

        tk.Label(self, text="Lista de Compras", font=("Segoe UI", 36, "bold"), fg="#696969").grid(row=0, column=0, columnspan=5, pady=(90, 10), padx=(190,0))

        botao = ttk.Button(self, text="Gerar Lista de Compras", width=50,command=self.gerar_lista_ingredientes)
        botao.grid(row=1, column=3, padx=(130,0), pady=10)

        self.listbox_ingredientes = tk.Listbox(self, width=70, height=20)
        self.listbox_ingredientes.grid(row=2, column=3, padx=(130,0), pady=10)

    def gerar_lista_ingredientes(self):
        self.ingredientes.clear()
        receitas_favoritas = self.ler_ficheiro_txt(r"trabalho_lab_2\files\favoritos.txt")

        for receita in receitas_favoritas:
            id_receita = self.buscar_id_receita(receita)
            if id_receita:
                self.pegar_ingredientes(id_receita)

        self.listbox_ingredientes.delete(0, tk.END)
        if not self.ingredientes:
            self.listbox_ingredientes.insert(tk.END, "Nenhum ingrediente encontrado.")
        else:
            for ingr in sorted(self.ingredientes):
                self.listbox_ingredientes.insert(tk.END, ingr)

    def ler_ficheiro_txt(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                linhas = [linha.strip() for linha in f if linha.strip()]
            return linhas
        except Exception as e:
            print(f"Erro ao ler o ficheiro: {e}")
            return []

    def buscar_id_receita(self, nome_receita):
        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": self.api_key,
            "query": nome_receita,
            "number": 1
        }
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            dados = resp.json()
            if dados.get("results"):
                return dados["results"][0]["id"]
        except Exception as e:
            print(f"Erro ao buscar id da receita '{nome_receita}': {e}")
        return None

    def pegar_ingredientes(self, receita_id):
        url = f"https://api.spoonacular.com/recipes/{receita_id}/information"
        params = {"apiKey": self.api_key}
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            dados = resp.json()
            for ingr in dados.get("extendedIngredients", []):
                self.ingredientes.add(ingr["name"])
        except Exception as e:
            print(f"Erro ao buscar ingredientes da receita {receita_id}: {e}")

class TelaCozinhas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2,image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

        tk.Label(self, text="Classificar Cozinha", font=("Segoe UI", 36, "bold"), fg="#696969").grid(row=1, column=0, columnspan=5, pady=20, sticky="n")

        tk.Label(self, text="Nome da Receita:", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="e", padx=10)
        self.nome_receita = ttk.Entry(self, width=40)
        self.nome_receita.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(self, text="Ingredientes (1 por linha):", font=("Segoe UI", 12, "bold")).grid(row=3, column=0, sticky="ne", padx=10)
        self.text_ingredientes = tk.Text(self, height=10, width=40)
        self.text_ingredientes.grid(row=3, column=1, sticky="w", pady=5)

        self.botao = ttk.Button(self, text="Classificar Cozinha", command=self.classificar_cozinha)
        self.botao.grid(row=4, column=1, pady=10, sticky="e")

        self.resultado = tk.Label(self, text="", font=("Segoe UI", 12, "italic"), fg="green")
        self.resultado.grid(row=5, column=0, columnspan=2, pady=10)

    def classificar_cozinha(self):
        titulo = self.entry_titulo.get()
        ingredientes = self.text_ingredientes.get("1.0", "end").strip()

        if not titulo or not ingredientes:
            messagebox.showinfo("Preenche o titulo e ingredientes")
            return

        url = "https://api.spoonacular.com/recipes/cuisine"
        data = {
            "apiKey": "0aac92641e5d488192ee8acb1498cc4d",
            "title": titulo,
            "ingredientList": ingredientes,
            "language": "en"
        }

        response = requests.post(url, data=data)
        result = response.json()

        cuisine = result.get("cuisine", "Desconhecida")
        confidence = result.get("confidence", 0)
        texto_resultado = f"Cozinha: {cuisine} (confiança: {confidence:.2f})"

app = App()
app.mainloop()