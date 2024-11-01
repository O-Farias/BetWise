import requests
import os
import random
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

API_TOKEN = os.getenv("FOOTBALL_DATA_API_TOKEN")  # Token da Football-Data.org
BASE_URL = "https://api.football-data.org/v4"  # URL da API

# Função para buscar partidas de uma competição específica e temporada, com suporte para datas opcionais
def buscar_partidas(competicao_id, temporada, date_from=None, date_to=None, proxima=False):
    url = f"{BASE_URL}/competitions/{competicao_id}/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": temporada}

    # Adiciona os parâmetros opcionais de data, se fornecidos
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        partidas = response.json().get("matches", [])
        
        # Filtra a próxima partida, se solicitado
        if proxima:
            partidas_futuras = [partida for partida in partidas if partida["status"] == "TIMED"]
            return partidas_futuras[0] if partidas_futuras else None
        return partidas
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")
        return None


# Função para listar ligas disponíveis
def listar_ligas():
    url = f"{BASE_URL}/competitions"
    headers = {"X-Auth-Token": API_TOKEN}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar ligas: {response.status_code} - {response.text}")
        return None

# Função para buscar uma partida específica
def buscar_partida_especifica(competicao_id, temporada, time_1, time_2, data_jogo):
    url = f"{BASE_URL}/competitions/{competicao_id}/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": temporada, "dateFrom": data_jogo, "dateTo": data_jogo}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        jogos = response.json().get("matches", [])
        for jogo in jogos:
            if (time_1.lower() in jogo["homeTeam"]["name"].lower() and
                time_2.lower() in jogo["awayTeam"]["name"].lower()):
                return jogo
        return None
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return None


# Função para garantir que os valores de gols não sejam None
def get_gols(valor):
    return valor if valor is not None else 0

# Função para analisar H2H (histórico de confrontos diretos)
def analisar_h2h(jogos):
    total_jogos = len(jogos)
    gols_casa = sum(get_gols(jogo["score"]["fullTime"]["home"]) for jogo in jogos)
    gols_fora = sum(get_gols(jogo["score"]["fullTime"]["away"]) for jogo in jogos)
    media_gols = (gols_casa + gols_fora) / total_jogos if total_jogos > 0 else 0
    ambos_marcam = sum(
        1 for jogo in jogos
        if get_gols(jogo["score"]["fullTime"]["home"]) > 0 and get_gols(jogo["score"]["fullTime"]["away"]) > 0
    )
    return {
        "media_gols": media_gols,
        "ambos_marcam_percentual": ambos_marcam / total_jogos if total_jogos > 0 else 0
    }

# Função para calcular a probabilidade de BTTS (Both Teams to Score)
def calcular_btts(jogos):
    btts = sum(1 for jogo in jogos if get_gols(jogo["score"]["fullTime"]["home"]) > 0 and get_gols(jogo["score"]["fullTime"]["away"]) > 0)
    return btts / len(jogos) if jogos else 0

# Função para simular um jogo usando uma média de gols
def simular_jogo(media_gols_casa, media_gols_fora):
    gols_casa = random.randint(0, int(media_gols_casa + 1))  # Simples alternativa ao Poisson
    gols_fora = random.randint(0, int(media_gols_fora + 1))
    return {"gols_casa": gols_casa, "gols_fora": gols_fora}
