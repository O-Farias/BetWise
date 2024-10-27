import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

API_TOKEN = os.getenv("FOOTBALL_DATA_API_TOKEN")  # Token da Football-Data.org
BASE_URL = "https://api.football-data.org/v4"  # URL da API

# Função para buscar partidas de uma competição específica e temporada
def buscar_partidas(competicao_id, temporada):
    url = f"{BASE_URL}/competitions/{competicao_id}/matches"
    headers = {
        "X-Auth-Token": API_TOKEN
    }
    params = {
        "season": temporada
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")
        return None

# Função para listar ligas disponíveis
def listar_ligas():
    url = f"{BASE_URL}/competitions"
    headers = {
        "X-Auth-Token": API_TOKEN
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar ligas: {response.status_code} - {response.text}")
        return None
