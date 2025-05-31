#file pa funcoes q interagem com a api e assim

import requests
import time
import datetime
from tkinter import messagebox
from API import utils

api_key = utils.ler_api_key()

def guardar_receita_favorita_api(recipe_id, title):
    users = utils.ler_user_connect()
    username = utils.get_user_active()
    if not username or username not in users:
        messagebox.showinfo("Login", "Faz login primeiro!")
        return
    hash = users[username].get("hash")
    url = f"https://api.spoonacular.com/mealplanner/{username}/items"
    params = {
        "apiKey": api_key,
        "hash": hash
    }
    data = {
        "date": int(time.time()),
        "slot": 1,
        "position": 0,
        "type": "RECIPE",
        "value": {
            "id": recipe_id,
            "title": title,
            "imageType": "jpg"
        }
    }
    try:
        resp = requests.post(url, params=params, json=data)
        resp.raise_for_status()
        messagebox.showinfo("Sucesso", "Receita favorita guardada na cloud!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao guardar favorito: {e}")

def buscar_receitas_favoritas_api():
    users = utils.ler_user_connect()
    username = utils.get_user_active()
    if not username or username not in users:
        messagebox.showinfo("Login", "Faz login primeiro!")
        return [], []
    hash = users[username].get("hash")
    receitas = []
    ids = []
    dias = 7 
    for i in range(dias):
        data = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
        url = f"https://api.spoonacular.com/mealplanner/{username}/day/{data}"
        params = {
            "apiKey": api_key,
            "hash": hash
        }
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            dados = resp.json()
            items = dados.get("items", [])
            for item in items:
                value = item.get("value", {})
                if isinstance(value, str):
                    import json
                    value = json.loads(value)
                if item.get("type") == "RECIPE" and "title" in value:
                    if value["title"] not in receitas:  # evitar duplicados
                        receitas.append(value["title"])
                        ids.append(item["id"])
        except Exception:
            continue  # ignora dias sem favoritos
    return receitas, ids

def buscar_ingredientes_receita(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/ingredientWidget.json"
    params = {
        "apiKey": api_key
    }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        dados = resp.json()
        ingredientes = []
        for ingr in dados.get("ingredients", []):
            nome = ingr.get("name", "")
            quantidade = ingr.get("amount", {}).get("metric", {}).get("value", "")
            unidade = ingr.get("amount", {}).get("metric", {}).get("unit", "")
            ingredientes.append(f"{nome} ({quantidade} {unidade})")
        return ingredientes
    except requests.HTTPError as e:
        if resp.status_code == 404:
            print(f"Receita {recipe_id} não tem ingredientes públicos na Spoonacular.")
        else:
            print(f"Erro ao buscar ingredientes da receita {recipe_id}: {e}")
        return []

def buscar_id_receita(nome_receita, api_key):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": api_key,
        "query": nome_receita,
        "number": 1
    }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        dados = resp.json()
        if dados.get("results"):
            return dados["results"][0]["id"]
    except Exception as e:
        print(f"Erro ao buscar id da receita '{nome_receita}': {e}")
    return None

def pegar_ingredientes(receita_id, api_key):
    url = f"https://api.spoonacular.com/recipes/{receita_id}/information"
    params = {"apiKey": api_key}
    ingredientes = set()
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        dados = resp.json()
        for ingr in dados.get("extendedIngredients", []):
            ingredientes.add(ingr["name"])
    except Exception as e:
        print(f"Erro ao buscar ingredientes da receita {receita_id}: {e}")
    return ingredientes

def buscar_detalhes_receita(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": api_key}
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Erro ao buscar detalhes da receita {recipe_id}: {e}")
        return {}

def eliminar_receita_favorita_api(username, hash, item_id):
    url = f"https://api.spoonacular.com/mealplanner/{username}/items/{item_id}"
    params = {
        "apiKey": api_key,
        "hash": hash
    }
    try:
        resp = requests.delete(url, params=params)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"Erro ao eliminar receita favorita: {e}")
        return False

def gerar_plano_refeicoes(timeframe, calorias, dieta, excluir):
    url = "https://api.spoonacular.com/mealplanner/generate"
    params = {
        "apiKey": api_key,
        "timeFrame": timeframe,
        "targetCalories": calorias,
        "diet": dieta,
        "exclude": excluir
    }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Erro ao gerar plano de refeições: {e}")
        return {}
    
def classificar_cozinha_api(titulo, ingredientes, api_key):
    import requests
    url = "https://api.spoonacular.com/recipes/cuisine"
    params = {
        "apiKey": api_key
    }
    data = {
        "title": titulo,
        "ingredientList": ingredientes,
        "language": "en"
    }
    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("cuisine", "Desconhecida")
    except Exception as e:
        return f"Erro: {e}"
    
def eliminar_receita_cloud_api(username, hash, item_id, api_key):
    import requests
    url_del = f"https://api.spoonacular.com/mealplanner/{username}/items/{item_id}"
    params = {
        "apiKey": api_key,
        "hash": hash
    }
    try:
        resp_del = requests.delete(url_del, params=params)
        resp_del.raise_for_status()
        return True, "Receita eliminada da cloud!"
    except Exception as e:
        return False, f"Erro ao eliminar receita: {e}"

def buscar_receitas_por_ingredientes(api_key, ingredientes, dieta, cozinha, alergias, numero=10):
    import requests
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": api_key,
        "includeIngredients": ingredientes,
        "diet": dieta,
        "cuisine": cozinha,
        "intolerances": alergias,
        "number": numero
    }
    try:
        resposta = requests.get(url, params=params)
        resposta.raise_for_status()
        dados = resposta.json()
        receitas = []
        receitas_ids = []
        for r in dados.get("results", []):
            receitas.append(r['title'])
            receitas_ids.append(r['id'])
        return receitas, receitas_ids
    except Exception as e:
        return [], []

def gerar_refeicoes_api(api_key, tipo_plano, calorias, tipo_dieta, excluir):
    import requests
    url = "https://api.spoonacular.com/mealplanner/generate"
    parametros = {
        "apiKey": api_key,
        "timeFrame": tipo_plano,
        "targetCalories": calorias,
        "diet": tipo_dieta,
        "exclude": excluir
    }
    try:
        resposta = requests.get(url, params=parametros)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as e:
        return {"erro": str(e)}