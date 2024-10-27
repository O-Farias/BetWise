from fastapi import APIRouter, HTTPException, Query
from .utils import buscar_jogos, listar_ligas
from .services import criar_jogo_mock
from .models import Jogo
from .logging_config import registrar_log

router = APIRouter()

# Rota para buscar jogos reais
@router.get("/jogos-reais")
async def get_jogos_reais(
    liga_id: int = Query(..., description="ID da liga"),
    temporada: int = Query(..., description="Ano da temporada")
):
    registrar_log(f"Requisição recebida: /jogos-reais?liga_id={liga_id}&temporada={temporada}")

    try:
        dados = buscar_jogos(liga_id, temporada)
        if dados is None:
            raise ValueError("Nenhum dado encontrado")
    except Exception as e:
        registrar_log(f"Erro ao buscar jogos: {str(e)}", nivel='error')
        raise HTTPException(status_code=500, detail="Erro interno ao buscar jogos")

    return dados

# Rota para listar ligas disponíveis
@router.get("/ligas")
async def get_ligas():
    registrar_log("Requisição recebida: /ligas")
    ligas = listar_ligas()
    if ligas is None:
        registrar_log("Erro ao buscar ligas", nivel='error')
        raise HTTPException(status_code=400, detail="Erro ao buscar ligas")
    return ligas

# Rota para retornar um jogo mockado
@router.get("/jogo-mock", response_model=Jogo)
async def get_jogo_mock():
    registrar_log("Requisição recebida: /jogo-mock")
    return criar_jogo_mock()
