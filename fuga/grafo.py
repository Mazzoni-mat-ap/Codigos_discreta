"""Montagem do grafo e das matrizes.

O grafo é um dicionário: G[u][v] = tempo da porta entre as salas u e v.
Como as portas funcionam nos dois sentidos, G[u][v] == G[v][u].
"""

import re

from fuga import mapa

INF = float("inf")


def criar_grafo(portas, salas_bloqueadas=(), n=mapa.N_SALAS):
    """Cria o grafo com as salas 1..n a partir de uma lista de portas (u, v, tempo).

    Salas bloqueadas ficam de fora, junto com todas as portas delas.
    """
    G = {v: {} for v in range(1, n + 1) if v not in salas_bloqueadas}
    for u, v, tempo in portas:
        if u in G and v in G:
            G[u][v] = tempo
            G[v][u] = tempo
    return G


def grafo_original():
    return criar_grafo(mapa.PORTAS)


def matriz_adjacencia(G, n=mapa.N_SALAS):
    """a[i][j] = 1 se existe porta entre vi e vj, senão 0."""
    salas = range(1, n + 1)
    return [[1 if j in G.get(i, {}) else 0 for j in salas] for i in salas]


def matriz_pesos(G, n=mapa.N_SALAS):
    """w[i][j] = 0 na diagonal, o tempo se existe porta, infinito se não existe."""
    salas = range(1, n + 1)
    return [[0 if i == j else G.get(i, {}).get(j, INF) for j in salas] for i in salas]


def ler_matriz(texto):
    """Lê uma matriz de pesos escrita como texto (uma linha por sala).

    Aceita valores separados por vírgula, ponto e vírgula, tab ou espaço.
    Fora da diagonal, "0", "inf", "∞", "-" ou vazio significam "sem porta".
    Uma primeira linha ou coluna com nomes (v1, v2, ...) é ignorada.
    Devolve (n, portas) ou levanta ValueError explicando o problema.
    """
    linhas = [re.split(r"[;,\t ]+", l.strip()) for l in texto.strip().splitlines() if l.strip()]

    def numero(x):
        x = x.strip().lower()
        if x in ("", "inf", "∞", "-"):
            return INF
        return float(x)

    def eh_numero(x):
        try:
            numero(x)
            return True
        except ValueError:
            return False

    if linhas and not all(eh_numero(x) for x in linhas[0]):
        linhas = linhas[1:]  # primeira linha com nomes
    if linhas and not eh_numero(linhas[0][0]):
        linhas = [l[1:] for l in linhas]  # primeira coluna com nomes

    n = len(linhas)
    if not 2 <= n <= 25:
        raise ValueError(f"A matriz precisa ter entre 2 e 25 salas (tem {n}).")
    if any(len(l) != n for l in linhas):
        raise ValueError("A matriz precisa ser quadrada: cada linha com o mesmo número de valores.")
    try:
        W = [[numero(x) for x in l] for l in linhas]
    except ValueError:
        raise ValueError("A matriz tem um valor que não é número.") from None

    portas = []
    for i in range(n):
        for j in range(i + 1, n):
            if W[i][j] != W[j][i]:
                raise ValueError(f"A matriz não é simétrica: v{i + 1}–v{j + 1} difere de "
                                 f"v{j + 1}–v{i + 1}.")
            if W[i][j] < 0:
                raise ValueError(f"Tempo negativo na porta v{i + 1}–v{j + 1}.")
            if W[i][j] not in (0, INF):
                portas.append((i + 1, j + 1, W[i][j]))
    return n, portas
