"""Algoritmos do trabalho, implementados sem bibliotecas de grafos."""

from collections import deque

from fuga.grafo import INF


def tempo_do_caminho(G, caminho):
    """Soma dos tempos das portas de um caminho."""
    return sum(G[u][v] for u, v in zip(caminho, caminho[1:]))


def montar_caminho(anterior, destino):
    """Volta de sala em sala pelo dicionário `anterior` até a origem."""
    caminho = [destino]
    while caminho[-1] in anterior:
        caminho.append(anterior[caminho[-1]])
    return caminho[::-1]


def bfs(G, origem, destino):
    """Busca em largura: caminho com o MENOR NÚMERO DE PORTAS (ignora os tempos).

    Visita as salas em camadas: primeiro as vizinhas da origem, depois as
    vizinhas das vizinhas, e assim por diante. Devolve None se não houver caminho.
    """
    if origem not in G or destino not in G:
        return None
    anterior = {}
    visitadas = {origem}
    fila = deque([origem])
    while fila:
        u = fila.popleft()
        if u == destino:
            return montar_caminho(anterior, destino)
        for v in sorted(G[u]):
            if v not in visitadas:
                visitadas.add(v)
                anterior[v] = u
                fila.append(v)
    return None


def dijkstra(G, origem, destino):
    """Dijkstra: caminho de MENOR TEMPO. Devolve None se não houver caminho.

    A cada passo, fixa a sala não visitada mais próxima da origem e tenta
    melhorar a distância das vizinhas dela passando por ela.
    """
    if origem not in G or destino not in G:
        return None
    dist = {v: INF for v in G}
    dist[origem] = 0
    anterior = {}
    visitadas = set()
    while len(visitadas) < len(G):
        u = min((v for v in G if v not in visitadas), key=lambda v: dist[v])
        if dist[u] == INF:
            break  # as salas que sobraram são inalcançáveis
        visitadas.add(u)
        for v, tempo in G[u].items():
            if dist[u] + tempo < dist[v]:
                dist[v] = dist[u] + tempo
                anterior[v] = u
    if dist[destino] == INF:
        return None
    return montar_caminho(anterior, destino)


def salas_obrigatorias(G, origem, destino):
    """Salas sem as quais não existe caminho da origem ao destino.

    Testa uma por uma: tira a sala do grafo e roda a BFS.
    Se a BFS não achar caminho, a sala é obrigatória.
    """
    obrigatorias = []
    for sala in G:
        if sala in (origem, destino):
            continue
        sem_sala = {u: {v: t for v, t in viz.items() if v != sala}
                    for u, viz in G.items() if u != sala}
        if bfs(sem_sala, origem, destino) is None:
            obrigatorias.append(sala)
    return obrigatorias
