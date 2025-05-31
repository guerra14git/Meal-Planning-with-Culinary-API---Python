import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from API import utils

class TelaHome(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        ttk.Button(self, width=85, style='Accent.TButton', text="Planeamento das Refeições", command=lambda: master.mostrar_tela(master.tela_refeicoes)).grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0,40), padx=(60,60))
        ttk.Button(self, width=40, style='Accent.TButton', text="Pesquisar Receitas", command=lambda: master.mostrar_tela(master.tela_ingredientes)).grid(row=2, column=1, sticky="w", padx=(52,10), pady=(0,40))
        ttk.Button(self, width=40, style='Accent.TButton', text="Receitas Favoritas", command=lambda: master.mostrar_tela(master.tela_receitas_favoritas)).grid(row=2, column=3, sticky="ew", padx=(95,10), pady=(0,40))

        ttk.Button(self, width=40, style='Accent.TButton', text="Lista de Compras", command=lambda: master.mostrar_tela(master.tela_lista)).grid(row=3, column=1, sticky="w", padx=(52,10), pady=(0,0))
        ttk.Button(self, width=40, style='Accent.TButton', text="Descobrir Cozinhas", command=lambda: master.mostrar_tela(master.tela_cozinhas)).grid(row=3, column=3, sticky="ew", padx=(95,10), pady=(0,0))

        imagem = Image.open(r"trabalho_lab_2\icons\imagem.png")
        imagem = imagem.resize((600, 350))
        self.imagem_tk = ImageTk.PhotoImage(imagem)

        icongit = Image.open(r"trabalho_lab_2\icons\github.png")
        icongit = icongit.resize((40, 40))
        self.icongit = ImageTk.PhotoImage(icongit)

        tk.Label(self, image=self.imagem_tk).grid(row=0, column=0, sticky="n", columnspan=5, padx=(60,0), pady=(25, 0))
        tk.Label(self, text="made by: Ricardo Guerra, Mariana Parente, Tiago Garcia, Guilherme Costa.", font=("Segoe UI", 8)).grid(row=4, column=3, columnspan=3,sticky="se", pady=(20,0))
        tk.Button(self, image=self.icongit, width=0, borderwidth=0, highlightthickness=0, cursor="hand2", bg="#FFFFFF", activebackground="#FFFFFF", command=utils.abrir_github).grid(row=0, column=4, sticky="nw")

        ttk.Button(self, width=7, text="Registar", command=utils.conectar_spoonacular).grid(row=0, column=0, columnspan=2,pady=(5,0), padx=(5),sticky="nw")
        ttk.Button(self, width=8, text="Login", command=utils.escolher_user_connect).grid(row=0, column=1, columnspan=2,pady=(5,0), sticky="nw", padx=75)