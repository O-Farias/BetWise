import requests
import os
import random
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

API_TOKEN = os.getenv("FOOTBALL_DATA_API_TOKEN")  # Token da Football-Data.org
BASE_URL = "https://api.football-data.org/v4"  # URL da API

# Função para buscar partidas de uma competição específica e temporada
def buscar_partidas(competicao_id, temporada):
    url = f"{BASE_URL}/competitions/{competicao_id}/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": temporada}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
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
        print(f"Jogos recebidos: {jogos}")  # Verifica se a resposta tem jogos

        for jogo in jogos:
            home_team = jogo["homeTeam"]["name"].lower() if jogo["homeTeam"]["name"] else ""
            away_team = jogo["awayTeam"]["name"].lower() if jogo["awayTeam"]["name"] else ""
            print(f"Comparando {home_team} com {time_1.lower()} e {away_team} com {time_2.lower()}")

            if time_1.lower() in home_team and time_2.lower() in away_team:
                print("Jogo encontrado!")
                return jogo  # Retorna o jogo se encontrado
        print("Jogo não encontrado.")
        return None  # Jogo não encontrado
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return None
    

# Função para garantir que os valores de gols não sejam None
def get_gols(valor):
    if valor is None:
        print(f"Valor de gol encontrado como None, substituindo por 0")
        return 0
    return valor

# Função para analisar H2H (histórico de confrontos diretos)
def analisar_h2h(jogos):
    total_jogos = len(jogos)

    gols_casa = sum(get_gols(jogo["score"]["fullTime"]["home"]) for jogo in jogos)
    gols_fora = sum(get_gols(jogo["score"]["fullTime"]["away"]) for jogo in jogos)

    print(f"Gols Casa: {gols_casa}, Gols Fora: {gols_fora}, Total de Jogos: {total_jogos}")

    # Verificação extra para evitar divisões por 0
    media_gols = (gols_casa + gols_fora) / total_jogos if total_jogos > 0 else 0

    # Calcula a frequência de ambos marcarem, garantindo que os valores sejam inteiros
    ambos_marcam = sum(
        1 for jogo in jogos
        if get_gols(jogo["score"]["fullTime"]["home"]) > 0 and
           get_gols(jogo["score"]["fullTime"]["away"]) > 0
    )

    print(f"Media de Gols: {media_gols}, Ambos Marcam: {ambos_marcam}")

    return {
        "media_gols": media_gols,
        "ambos_marcam_percentual": ambos_marcam / total_jogos if total_jogos > 0 else 0,
        "gols_casa_total": gols_casa,
        "gols_fora_total": gols_fora,
        "total_jogos": total_jogos
    }




# Função para calcular a probabilidade de BTTS (Both Teams to Score)
def calcular_btts(jogos):
    btts = sum(1 for jogo in jogos if jogo["score"]["fullTime"]["home"] > 0 and jogo["score"]["fullTime"]["away"] > 0)
    return btts / len(jogos) if jogos else 0

# Função para simular um jogo usando a distribuição de Poisson
def simular_jogo(media_gols_casa, media_gols_fora):
    gols_casa = random.poisson(media_gols_casa)
    gols_fora = random.poisson(media_gols_fora)
    return {"gols_casa": gols_casa, "gols_fora": gols_fora}
