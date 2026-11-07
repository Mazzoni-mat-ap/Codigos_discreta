import matplotlib.pyplot as plt
import networkx as nx


def visualizar_grafo(G):
    """
    Visualiza o grafo usando Matplotlib.
    Cada nó representa uma sala e cada aresta representa uma porta.
    """
    plt.figure()
    pos = nx.spring_layout(G, seed=42)

    cores = [
        'green',
        'lightblue',
        'lightblue',
        'lightblue',
        'red',
        'lightblue'
    ]

    nx.draw(G, pos, with_labels=True, node_color=cores, edge_color='gray', node_size=2000, font_size=16)
    
    plt.show()