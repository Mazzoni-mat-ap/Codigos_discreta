"""Gera as figuras e tabelas do relatório LaTeX.

Execute na raiz do repositório:  python -m fuga.relatorio
Saída: relatorio/figuras/*.pdf, relatorio/gerado/*.tex e uma cópia do código
em relatorio/gerado/codigo/ (assim a pasta relatorio/ compila sozinha no Overleaf).
"""

import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fuga import mapa
from fuga.algoritmos import bfs, dijkstra, salas_obrigatorias, tempo_do_caminho
from fuga.grafo import INF, criar_grafo, grafo_original, matriz_adjacencia, matriz_pesos

RAIZ = Path(__file__).resolve().parent.parent
FIGURAS = RAIZ / "relatorio" / "figuras"
GERADO = RAIZ / "relatorio" / "gerado"

SEM_9_11 = [p for p in mapa.PORTAS if p[:2] != (9, 11)]
CENARIOS = [
    # (nome, arquivo da figura, portas abertas, salas bloqueadas)
    ("Mapa original", None, mapa.PORTAS, []),
    ("Fumaça na $v_{17}$", "fumaca", mapa.PORTAS, [17]),
    ("Corredor $v_9$--$v_{11}$ alagado", "alagado", SEM_9_11, []),
    ("Os dois juntos", "dois", SEM_9_11, [17]),
    ("Sala de controle trancada", "controle", mapa.PORTAS, [21]),
]
PREDIO = [
    ("Prédio sem fogo", []),
    ("Fogo na cozinha ($v_{14}$)", [14]),
    ("Fogo e fumaça na escada B ($v_{14}, v_{10}$)", [14, 10]),
    ("Fogo nas duas escadas ($v_{14}, v_{10}, v_9$)", [14, 10, 9]),
]


def escrever(arquivo, linhas):
    (GERADO / arquivo).write_text("\n".join(linhas) + "\n", encoding="utf-8")


def num(x):
    """Número no formato brasileiro para o LaTeX (vírgula decimal)."""
    return f"{x:g}".replace(".", "{,}")


def caminho_tex(c):
    return "$" + r" \to ".join(f"v_{{{v}}}" for v in c) + "$"


def figura(G, caminho, bloqueadas, obrigatorias, arquivo, pos=mapa.POSICOES,
           entrada=mapa.ENTRADA, saida=mapa.SAIDA):
    """Mesmo estilo do app, em fundo branco para impressão."""
    xs = [x for x, _ in pos.values()]
    ys = [y for _, y in pos.values()]
    largura = 12
    altura = largura * (max(ys) - min(ys) + 0.8) / (max(xs) - min(xs) + 1)
    fig, ax = plt.subplots(figsize=(largura, altura))
    no_caminho = set(zip(caminho, caminho[1:])) if caminho else set()
    for u in G:
        for v, tempo in G[u].items():
            if u > v:
                continue
            azul = (u, v) in no_caminho or (v, u) in no_caminho
            (x1, y1), (x2, y2) = pos[u], pos[v]
            ax.plot([x1, x2], [y1, y2], color="#2563eb" if azul else "#9ca3af",
                    lw=3 if azul else 1, zorder=1)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{tempo:g}", fontsize=8, ha="center",
                    va="center", color="#374151", zorder=2,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
    for s, (x, y) in pos.items():
        if s in bloqueadas:
            cor = "#dc2626"
        elif s in (entrada, saida):
            cor = "#16a34a"
        elif s in obrigatorias:
            cor = "#d97706"
        else:
            cor = "#4b5563"
        ax.scatter([x], [y], s=330, color=cor, zorder=3)
        ax.text(x, y, str(s), color="white", fontsize=8, ha="center", va="center",
                fontweight="bold", zorder=4)
    ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
    ax.set_ylim(min(ys) - 0.4, max(ys) + 0.4)
    ax.axis("off")
    fig.savefig(FIGURAS / f"{arquivo}.pdf", bbox_inches="tight")
    plt.close(fig)


def matriz_tex(M, arquivo):
    n = len(M)
    linhas = [r"\begin{tabular}{c|" + "c" * n + "}",
              " & " + " & ".join(f"$v_{{{j}}}$" for j in range(1, n + 1)) + r" \\ \hline"]
    for i, linha in enumerate(M, start=1):
        celulas = [r"$\infty$" if x == INF else f"{x:g}" for x in linha]
        linhas.append(f"$v_{{{i}}}$ & " + " & ".join(celulas) + r" \\")
    linhas.append(r"\end{tabular}")
    escrever(arquivo, linhas)


def potencias_de_A(G):
    """Menor k com (A^k)_{1,25} > 0 e quantos caminhos de comprimento k existem."""
    A = matriz_adjacencia(G)
    n = len(A)
    P = A
    k = 1
    while P[0][n - 1] == 0:
        P = [[sum(P[i][l] * A[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        k += 1
    return k, P[0][n - 1]


def caminhos_com_k_arestas(G, u, v, k):
    """Todos os caminhos de u a v com exatamente k arestas (busca exaustiva)."""
    if k == 0:
        return [[u]] if u == v else []
    return [[u] + resto for w in sorted(G[u]) for resto in caminhos_com_k_arestas(G, w, v, k - 1)]


def main():
    FIGURAS.mkdir(parents=True, exist_ok=True)
    GERADO.mkdir(parents=True, exist_ok=True)
    G = grafo_original()
    obrig = salas_obrigatorias(G, 1, 25)

    # Mapa e os dois caminhos
    figura(G, [], [], obrig, "mapa")
    figura(G, dijkstra(G, 1, 25), [], obrig, "caminho_rapido")
    figura(G, bfs(G, 1, 25), [], obrig, "caminho_portas")
    matriz_tex(matriz_adjacencia(G), "matriz_adjacencia.tex")
    matriz_tex(matriz_pesos(G), "matriz_pesos.tex")

    # Nome de cada sala, em três colunas
    itens = [f"$v_{{{s}}}$ & {mapa.NOMES[s]}" for s in sorted(mapa.NOMES)]
    linhas = [r"\begin{tabular}{rl|rl|rl}", r"\toprule"]
    for i in range(0, len(itens), 3):
        grupo = itens[i:i + 3] + [" & "] * (3 - len(itens[i:i + 3]))
        linhas.append(" & ".join(grupo) + r" \\")
    linhas += [r"\bottomrule", r"\end{tabular}"]
    escrever("nomes_salas.tex", linhas)

    # Potências da matriz de adjacência
    k, quantidade = potencias_de_A(G)
    caminhos = caminhos_com_k_arestas(G, 1, 25, k)
    assert len(caminhos) == quantidade
    linhas = [r"\begin{tabular}{cl}", r"\toprule", r"Tempo (min) & Caminho \\", r"\midrule"]
    for c in sorted(caminhos, key=lambda c: tempo_do_caminho(G, c)):
        linhas.append(f"{tempo_do_caminho(G, c):g} & {caminho_tex(c)} \\\\")
    linhas += [r"\bottomrule", r"\end{tabular}"]
    escrever("caminhos_11.tex", linhas)

    graus = sorted((len(G[v]) for v in G), reverse=True)
    impares = sum(1 for g in graus if g % 2)
    escrever("numeros.tex", [
        rf"\newcommand{{\kmin}}{{{k}}}",
        rf"\newcommand{{\qtdcaminhos}}{{{quantidade}}}",
        rf"\newcommand{{\sequenciagraus}}{{({', '.join(map(str, graus))})}}",
        rf"\newcommand{{\grauminimo}}{{{min(graus)}}}",
        rf"\newcommand{{\graumaximo}}{{{max(graus)}}}",
        rf"\newcommand{{\somagraus}}{{{sum(graus)}}}",
        rf"\newcommand{{\impares}}{{{impares}}}",
    ])

    # Cenários do mapa original
    tabela = [r"\begin{tabular}{lccc}", r"\toprule",
              r"Cenário & Menor tempo & Menos portas & Escapa? \\", r"\midrule"]
    lista = [r"\begin{itemize}"]
    for nome, arquivo, portas, bloqueadas in CENARIOS:
        H = criar_grafo(portas, bloqueadas)
        rapido, poucas = dijkstra(H, 1, 25), bfs(H, 1, 25)
        if rapido:
            t = tempo_do_caminho(H, rapido)
            tabela.append(f"{nome} & {t:g} ({len(rapido) - 1}) & "
                          f"{tempo_do_caminho(H, poucas):g} ({len(poucas) - 1}) & "
                          f"{'sim' if t <= mapa.TEMPO_LIMITE else 'não'} \\\\")
            lista.append(rf"\item \textbf{{{nome}:}} {caminho_tex(rapido)}.")
        else:
            tabela.append(rf"{nome} & $\infty$ & $\infty$ & não \\")
            lista.append(rf"\item \textbf{{{nome}:}} não há caminho.")
        if arquivo:
            figura(H, rapido, bloqueadas, salas_obrigatorias(H, 1, 25) if rapido else [],
                   f"cenario_{arquivo}")
    tabela += [r"\bottomrule", r"\end{tabular}"]
    lista.append(r"\end{itemize}")
    escrever("tabela_cenarios.tex", tabela)
    escrever("caminhos_cenarios.tex", lista)

    # Caso real: prédio em chamas (cenário salvo em cenarios.json)
    c = json.loads((RAIZ / "cenarios.json").read_text(encoding="utf-8"))["Prédio em chamas"]
    pos = {int(s): tuple(p) for s, p in c["posicoes"].items()}
    portas = [tuple(p) for p in c["portas"]]
    tabela = [r"\begin{tabular}{lccc}", r"\toprule",
              r"Situação & Menor tempo & Menos portas & Escapa? \\", r"\midrule"]
    for i, (nome, bloqueadas) in enumerate(PREDIO):
        H = criar_grafo(portas, bloqueadas, c["n"])
        rapido, poucas = dijkstra(H, 1, c["n"]), bfs(H, 1, c["n"])
        if rapido:
            t = tempo_do_caminho(H, rapido)
            tabela.append(f"{nome} & {num(t)} ({len(rapido) - 1}) & "
                          f"{num(tempo_do_caminho(H, poucas))} ({len(poucas) - 1}) & "
                          f"{'sim' if t <= c['limite'] else 'não'} \\\\")
        else:
            tabela.append(rf"{nome} & $\infty$ & $\infty$ & não \\")
        if i in (0, 2):
            figura(H, rapido, bloqueadas, salas_obrigatorias(H, 1, c["n"]) if rapido else [],
                   f"predio_{i}", pos, 1, c["n"])
    tabela += [r"\bottomrule", r"\end{tabular}"]
    escrever("tabela_predio.tex", tabela)
    escrever("nomes_predio.tex", [", ".join(f"$v_{{{s}}}$ {nome}" for s, nome in
                                            sorted((int(s), n) for s, n in c["nomes"].items()))])

    codigo = GERADO / "codigo"
    shutil.rmtree(codigo, ignore_errors=True)
    codigo.mkdir(parents=True, exist_ok=True)
    for nome in ["mapa.py", "grafo.py", "algoritmos.py"]:
        shutil.copy(RAIZ / "fuga" / nome, codigo / nome)
    print("Figuras e tabelas geradas em relatorio/")


if __name__ == "__main__":
    main()
