import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from GUI.icones import icone

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
