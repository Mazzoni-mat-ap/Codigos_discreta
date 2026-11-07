import matplotlib.pyplot as plt
import networkx as nx


def visualizar_grafo(G, entrada, saida, criticas, caminho):
    """
    Visualiza o grafo usando Matplotlib.
    Cada nó representa uma sala e cada aresta representa uma porta.
    """
    plt.figure()
    pos = nx.spring_layout(G, seed=42)

    cores = []
    arestas_caminho = []
    cores_arestas = []

    if caminho is not None:
        for i in range(len(caminho) - 1):
            arestas_caminho.append((caminho[i], caminho[i + 1]))

    for node in G.nodes():
        if node == entrada:
            cores.append('green')
        elif node  == saida:
            cores.append('red')
        elif node in criticas:
            cores.append('orange')
        else:
            cores.append('lightblue')

    for aresta in G.edges():
        if aresta in arestas_caminho:
            cores_arestas.append('red')
        else:
            cores_arestas.append('gray')

    nx.draw(G, pos, with_labels=True, node_color=cores, edge_color=cores_arestas, node_size=2000, font_size=16)
    
    plt.show()