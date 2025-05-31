import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
import requests
from GUI.icones import icone
from API import utils
from API.spoonacular import gerar_refeicoes_api

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
        ttk.Button(self, width=2, image=self.icone_tk, compound="left", command=lambda: master.mostrar_tela(master.tela_home)).grid(row=0, column=0, sticky="nw")

    def gerar_refeicoes(self):
        tela_anterior = self.master.tela_refeicoes
        tipo_plano = tela_anterior.tipo_plano.get()
        calorias = tela_anterior.calorias.get()
        tipo_dieta = tela_anterior.tipo_dieta.get()
        excluir = tela_anterior.tipo_comida.get()
        api_key = utils.ler_api_key()

        dados = gerar_refeicoes_api(api_key, tipo_plano, calorias, tipo_dieta, excluir)

        for label in self.resultados_labels:
            label.config(text="")

        if "erro" in dados or "meals" not in dados:
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
