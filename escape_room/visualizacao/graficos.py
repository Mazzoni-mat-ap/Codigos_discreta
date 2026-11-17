
import matplotlib.pyplot as plt
import networkx as nx

from escape_room.algoritmos.grafo import criar_grafo
from escape_room.algoritmos.matriz_de_adjacencia import matriz_pesos


def visualizar_grafo(G, entrada, saida, criticas, caminho):
    """
    Visualiza o grafo usando Matplotlib.
    Cada nó representa uma sala e cada aresta representa uma porta.
    """

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)

    cores = []

    for node in G.nodes():
        if node == entrada:
            cores.append("green")
        elif node == saida:
            cores.append("red")
        elif node in criticas:
            cores.append("orange")
        else:
            cores.append("lightblue")

    arestas_caminho = set()

    if caminho is not None:
        for i in range(len(caminho) - 1):
            arestas_caminho.add(
                frozenset((caminho[i], caminho[i + 1]))
            )

    cores_arestas = [
        "red" if frozenset(aresta) in arestas_caminho else "gray"
        for aresta in G.edges()
    ]

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=cores,
        edge_color=cores_arestas,
        node_size=500,
        font_size=16
    )

    # Exibe os pesos das arestas no grafo.
    pesos = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=pesos
    )

    plt.show()


if __name__ == "__main__":

    # Cria o grafo usando a matriz de pesos.
    G = criar_grafo(matriz_pesos)

    print("Vértices:", G.number_of_nodes())
    print("Arestas:", G.number_of_edges())

    visualizar_grafo(
        G,
        entrada=1,
        saida=25,
        criticas=[],
        caminho=None
    )
