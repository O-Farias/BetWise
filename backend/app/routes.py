from fastapi import APIRouter, HTTPException
from .utils import buscar_jogos
from.utils import listar_ligas

router = APIRouter()

# Rota para buscar jogos reais de uma liga específica e temporada
@router.get("/jogos-reais")
async def get_jogos_reais(liga_id: int, temporada: int):
    dados = buscar_jogos(liga_id, temporada)

    if dados is None:
        raise HTTPException(status_code=400, detail="Erro ao buscar dados")

    return dados

# Rota para listar todas as ligas disponíveis
@router.get("/ligas")
async def get_ligas():
    ligas = listar_ligas()
    if ligas is None:
        raise HTTPException(status_code=400, detail="Erro ao buscar ligas")
    return ligas



# https://possessed-toad-69597pjpr53r9jg.github.dev/api/jogos-reais?liga_id=39&temporada=2024 > Testar essa rota.
# liga_id=39 é a Premier League, e temporada=2024 é o ano atual.
