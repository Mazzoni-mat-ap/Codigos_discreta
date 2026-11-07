from algoritmos.grafo import criar_grafo
from algoritmos.rotas import (
    menor_caminho,
    pontos_articulacao,
    salas_criticas_rota,
    simular_bloqueio_sala
)
from visualizacao.graficos import visualizar_grafo


# Matriz de teste
matriz = [
    [0, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0]
]

G = criar_grafo(matriz)

entrada = 1
saida = 5

caminho, distancia = menor_caminho(G, entrada, saida)

print("Menor caminho:", caminho)
print("Distância:", distancia)

print("Pontos de articulação:", pontos_articulacao(G))

print(
    "Salas críticas para a fuga:",
    salas_criticas_rota(G, entrada, saida)
)

# Simulação: bloqueio da sala 2
novo_caminho, nova_distancia = simular_bloqueio_sala(
    G, 2, entrada, saida
)

print("\nApós bloquear a sala 2:")
print("Novo caminho:", novo_caminho)
print("Nova distância:", nova_distancia)

visualizar_grafo(G)