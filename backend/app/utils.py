import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

# Função para buscar dados dos jogos de uma liga específica e temporada
def buscar_jogos(liga_id, temporada):
    url = f"{BASE_URL}/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "league": liga_id,
        "season": temporada
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None


# Função para listar todas as ligas disponíveis
def listar_ligas():
    url = f"{BASE_URL}/leagues"
    headers = {
        "x-apisports-key": API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar ligas: {response.status_code}")
        return None