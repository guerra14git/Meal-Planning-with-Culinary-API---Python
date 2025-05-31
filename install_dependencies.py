import subprocess
import sys

pacotes = ["requests", "pillow"]

for pacote in pacotes:
    subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

print("Dependências instaladas com sucesso!")
input("Pressiona Enter para fechar...")