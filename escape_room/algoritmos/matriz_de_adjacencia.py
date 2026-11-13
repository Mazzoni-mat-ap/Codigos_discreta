# Matriz de adjacência correspondente ao grafo do Escape Room

# Vai ter que alterar o modo de buscar os indices, pq eu usei numpy

import numpy as np

# Número de vértices
n = 25

# Inicializa a matriz com infinito
matriz_pesos = np.full((n, n), np.inf)

# Diagonal principal igual a zero
np.fill_diagonal(matriz_pesos, 0)

# Arestas: (vértice 1, vértice 2, peso)
arestas = [
    (1, 2, 3),
    (1, 3, 4),
    (2, 3, 3),
    (2, 4, 3),
    (3, 4, 4),
    (4, 5, 3),
    (4, 6, 2),
    (4, 8, 5),
    (5, 8, 3),
    (6, 8, 3),
    (7, 8, 5),
    (7, 10, 3),
    (8, 9, 2),
    (8, 10, 6),
    (9, 11, 2),
    (10, 11, 3),
    (10, 12, 2),
    (11, 12, 2),
    (12, 13, 3),
    (12, 14, 4),
    (13, 14, 4),
    (13, 15, 2),
    (14, 15, 3),
    (15, 16, 4),
    (15, 17, 4),
    (15, 18, 7),
    (16, 18, 2),
    (16, 19, 4),
    (17, 18, 3),
    (17, 20, 4),
    (18, 20, 4),
    (18, 21, 6),
    (19, 21, 5),
    (20, 21, 2),
    (21, 22, 4),
    (21, 23, 3),
    (22, 24, 4),
    (23, 24, 4),
    (23, 25, 3),
    (24, 25, 4)
]

# Preenche a matriz de pesos
for u, v, peso in arestas:
    matriz_pesos[u - 1, v - 1] = peso
    matriz_pesos[v - 1, u - 1] = peso

print(matriz_pesos)