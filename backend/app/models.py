# Criação e validação de um modelo de dados com Pydantic

from pydantic import BaseModel
class Jogo(BaseModel):
    time_casa: str
    time_fora: str
    gols_casa: int
    gols_fora: int
    data: str
