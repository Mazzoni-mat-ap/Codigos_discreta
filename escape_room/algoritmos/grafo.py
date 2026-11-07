import networkx as nx


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

    # Verifica se a matriz é quadrada
    for linha in matriz:
        if len(linha) != n:
            raise ValueError("A matriz precisa ser quadrada.")

    # Verifica se a matriz representa um grafo simples
    for i in range(n):
        for j in range(n):

            if matriz[i][j] not in (0, 1):
                raise ValueError("A matriz deve conter apenas 0 e 1.")

            if matriz[i][j] != matriz[j][i]:
                raise ValueError("A matriz precisa ser simétrica.")

            if i == j and matriz[i][j] != 0:
                raise ValueError("Não são permitidos laços.")

    # Criação do grafo
    G = nx.Graph()

    # Adiciona as salas
    G.add_nodes_from(range(1, n + 1))

    # Adiciona as portas
    for i in range(n):
        for j in range(i + 1, n):
            if matriz[i][j] == 1:
                G.add_edge(i + 1, j + 1)

    return G
