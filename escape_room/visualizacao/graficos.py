import matplotlib.pyplot as plt
import networkx as nx
from escape_room.algoritmos.grafo import criar_grafo
from escape_room.algoritmos.matriz_de_adjacencia import matriz_pesos



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

    nx.draw(G, pos, with_labels=True, node_color=cores, edge_color=cores_arestas, node_size=500, font_size=16)

    # mudei node_size, pq os vértices tavam muito grandes, aí tava ruim de ver as arestas

    # adicionei esse bloco aí embaixo pra visualizar os pesos

    pesos = nx.get_edge_attributes(G, 'weight')

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=pesos
    )
    
    plt.show()


if __name__ == "__main__":

    # Cria o grafo usando sua matriz de pesos
    G = criar_grafo(matriz_pesos)
    print("Vértices:", G.number_of_nodes())
    print("Arestas:", G.number_of_edges())

    # Chama a função de visualização
    visualizar_grafo(
        G,
        entrada=1,
        saida=25,
        criticas=[],
        caminho=None
    )