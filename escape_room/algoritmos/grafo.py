import numpy as np
import networkx as nx


def criar_grafo(matriz):
    """
    Recebe uma matriz de adjacência ponderada e constrói um grafo.
    Cada vértice representa uma sala.
    Cada aresta representa uma passagem, com seu respectivo peso.
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
            peso = matriz[i][j]

            if not (np.isfinite(peso) or np.isposinf(peso)):
                raise ValueError("Peso inválido.")

            if np.isfinite(peso) and peso < 0:
                raise ValueError("Os pesos não podem ser negativos.")

            if peso != matriz[j][i]:
                raise ValueError("A matriz precisa ser simétrica.")

            if i == j and peso != 0:
                raise ValueError("Não são permitidos laços.")

    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))

    for i in range(n):
        for j in range(i + 1, n):
            peso = matriz[i][j]

            if np.isfinite(peso):
                G.add_edge(i + 1, j + 1, weight=float(peso))

    return G
