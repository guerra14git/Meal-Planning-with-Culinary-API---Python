import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
from GUI.icones import icone
from API.spoonacular import classificar_cozinha_api
from API import utils

class TelaCozinhas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2, image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

        tk.Label(self, text="Classificar Cozinha", font=("Segoe UI", 36, "bold"), fg="#696969").grid(row=0, column=1, padx=(10,0), columnspan=5, pady=(120, 30), sticky="w")

        tk.Label(self, text="Nome da Receita:", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="e", padx=25)
        self.nome_receita = ttk.Entry(self, width=25)
        self.nome_receita.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(self, text="Ingredientes (1 por linha):", font=("Segoe UI", 12, "bold")).grid(row=2, column=2, sticky="nw", pady=33)
        self.text_ingredientes = tk.Text(self, height=5, width=25)
        self.text_ingredientes.grid(row=2, column=4, sticky="w", pady=5)

        self.botao = ttk.Button(self, width=70, text="Classificar Cozinha", style='Accent.TButton', command=self.classificar_cozinha)
        self.botao.grid(row=4, column=0, pady=30, sticky="e", columnspan=5, padx=100)

        self.resultado = tk.Label(self, text="", font=("Segoe UI", 12, "italic"), fg="green")
        self.resultado.grid(row=5, column=0, columnspan=2, pady=10)

    def classificar_cozinha(self):
        api_key = utils.ler_api_key()
        titulo = self.nome_receita.get()
        ingredientes = self.text_ingredientes.get("1.0", "end").strip()

        if not titulo or not ingredientes:
            messagebox.showinfo("escreve o titulo e ingredientes")
            return

        resultado = classificar_cozinha_api(titulo, ingredientes, api_key)
        if resultado.startswith("Erro:"):
            self.resultado.config(text=resultado, fg="red")
        else:
            self.resultado.config(text=f"Cozinha: {resultado}", fg="green")
