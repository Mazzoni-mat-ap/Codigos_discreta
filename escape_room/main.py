
from escape_room.algoritmos.grafo import criar_grafo
from escape_room.algoritmos.matriz_de_adjacencia import matriz_pesos
from escape_room.algoritmos.rotas import (
    menor_caminho,
    pontos_articulacao,
    salas_criticas_rota,
    simular_bloqueio_sala
)
from escape_room.visualizacao.graficos import visualizar_grafo


# Cria o grafo ponderado.
G = criar_grafo(matriz_pesos)

origem = 13
saidas = [1, 5, 21, 25]

print("Vértices:", G.number_of_nodes())
print("Arestas:", G.number_of_edges())

# Calcula a rota de menor custo para cada saída.
for saida in saidas:
    caminho, custo = menor_caminho(G, origem, saida)

    print(f"\nSaída: {saida}")
    print("Menor caminho:", caminho)
    print("Custo total:", custo)

# Identifica os pontos de articulação.
print("\nPontos de articulação:", pontos_articulacao(G))

# Analisa as salas críticas para a saída 25.
saida = 25
criticas = salas_criticas_rota(G, origem, saida)

print("\nSalas críticas para a fuga:", criticas)

# Simula o bloqueio da sala 2.
novo_caminho, novo_custo = simular_bloqueio_sala(
    G, 2, origem, saida
)

print("\nApós bloquear a sala 2:")
print("Novo caminho:", novo_caminho)
print("Novo custo:", novo_custo)

# Visualiza o caminho original.
caminho, custo = menor_caminho(G, origem, saida)

visualizar_grafo(
    G,
    origem,
    saida,
    criticas,
    caminho
)

# Simula um cenário de alagamento.
G_alagado = G.copy()

arestas_interditadas = [(13, 14), (19, 20)]

for u, v in arestas_interditadas:
    if G_alagado.has_edge(u, v):
        G_alagado.remove_edge(u, v)

print("\nCenário: Rua alagada")

for saida in saidas:
    caminho, custo = menor_caminho(G_alagado, origem, saida)

    print(f"\nSaída: {saida}")
    print("Menor caminho:", caminho)
    print("Custo total:", custo)
