import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from API.spoonacular import guardar_receita_favorita_api, buscar_receitas_por_ingredientes
import requests
from GUI.icones import icone
from API import utils

class TelaReceitas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.receitas = []
        self.receitas_ids = []
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
        api_key = utils.ler_api_key()

        self.receitas, self.receitas_ids = buscar_receitas_por_ingredientes(
            api_key, ingredientes, dieta, cozinha, alergias, numero=10
        )

        for label in self.receita_labels:
            label.config(text="")

        for i, receita in enumerate(self.receitas):
            if i < len(self.receita_labels):
                self.receita_labels[i].config(text=receita)

    def salvar_favorito_indice(self, indice):
        if 0 <= indice < len(self.receitas):
            receita = self.receitas[indice]
            recipe_id = self.receitas_ids[indice]
            guardar_receita_favorita_api(recipe_id, receita)
        else:
            messagebox.showerror("Erro", "Receita não encontrada.")
