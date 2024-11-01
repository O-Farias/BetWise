from fastapi import APIRouter, HTTPException, Query
from .utils import (buscar_partidas, listar_ligas, buscar_partida_especifica, 
                    analisar_h2h, calcular_btts, simular_jogo)
from .services import criar_jogo_mock
from .models import Jogo
from .logging_config import registrar_log
from datetime import date

router = APIRouter()

# Rota para buscar partidas reais (agora com parâmetros opcionais de data)
@router.get("/partidas")
async def get_partidas(
    competicao_id: str = Query(..., description="ID da competição"),
    temporada: int = Query(..., description="Ano da temporada"),
    date_from: str = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    date_to: str = Query(None, description="Data final no formato YYYY-MM-DD")
):
    registrar_log(f"Requisição recebida: /partidas?competicao_id={competicao_id}&temporada={temporada}")

    try:
        # Passa as datas como parâmetros opcionais
        dados = buscar_partidas(competicao_id, temporada, date_from, date_to)
        if not dados:
            raise ValueError("Nenhum dado encontrado")
    except Exception as e:
        registrar_log(f"Erro ao buscar partidas: {str(e)}", nivel='error')
        raise HTTPException(status_code=500, detail="Erro interno ao buscar partidas")

    return dados

# Rota para listar competições disponíveis
@router.get("/ligas")
async def get_ligas():
    registrar_log("Requisição recebida: /ligas")

    try:
        ligas = listar_ligas()
        if not ligas:
            raise ValueError("Nenhuma liga encontrada")
    except Exception as e:
        registrar_log(f"Erro ao buscar ligas: {str(e)}", nivel='error')
        raise HTTPException(status_code=500, detail="Erro interno ao buscar ligas")

    return ligas

# Rota para retornar um jogo mockado
@router.get("/jogo-mock", response_model=Jogo)
async def get_jogo_mock():
    registrar_log("Requisição recebida: /jogo-mock")
    return criar_jogo_mock()

# Rota para buscar e analisar um jogo específico
@router.get("/analise-jogo")
async def analise_jogo(
    competicao_id: str = Query(..., description="ID da competição"),
    temporada: int = Query(..., description="Ano da temporada"),
    time_1: str = Query(..., description="Nome do time da casa"),
    time_2: str = Query(..., description="Nome do time visitante"),
    data_jogo: str = Query(..., description="Data do jogo (YYYY-MM-DD)")
):
    registrar_log(f"Analisando jogo: {time_1} vs {time_2} em {data_jogo}")

    try:
        # Buscar o jogo específico
        jogo = buscar_partida_especifica(competicao_id, temporada, time_1, time_2, data_jogo)
        if not jogo:
            raise ValueError("Jogo não encontrado")

        # Chamar a função de análise H2H
        h2h_result = analisar_h2h([jogo])

        # Calcular a probabilidade de BTTS
        btts_prob = calcular_btts([jogo])

        # Simular o resultado do jogo
        simulacao = simular_jogo(h2h_result["media_gols"], h2h_result["media_gols"])

        # Recomendação com base na análise
        recomendacao = (
            "Apostar em BTTS" if btts_prob > 0.5 
            else "Não apostar em BTTS"
        )

        # Retornar o resultado completo
        return {
            "jogo": jogo,
            "media_gols": h2h_result["media_gols"],
            "probabilidade_btts": btts_prob,
            "simulacao": simulacao,
            "recomendacao": recomendacao
        }

    except Exception as e:
        registrar_log(f"Erro na análise do jogo: {str(e)}", nivel='error')
        raise HTTPException(status_code=500, detail=f"Erro ao buscar ou analisar o jogo: {str(e)}")


@router.get("/proxima-partida-brasileirao")
async def get_proxima_partida_brasileirao(
    temporada: int = Query(..., description="Ano da temporada")
):
    # ID da Série A do Brasileirão na API
    competicao_id = "2013"  # Ajuste para o ID correto do Brasileirão
    registrar_log(f"Requisição recebida: /proxima-partida-brasileirao?temporada={temporada}")

    try:
        proxima_partida = buscar_partidas(competicao_id, temporada, proxima=True)
        if not proxima_partida:
            raise ValueError("Nenhuma próxima partida encontrada")

        # Análise da próxima partida usando H2H e probabilidades de BTTS
        h2h_result = analisar_h2h([proxima_partida])
        btts_prob = calcular_btts([proxima_partida])

        # Simulação da partida com base na média de gols
        simulacao = simular_jogo(h2h_result["media_gols"], h2h_result["media_gols"])

        # Recomendação de aposta com base na análise
        recomendacao = (
            "Apostar em BTTS" if btts_prob > 0.5 
            else "Não apostar em BTTS"
        )

        return {
            "proxima_partida": proxima_partida,
            "analise": {
                "media_gols": h2h_result["media_gols"],
                "probabilidade_btts": btts_prob,
                "simulacao": simulacao,
                "recomendacao": recomendacao
            }
        }

    except Exception as e:
        registrar_log(f"Erro ao buscar a próxima partida: {str(e)}", nivel='error')
        raise HTTPException(status_code=500, detail="Erro ao buscar a próxima partida")

