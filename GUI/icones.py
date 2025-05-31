#so para n ter d importar a imagem sempre que a tela for raised

from PIL import Image

icone = Image.open(r"trabalho_lab_2\icons\iconhome.png")
icone = icone.resize((15, 15))