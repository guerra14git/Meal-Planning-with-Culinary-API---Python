import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
import requests
from API.spoonacular import buscar_receitas_favoritas_api, buscar_id_receita, pegar_ingredientes
from GUI.icones import icone
from API import utils

api_key = utils.ler_api_key()

class TelaListaCompras(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.api_key = api_key
        self.ingredientes = set()

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2, image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")
        tk.Label(self, text="Atenção a utilizacao desta API gasta quase todos os creditos diarios(~30)*", font=("Segoe UI", 8), fg="#696969").grid(row=4, column=3, sticky="se", padx=(10, 0))

        tk.Label(self, text="Lista de Compras", font=("Segoe UI", 36, "bold"), fg="#696969").grid(row=0, column=0, columnspan=5, pady=(90, 10), padx=(190,0))

        botao = ttk.Button(self, text="Gerar Lista de Compras", width=50, command=self.gerar_lista_ingredientes)
        botao.grid(row=1, column=3, padx=(130,0), pady=10)

        self.listbox_ingredientes = tk.Listbox(self, width=70, height=20)
        self.listbox_ingredientes.grid(row=2, column=3, padx=(130,0), pady=10)

    def gerar_lista_ingredientes(self):
        self.ingredientes.clear()
        receitas, _ = buscar_receitas_favoritas_api()
        for receita in receitas:
            id_receita = buscar_id_receita(receita, self.api_key)
            if id_receita:
                self.ingredientes.update(pegar_ingredientes(id_receita, self.api_key))

        self.listbox_ingredientes.delete(0, tk.END)
        if not self.ingredientes:
            self.listbox_ingredientes.insert(tk.END, "Nenhum ingrediente encontrado.")
        else:
            for ingr in sorted(self.ingredientes):
                self.listbox_ingredientes.insert(tk.END, ingr)