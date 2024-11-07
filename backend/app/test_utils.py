# Importa as funções de utils.py
from .utils import buscar_partidas, listar_ligas, buscar_partida_especifica

def testar_funcoes():
    # Teste de buscar partidas para uma temporada específica
    print("Teste: buscar_partidas")
    season_id = 19734  # Use um season_id real da SportMonks
    partidas = buscar_partidas(season_id)
    if partidas:
        print("Partidas encontradas:", partidas[:1])  # Mostra o primeiro item
    else:
        print("Nenhuma partida encontrada ou erro na requisição.")

    # Teste de listar ligas
    print("\nTeste: listar_ligas")
    ligas = listar_ligas()
    if ligas:
        print("Ligas encontradas:", ligas[:1])  # Mostra o primeiro item
    else:
        print("Nenhuma liga encontrada ou erro na requisição.")

    # Teste de buscar partida específica
    print("\nTeste: buscar_partida_especifica")
    fixture_id = 1035456  # Substitua por um ID de fixture real para testar
    partida = buscar_partida_especifica(fixture_id)
    if partida:
        print("Partida específica encontrada:", partida)
    else:
        print("Partida não encontrada ou erro na requisição.")

# Executa os testes
if __name__ == "__main__":
    testar_funcoes()
