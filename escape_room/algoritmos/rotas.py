import networkx as nx


def menor_caminho(G, entrada, saida):
    """Encontra o menor caminho entre duas salas."""

    try:
        caminho = nx.shortest_path(
            G,
            source=entrada,
            target=saida
        )

        distancia = len(caminho) - 1

        return caminho, distancia

    except nx.NetworkXNoPath:
        return None, None


def pontos_articulacao(G):
    """Identifica todos os vértices de corte do grafo."""

    return list(nx.articulation_points(G))


def salas_criticas_rota(G, entrada, saida):
    """
    Identifica salas cuja remoção desconecta
    especificamente a entrada da saída.
    """

    criticas = []

    for sala in pontos_articulacao(G):

        if sala == entrada or sala == saida:
            continue

        copia = G.copy()
        copia.remove_node(sala)

        if not nx.has_path(copia, entrada, saida):
            criticas.append(sala)

    return criticas


def simular_bloqueio_sala(G, sala, entrada, saida):
    """Simula o bloqueio de uma sala."""

    copia = G.copy()

    if sala not in copia:
        raise ValueError("Sala inexistente.")

    copia.remove_node(sala)

    return menor_caminho(copia, entrada, saida)
