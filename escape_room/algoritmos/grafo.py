import numpy as np
import networkx as nx
from escape_room.algoritmos.matriz_de_adjacencia import matriz_pesos

def criar_grafo(matriz):
    """
    Recebe uma matriz de adjacência e constrói um grafo.
    Cada vértice representa uma sala.
    Cada aresta representa uma porta.
    """

    n = len(matriz)

    if n == 0:
        raise ValueError("A matriz não pode estar vazia.")

    if n > 25:
        raise ValueError("O limite do projeto é de 25 salas.")

    for linha in matriz:
        if len(linha) != n:
            raise ValueError("A matriz precisa ser quadrada.")

    for i in range(n):
        for j in range(n):

            # if matriz[i][j] not in (0, 1):
            #     raise ValueError("A matriz deve conter apenas 0 e 1.")

            # Comentei as linhas acima, pq agora o grafo tem pesos, 
            # e coloquei uma correção da validação abaixo

            if not np.isfinite(matriz[i][j]) and not np.isposinf(matriz[i][j]):
                raise ValueError("Peso inválido.")

            if matriz[i][j] != matriz[j][i]:
                raise ValueError("A matriz precisa ser simétrica.")

            if i == j and matriz[i][j] != 0:
                raise ValueError("Não são permitidos laços.")

    G = nx.Graph()

    G.add_nodes_from(range(1, n + 1))

    # for i in range(n):
    #     for j in range(i + 1, n):
    #         if matriz[i][j] == 1:
    #             G.add_edge(i + 1, j + 1)

    # não tava aparecendo as arestas, aí eu criei o bloco abaixo:

    for i in range(n):
        for j in range(i + 1, n):

            peso = matriz[i][j]

            if np.isfinite(peso):
                G.add_edge(i + 1, j + 1, weight=int(peso))

    return G
