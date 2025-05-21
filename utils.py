# utils.py - chatgpt functions
import tkinter as tk

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