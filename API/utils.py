#file para importar funcoes globais do codigo main

import tkinter as tk
from tkinter import simpledialog, messagebox
import webbrowser
import json
import os
import requests


def add_placeholder(entry_widget, placeholder_text):
    def on_focus_in(event):
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, tk.END)
            entry_widget.configure(foreground='black')

    def on_focus_out(event):
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder_text)
            entry_widget.configure(foreground='grey')

    entry_widget.insert(0, placeholder_text)
    entry_widget.configure(foreground='grey')
    entry_widget.bind("<FocusIn>", on_focus_in)
    entry_widget.bind("<FocusOut>", on_focus_out)

def write_ficheiro_txt(caminho, linhas):
    with open(caminho, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha.strip() + "\n")

def abrir_github():
    url = "https://github.com/guerra14git/Meal-Planning-with-Culinary-API---Python.git" 
    webbrowser.open(url)

def itens_por_virgulas(texto):
    return [item.strip() for item in texto.split(",") if item.strip()]

def ler_ficheiro_txt(caminho_file):
    with open(caminho_file, 'r', encoding='utf-8') as file:
        items = file.readlines()
        items = [linha.strip() for linha in items if linha.strip()]
        return items

def ler_blocos_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    blocos = [bloco.strip() for bloco in conteudo.split("===") if bloco.strip()]
    return blocos

'''
def ler_api_key():
    with open(r"trabalho_lab_2\files\api.txt", 'r', encoding='utf-8') as file:
        for linha in file:
            key = linha.strip()
            if key:
                return key
    return None
'''
def ler_api_key():
    try:
        with open(r"trabalho_lab_2\FILES\api.txt", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""

api_key = ler_api_key()

USER_CONNECT_PATH = r"trabalho_lab_2\FILES\user_connect.json"
USER_ACTIVE_PATH = r"trabalho_lab_2\FILES\user_active.txt"

def guardar_user_connect(novo_user):
    users = ler_user_connect()
    if not isinstance(users, dict):
        users = {}
    username = novo_user.get("username")
    if username:
        users[username] = novo_user
        with open(USER_CONNECT_PATH, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

def ler_user_connect():
    try:
        with open(USER_CONNECT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def conectar_spoonacular():
    username = simpledialog.askstring("Username", "Insere o teu username:")
    first_name = simpledialog.askstring("Primeiro Nome", "Insere o teu primeiro nome:")
    last_name = simpledialog.askstring("Último Nome", "Insere o teu último nome:")
    email = simpledialog.askstring("Email", "Insere o teu email:")

    if not all([username, first_name, last_name, email]):
        messagebox.showinfo("Erro", "Todos os campos são obrigatórios.")
        return

    url = "https://api.spoonacular.com/users/connect"
    params = {"apiKey": api_key}
    data = {
        "username": username,
        "firstName": first_name,
        "lastName": last_name,
        "email": email
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        guardar_user_connect(result)
        set_user_active(result.get("username"))
        messagebox.showinfo("Sucesso", f"Utilizador conectado!\nUsername: {result.get('username')}\nHash: {result.get('hash')}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar: {e}")

def set_user_active(username):
    with open(USER_ACTIVE_PATH, "w", encoding="utf-8") as f:
        f.write(username)

def get_user_active():
    if not os.path.exists(USER_ACTIVE_PATH):
        return None
    with open(USER_ACTIVE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

def escolher_user_connect():
    users = ler_user_connect()
    if not users:
        messagebox.showinfo("Info", "Nenhum utilizador disponível.")
        return
    usernames = list(users.keys())
    username = simpledialog.askstring("Login", f"Escolhe o username:\n{', '.join(usernames)}")
    if username in users:
        set_user_active(username)
        messagebox.showinfo("Login", f"Agora estás logado como: {username}")
    else:
        messagebox.showerror("Erro", "Username inválido.")