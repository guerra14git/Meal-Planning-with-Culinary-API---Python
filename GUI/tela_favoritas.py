import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
from API.spoonacular import buscar_receitas_favoritas_api, eliminar_receita_cloud_api
from GUI.icones import icone
from API import utils
import requests
import datetime

class TelaFavoritas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.receita_labels = []
        self.botoes_eliminar = []

        self.frame_borda = tk.Frame(self, background="#9ad9bb", padx=1, pady=1)
        self.frame_borda.grid(row=1, column=0, padx=(60, 0), pady=20, sticky="w", columnspan=5)

        tk.Label(self, text="Receitas Favoritas", font=("Segoe UI", 36, "bold"), fg="#696969").grid(
            row=0, column=0, columnspan=5, pady=(90, 10), padx=(85, 0)
        )

        self.atualizar_receitas_favoritas()

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2, image=self.icone_tk, compound="left",
                   command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

    def atualizar_receitas_favoritas(self):
        self.receitas_favoritas, self.receitas_ids = buscar_receitas_favoritas_api()
        for widget in self.frame_borda.winfo_children():
            widget.destroy()
        self.receita_labels.clear()
        self.botoes_eliminar.clear()
        self.label_receitas()

    def label_receitas(self):
        if not self.receitas_favoritas:
            label = tk.Label(self.frame_borda, text="Não tens receitas guardadas :/", font=("Segoe UI", 14, "italic"),
                             bg="white", width=70, anchor="center")
            label.grid(row=0, column=0, padx=5, pady=5)
            self.receita_labels.append(label)
            return

        for i, receita in enumerate(self.receitas_favoritas):
            label = tk.Label(self.frame_borda, text=receita, font=("Segoe UI", 14), anchor="w", bg="white", width=60)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            self.receita_labels.append(label)

            btn = tk.Button(self.frame_borda, text="❌", command=lambda indice=i: self.eliminar_receita_cloud(indice))
            btn.grid(row=i, column=1, sticky="e", padx=5)
            self.botoes_eliminar.append(btn)

    def eliminar_receita_cloud(self, indice):
        users = utils.ler_user_connect()
        username = utils.get_user_active()
        if not username or username not in users:
            messagebox.showinfo("Login", "Faz login primeiro")
            return
        hash = users[username].get("hash")
        if 0 <= indice < len(self.receitas_ids):
            item_id = self.receitas_ids[indice]
            api_key = utils.ler_api_key()
            sucesso, msg = eliminar_receita_cloud_api(username, hash, item_id, api_key)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.atualizar_receitas_favoritas()
            else:
                messagebox.showerror("Erro", msg)
        else:
            messagebox.showerror("Erro", "receita não encontrada na cloud")
