import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from API import utils
from API.spoonacular import (
    guardar_receita_favorita_api,
    buscar_receitas_favoritas_api,
    buscar_ingredientes_receita
)

#Importa as telas
from GUI.tela_home import TelaHome
from GUI.tela_ingredientes import TelaIngredientes
from GUI.tela_receitas import TelaReceitas
from GUI.tela_favoritas import TelaFavoritas
from GUI.tela_lista_compras import TelaListaCompras
from GUI.tela_refeicoes import TelaRefeicoes
from GUI.tela_refeicoes_criar import TelaRefeicoesCriar
from GUI.tela_refeicoes_favoritas import TelaRefeicoesFavoritas
from GUI.tela_cozinhas import TelaCozinhas

from GUI.icones import icone 
api_key = utils.ler_api_key()

class App(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.geometry("860x620")
        self.title("Planeamento de Refeições")
        self.iconbitmap(r"trabalho_lab_2\icons\icon_circle.ico")
        self.tk.call('source', r'trabalho_lab_2\Forest-ttk-theme-master\forest-light.tcl')
        ttk.Style().theme_use('forest-light')
        self.tema_atual = "light"
        self.tela_home = TelaHome(self)
        self.tela_refeicoes = TelaRefeicoes(self)
        self.tela_refeicoes_criar = TelaRefeicoesCriar(self)
        self.tela_refeicoes_favoritas = TelaRefeicoesFavoritas(self)
        self.tela_ingredientes = TelaIngredientes(self)
        self.tela_receitas = TelaReceitas(self)
        self.tela_receitas_favoritas = TelaFavoritas(self)
        self.tela_lista = TelaListaCompras(self)
        self.tela_cozinhas = TelaCozinhas(self)

        #qqr tela criada tem q ser adicionada aqui
        for tela in (self.tela_home, self.tela_ingredientes, self.tela_receitas, self.tela_receitas_favoritas, self.tela_lista, self.tela_cozinhas, self.tela_refeicoes, self.tela_refeicoes_criar, self.tela_refeicoes_favoritas):
            tela.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela(self.tela_home)

    def mostrar_tela(self, tela):
        if tela == self.tela_receitas_favoritas:
            tela.atualizar_receitas_favoritas()
        tela.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()