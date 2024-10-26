from fastapi import APIRouter

router = APIRouter()

# Rota para buscar dados de jogos (por enquanto, dados mockados)
@router.get("/jogos")
async def get_jogos():
    return [
        {"time_casa": "Flamengo", "time_fora": "Palmeiras", "gols_casa": 2, "gols_fora": 1},
        {"time_casa": "Corinthians", "time_fora": "Santos", "gols_casa": 1, "gols_fora": 1}
    ]

# Rota para recomendações de apostas (dados exemplo)
@router.get("/recomendacoes")
async def get_recomendacoes():
    return {
        "jogo": "Flamengo vs Palmeiras",
        "aposta_recomendada": "Vitória do Flamengo",
        "probabilidade": 0.75
    }
