from fastapi import APIRouter, HTTPException, Query
from .utils import buscar_partidas, listar_ligas  # Atualizamos os nomes
from .services import criar_jogo_mock
from .models import Jogo
from .logging_config import registrar_log

router = APIRouter()

# Rota para buscar partidas reais
@router.get("/partidas")
async def get_partidas(
    competicao_id: str = Query(..., description="ID da competição"),
    temporada: int = Query(..., description="Ano da temporada")
):
    registrar_log(f"Requisição recebida: /partidas?competicao_id={competicao_id}&temporada={temporada}")

    try:
        dados = buscar_partidas(competicao_id, temporada)
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
