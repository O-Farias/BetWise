from .models import Jogo

def criar_jogo_mock():
    return Jogo(
        time_casa="Flamengo",
        time_fora="Palmeiras",
        gols_casa=2,
        gols_fora=1,
        data="2024-10-25"
    )
