import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from GUI.icones import icone

class TelaRefeicoes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Planeamento de Refeições", fg="#696969", font=("Segoe UI", 36, "bold")).grid(row=0, column=0, columnspan=5, sticky="n", pady=(100, 50), padx=(80,0))

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
        ttk.Button(self, width=2, image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")
