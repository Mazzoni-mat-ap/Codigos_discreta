"""Testes. Execute com:  python -m unittest discover tests"""

import random
import unittest
from pathlib import Path

import networkx as nx

from fuga import mapa
from fuga.algoritmos import bfs, dijkstra, salas_obrigatorias, tempo_do_caminho
from fuga.grafo import (criar_grafo, grafo_original, ler_matriz, matriz_adjacencia,
                        matriz_pesos)


class TestEnunciado(unittest.TestCase):
    """Confere os números do enunciado (docs/Fuga_do_Laboratorio.pdf)."""

    def setUp(self):
        self.G = grafo_original()

    def test_tamanho(self):
        self.assertEqual(len(self.G), 25)
        self.assertEqual(sum(len(viz) for viz in self.G.values()) // 2, 40)

    def test_matrizes_simetricas(self):
        A, W = matriz_adjacencia(self.G), matriz_pesos(self.G)
        for i in range(25):
            self.assertEqual(W[i][i], 0)
            for j in range(25):
                self.assertEqual(A[i][j], A[j][i])
                self.assertEqual(W[i][j], W[j][i])
        self.assertEqual(sum(map(sum, A)), 2 * 40)

    def test_mais_rapido(self):
        c = dijkstra(self.G, 1, 25)
        self.assertEqual(c, [1, 2, 4, 8, 9, 11, 12, 13, 15, 17, 20, 21, 23, 25])
        self.assertEqual(tempo_do_caminho(self.G, c), 38)

    def test_menos_portas(self):
        c = bfs(self.G, 1, 25)
        self.assertEqual(c, [1, 2, 4, 8, 10, 12, 13, 15, 18, 21, 23, 25])
        self.assertEqual(tempo_do_caminho(self.G, c), 43)

    def test_salas_obrigatorias(self):
        self.assertEqual(salas_obrigatorias(self.G, 1, 25), [4, 8, 12, 15, 21])

    def test_bloquear_obrigatoria_impede_fuga(self):
        for sala in [4, 8, 12, 15, 21]:
            G = criar_grafo(mapa.PORTAS, salas_bloqueadas=[sala])
            self.assertIsNone(dijkstra(G, 1, 25))

    def test_cenarios_do_relatorio(self):
        sem_9_11 = [p for p in mapa.PORTAS if p[:2] != (9, 11)]
        casos = [
            (mapa.PORTAS, [17], 40),   # fumaça na v17
            (sem_9_11, [], 40),        # corredor v9-v11 alagado
            (sem_9_11, [17], 42),      # os dois juntos
        ]
        for portas, bloqueadas, esperado in casos:
            G = criar_grafo(portas, bloqueadas)
            self.assertEqual(tempo_do_caminho(G, dijkstra(G, 1, 25)), esperado)


class TestImportacao(unittest.TestCase):
    def test_ida_e_volta(self):
        W = matriz_pesos(grafo_original())
        texto = "\n".join(",".join("inf" if x == float("inf") else f"{x:g}" for x in linha)
                          for linha in W)
        n, portas = ler_matriz(texto)
        self.assertEqual(n, 25)
        self.assertEqual(criar_grafo(portas), grafo_original())

    def test_matrizes_invalidas(self):
        for texto in ["0 1\n2 0", "0 -1\n-1 0", "0 1 2\n1 0"]:
            with self.assertRaises(ValueError):
                ler_matriz(texto)

    def test_enchente(self):
        texto = Path("exemplos/enchente.csv").read_text(encoding="utf-8")
        n, portas = ler_matriz(texto)
        casos = [
            ([], [], 104),
            ([], [4], 104),
            ([], [2], 120),
            ([(10, 11)], [2], 130),
            ([], [2, 10], None),
        ]
        for fechadas, bloqueadas, esperado in casos:
            abertas = [p for p in portas if p[:2] not in fechadas]
            G = criar_grafo(abertas, bloqueadas, n)
            caminho = dijkstra(G, 1, 14)
            tempo = tempo_do_caminho(G, caminho) if caminho else None
            self.assertEqual(tempo, esperado)


class TestContraNetworkX(unittest.TestCase):
    """Compara com a biblioteca NetworkX em 200 grafos aleatórios."""

    def test_aleatorios(self):
        for semente in range(200):
            rnd = random.Random(semente)
            portas = {}
            while len(portas) < 35:
                u, v = sorted(rnd.sample(range(1, 26), 2))
                portas[(u, v)] = rnd.randint(1, 9)
            G = criar_grafo([(u, v, t) for (u, v), t in portas.items()])
            N = nx.Graph()
            N.add_nodes_from(G)
            N.add_weighted_edges_from((u, v, t) for (u, v), t in portas.items())

            for destino in range(2, 26):
                if not nx.has_path(N, 1, destino):
                    self.assertIsNone(dijkstra(G, 1, destino))
                    self.assertIsNone(bfs(G, 1, destino))
                    continue
                self.assertEqual(tempo_do_caminho(G, dijkstra(G, 1, destino)),
                                 nx.dijkstra_path_length(N, 1, destino))
                self.assertEqual(len(bfs(G, 1, destino)) - 1,
                                 nx.shortest_path_length(N, 1, destino))


if __name__ == "__main__":
    unittest.main()
