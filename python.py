import requests ##biblioteca para fazer pedidos HTTP(buscar API)
import tkinter as tk
from tkinter import messagebox

def buscar_receitas(ingredientes):
    url = "https://api.spoonacular.com/recipes/findByIngredients" ##escolhemos a API de procurar receitas por ingredientes
    dicionario = {
        "apiKey": "0aac92641e5d488192ee8acb1498cc4d", ##a api key
        "ingredients": ingredientes,
        "number": 6  ##numero de receitas
    }
    
    resposta = requests.get(url, params=dicionario) ##enviar a request GET para a API
    dados = resposta.json() ##transformar a resposta da api para um dicionario
    receitas = []##armanezar as receitas

    for receita in dados:
        ##acessamos o titulo da receita e adicionamos a receitas
        titulo = receita['title']
        receitas.append(titulo)##.append para adicionar no final da lista

    return receitas##devolver as receitas obtidas

def main():
    ingredientes = input("Digita os ingredientes(separados por virgulas): ")

    receitas_obtidas = buscar_receitas(ingredientes)

def main():
    def buscar():
        ingredientes = entrada.get()##buscar oq o user escrever
        receitas_obtidas = buscar_receitas(ingredientes)##puxa a funcao acima
        for receita in receitas_obtidas:
            resultado.insert(tk.END, receita)##mete as receitas na lista & tk.END para por no final da lista

    janela = tk.Tk() ##abre a janela
    janela.title("Pesquizar Receitas")
    janela.configure(bg="lightblue")##bg = backgroundcolor e fg e foregroundcolor
    
    titulo = tk.Label(janela, text="Pesquizar Receitas", font=("Arial", 14), bg="lightblue")
    titulo.pack(pady=10)

    instrucoes = tk.Label(janela, text="Ingredientes(separados por virgula):", bg="lightblue")
    instrucoes.pack(pady=5)

    frame = tk.Frame(janela, bg="lightblue")
    frame.pack(pady=5)

    entrada = tk.Entry(frame, width=30, font=("Arial", 12))
    entrada.pack(pady=5, padx=5, side="left")

    botao = tk.Button(frame, text="pesquisar", command=buscar, font=("Arial", 10))
    botao.pack(pady=10, side="right")

    resultado = tk.Listbox(janela)
    resultado.pack(pady=10)

    janela.mainloop()

if __name__ == "__main__":
    main()