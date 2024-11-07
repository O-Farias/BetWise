import requests
import os
import random
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

API_TOKEN = os.getenv("SPORTMONKS_API_TOKEN")  # Token da SportMonks
BASE_URL = "https://api.sportmonks.com/v3/football/fixtures"  # URL da API SportMonks

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Função para buscar partidas (fixtures) de uma competição específica e temporada, com suporte para datas opcionais
def buscar_partidas(season_id, date_from=None, date_to=None, proxima=False):
    params = {"season_id": season_id}

    # Adiciona os parâmetros opcionais de data, se fornecidos
    if date_from:
        params["date"] = date_from
    if date_to:
        params["to"] = date_to

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        partidas = response.json().get("data", [])
        
        # Filtra a próxima partida, se solicitado
        if proxima:
            partidas_futuras = [partida for partida in partidas if partida["status"] == "NS"]  # Status "NS" indica não iniciado
            return partidas_futuras[0] if partidas_futuras else None
        return partidas
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")
        return None

# Função para listar ligas disponíveis (adaptar se necessário para a SportMonks)
def listar_ligas():
    url = f"https://api.sportmonks.com/v3/football/leagues"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Erro ao buscar ligas: {response.status_code} - {response.text}")
        return None

# Função para buscar uma partida específica (fixtures) usando IDs específicos
def buscar_partida_especifica(fixture_id):
    url = f"{BASE_URL}/{fixture_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("data", {})
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return None

# Função para garantir que os valores de gols não sejam None
def get_gols(valor):
    return valor if valor is not None else 0

# Função para analisar H2H (histórico de confrontos diretos)
def analisar_h2h(jogos):
    total_jogos = len(jogos)
    gols_casa = sum(get_gols(jogo["scores"]["localteam_score"]) for jogo in jogos)
    gols_fora = sum(get_gols(jogo["scores"]["visitorteam_score"]) for jogo in jogos)
    media_gols = (gols_casa + gols_fora) / total_jogos if total_jogos > 0 else 0
    ambos_marcam = sum(
        1 for jogo in jogos
        if get_gols(jogo["scores"]["localteam_score"]) > 0 and get_gols(jogo["scores"]["visitorteam_score"]) > 0
    )
    return {
        "media_gols": media_gols,
        "ambos_marcam_percentual": ambos_marcam / total_jogos if total_jogos > 0 else 0
    }

# Função para calcular a probabilidade de BTTS (Both Teams to Score)
def calcular_btts(jogos):
    btts = sum(1 for jogo in jogos if get_gols(jogo["scores"]["localteam_score"]) > 0 and get_gols(jogo["scores"]["visitorteam_score"]) > 0)
    return btts / len(jogos) if jogos else 0

# Função para simular um jogo usando uma média de gols
def simular_jogo(media_gols_casa, media_gols_fora):
    gols_casa = random.randint(0, int(media_gols_casa + 1))  # Simples alternativa ao Poisson
    gols_fora = random.randint(0, int(media_gols_fora + 1))
    return {"gols_casa": gols_casa, "gols_fora": gols_fora}
