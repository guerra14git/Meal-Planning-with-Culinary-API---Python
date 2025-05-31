import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
from API import utils
from GUI.icones import icone

class TelaRefeicoesFavoritas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Refeições Favoritas", font=("Segoe UI", 36, "bold")).grid(row=0, column=0, columnspan=6, pady=(20, 30), padx=(90, 0))

        self.frame_borda = tk.Frame(self, background="#9ad9bb", padx=1, pady=1)
        self.frame_borda.grid(row=1, column=0, columnspan=6, pady=(0, 30), padx=(20, 0), sticky="w")

        self.refeicao_labels = []
        self.botoes_eliminar = []

        self.icone_tk = ImageTk.PhotoImage(icone)
        ttk.Button(self, width=2, image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

        self.atualizar_refeicoes_favoritas()

    def atualizar_refeicoes_favoritas(self):
        self.refeicoes_favoritas = utils.ler_blocos_txt(r"trabalho_lab_2\files\refeicoes_favoritos.txt")
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
