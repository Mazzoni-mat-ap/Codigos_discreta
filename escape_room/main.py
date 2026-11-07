from algoritmos.grafo import criar_grafo
from algoritmos.rotas import (
    menor_caminho,
    pontos_articulacao,
    salas_criticas_rota,
    simular_bloqueio_sala
)
from visualizacao.graficos import visualizar_grafo


# Matriz de teste
matriz = [[0 for _ in range(25)] for _ in range(25)]

for i in range(5):
    for j in range(4):
        atual = i * 5 + j
        direita = atual + 1

        matriz[atual][direita] = 1
        matriz[direita][atual] = 1

for i in range(4):
    for j in range(5):
        atual = i * 5 + j
        abaixo = atual + 5

        matriz[atual][abaixo] = 1
        matriz[abaixo][atual] = 1

G = criar_grafo(matriz)

entrada = 1
saida = 25

caminho, distancia = menor_caminho(G, entrada, saida)

print("Menor caminho:", caminho)
print("Distância:", distancia)

print("Pontos de articulação:", pontos_articulacao(G))

criticas = salas_criticas_rota(G, entrada, saida)

print("Salas crìticas para a fuga:", criticas)


# Simulação: bloqueio da sala 2
novo_caminho, nova_distancia = simular_bloqueio_sala(
    G, 2, entrada, saida
)

print("\nApós bloquear a sala 2:")
print("Novo caminho:", novo_caminho)
print("Nova distância:", nova_distancia)

visualizar_grafo(G, entrada, saida, criticas, caminho)