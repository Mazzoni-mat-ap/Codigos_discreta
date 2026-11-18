# Desenho do mapa em SVG: uma linha para cada porta e um círculo para cada sala.

import math

from fuga import mapa

CINZA = "#374151"
VERDE = "#16a34a"
LARANJA = "#d97706"
VERMELHO = "#dc2626"
AZUL = "#3b82f6"
ROXO = "#c084fc"


def posicoes(n, proprias=None):
    """Posição de cada sala em pixels e a altura do desenho.

    Usa as posições do cenário, se ele tiver; senão, o mapa do enunciado (25 salas);
    senão, põe as salas numa elipse. Depois ajusta tudo à largura do desenho.
    """
    if proprias:
        pos = proprias
    elif n == mapa.N_SALAS:
        pos = mapa.POSICOES
    else:
        pos = {s: (2.6 * math.cos(2 * math.pi * (s - 1) / n - math.pi / 2),
                   -math.sin(2 * math.pi * (s - 1) / n - math.pi / 2)) for s in range(1, n + 1)}
    xs = [x for x, _ in pos.values()]
    ys = [y for _, y in pos.values()]
    escala = (1072 - 80) / (max(xs) - min(xs))
    pixels = {s: (40 + (x - min(xs)) * escala, 40 + (max(ys) - y) * escala)
              for s, (x, y) in pos.items()}
    return pixels, 80 + (max(ys) - min(ys)) * escala


def linhas_do_caminho(pos, caminho, cor, deslocamento):
    """Desenha um caminho um pouco deslocado para o lado, para os dois
    caminhos (Dijkstra e BFS) aparecerem lado a lado quando coincidem."""
    linhas = []
    for u, v in zip(caminho, caminho[1:]):
        (x1, y1), (x2, y2) = pos[min(u, v)], pos[max(u, v)]
        tamanho = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        dx, dy = -(y2 - y1) / tamanho * deslocamento, (x2 - x1) / tamanho * deslocamento
        linhas.append(f'<line x1="{x1 + dx}" y1="{y1 + dy}" x2="{x2 + dx}" y2="{y2 + dy}" '
                      f'stroke="{cor}" stroke-width="3"/>')
    return linhas


def cor_da_sala(sala, bloqueadas, obrigatorias, entrada, saida):
    if sala in bloqueadas:
        return VERMELHO
    if sala in (entrada, saida):
        return VERDE
    if sala in obrigatorias:
        return LARANJA
    return CINZA


def desenhar(G, n, bloqueadas, rapido, poucas_portas, obrigatorias, entrada, saida,
             posicoes_proprias=None, nomes=None):
    """rapido: caminho do Dijkstra (azul); poucas_portas: caminho da BFS (roxo)."""
    pos, altura = posicoes(n, posicoes_proprias)
    nomes = nomes or {}
    linhas, textos, salas = [], [], []

    for u in G:
        for v, tempo in G[u].items():
            if u > v:
                continue  # cada porta aparece duas vezes no dicionário
            (x1, y1), (x2, y2) = pos[u], pos[v]
            linhas.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                          f'stroke="#4b5563" stroke-width="1.5"/>')
            textos.append(f'<text class="tempo" x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2}">'
                          f'{tempo:g}</text>')

    linhas += linhas_do_caminho(pos, poucas_portas or [], ROXO, -2.5)
    linhas += linhas_do_caminho(pos, rapido or [], AZUL, 2.5)

    for sala, (x, y) in pos.items():
        nome = nomes.get(sala, f"Sala {sala}")
        salas.append(f'<g class="sala" data-sala="{sala}"><title>{nome}</title>'
                     f'<circle cx="{x}" cy="{y}" r="15" '
                     f'fill="{cor_da_sala(sala, bloqueadas, obrigatorias, entrada, saida)}"/>'
                     f'<text x="{x}" y="{y}">{sala}</text></g>')

    return (f'<svg viewBox="0 0 1072 {altura}" width="100%"><style>' + ESTILO + "</style>"
            + "".join(linhas + textos + salas) + "</svg>")


ESTILO = """
svg text { text-anchor: middle; dominant-baseline: central; font-family: sans-serif; }
.tempo { font-size: 11px; fill: #9ca3af; paint-order: stroke; stroke: #0e1117; stroke-width: 4px; }
.sala text { font-size: 12px; fill: white; pointer-events: none; }
.sala { cursor: pointer; }
.sala:hover circle { stroke: white; stroke-width: 2; }
"""

# Código do componente clicável (usado em app.py).
# Quando uma sala é clicada, envia o número dela para o Python.
JS = """
export default function (componente) {
    const { data, parentElement, setTriggerValue } = componente;
    let div = parentElement.querySelector("div");
    if (!div) { div = document.createElement("div"); parentElement.appendChild(div); }
    div.innerHTML = data;
    div.querySelectorAll("[data-sala]").forEach((sala) => {
        sala.onclick = () => setTriggerValue("clique", Number(sala.dataset.sala));
    });
}
"""
