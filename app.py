"""Simulador da Fuga do Laboratório.  Execute com:  streamlit run app.py"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from fuga import mapa
from fuga.algoritmos import bfs, dijkstra, salas_obrigatorias, tempo_do_caminho
from fuga.desenho import AZUL, JS, LARANJA, ROXO, VERDE, VERMELHO, desenhar
from fuga.grafo import INF, criar_grafo, ler_matriz, matriz_adjacencia, matriz_pesos

st.set_page_config(page_title="Simulador", layout="wide")

# Componente que mostra o SVG do mapa e devolve a sala clicada.
mapa_clicavel = st.components.v2.component("mapa_clicavel", js=JS)

ARQUIVO_CENARIOS = Path(__file__).parent / "cenarios.json"
PRINCIPAL = "Jogo principal"


# ---------------------------------------------------------------- cenários
# Um cenário guarda o número de salas, as portas (com seus tempos), as portas
# fechadas, as salas bloqueadas, a entrada, a saída e o tempo limite.
# Os cenários criados na interface ficam em cenarios.json.

def cenario_principal():
    return {"n": mapa.N_SALAS, "portas": [list(p) for p in mapa.PORTAS], "fechadas": [],
            "bloqueadas": [], "entrada": mapa.ENTRADA, "saida": mapa.SAIDA,
            "limite": mapa.TEMPO_LIMITE, "nomes": mapa.NOMES}


def ler_cenarios():
    cenarios = {PRINCIPAL: cenario_principal()}
    if ARQUIVO_CENARIOS.exists():
        cenarios.update(json.loads(ARQUIVO_CENARIOS.read_text(encoding="utf-8")))
    return cenarios


def gravar_cenario(nome, cenario):
    cenarios = ler_cenarios()
    cenarios[nome] = cenario
    criados = {nome: c for nome, c in cenarios.items() if nome != PRINCIPAL}
    ARQUIVO_CENARIOS.write_text(json.dumps(criados, indent=2, ensure_ascii=False),
                                encoding="utf-8")


def abrir_cenario():
    c = ler_cenarios()[st.session_state.cenario]
    st.session_state.n = c["n"]
    st.session_state.todas_portas = [tuple(p) for p in c["portas"]]
    st.session_state.fechadas = [tuple(p) for p in c["fechadas"]]
    st.session_state.bloqueadas = list(c["bloqueadas"])
    st.session_state.entrada = c["entrada"]
    st.session_state.saida = c["saida"]
    st.session_state.limite = c["limite"]
    # Opcionais: posição e nome de cada sala no desenho (as chaves do JSON são texto).
    st.session_state.posicoes = {int(s): p for s, p in c.get("posicoes", {}).items()}
    st.session_state.nomes = {int(s): nome for s, nome in c.get("nomes", {}).items()} or None
    st.session_state.versao += 1  # recria a tabela de corredores


def importar_matriz():
    """Lê a matriz enviada (arquivo ou texto colado) e cria um cenário com ela."""
    arquivo = st.session_state.arquivo_matriz
    texto = arquivo.getvalue().decode("utf-8-sig") if arquivo else st.session_state.texto_matriz
    try:
        n, portas = ler_matriz(texto)
    except ValueError as erro:
        st.session_state.erro_importacao = str(erro)
        return
    nome = st.session_state.nome_importado.strip()
    gravar_cenario(nome, {"n": n, "portas": [list(p) for p in portas], "fechadas": [],
                          "bloqueadas": [], "entrada": 1, "saida": n,
                          "limite": st.session_state.limite})
    st.session_state.erro_importacao = ""
    st.session_state.nome_importado = ""
    st.session_state.cenario = nome
    abrir_cenario()


def excluir_cenario():
    cenarios = ler_cenarios()
    del cenarios[st.session_state.cenario]
    criados = {nome: c for nome, c in cenarios.items() if nome != PRINCIPAL}
    ARQUIVO_CENARIOS.write_text(json.dumps(criados, indent=2, ensure_ascii=False),
                                encoding="utf-8")
    st.session_state.cenario = PRINCIPAL
    abrir_cenario()


if "cenario" not in st.session_state:
    st.session_state.cenario = PRINCIPAL
    st.session_state.versao = 0
    st.session_state.erro_importacao = ""
    abrir_cenario()

cenarios = ler_cenarios()
n = st.session_state.n

# ---------------------------------------------------------------- barra lateral

with st.sidebar:
    st.selectbox("Cenário", list(cenarios), key="cenario", on_change=abrir_cenario)
    if st.session_state.cenario != PRINCIPAL:
        st.button("Excluir este cenário", on_click=excluir_cenario)
    salas = list(range(1, n + 1))
    col1, col2 = st.columns(2)
    rotulo = lambda v: f"v{v} {(st.session_state.nomes or {}).get(v, '')}".strip()
    col1.selectbox("Entrada", salas, key="entrada", format_func=rotulo)
    col2.selectbox("Saída", salas, key="saida", format_func=rotulo)
    st.number_input("Tempo limite (min)", 1, 1000, key="limite")

    st.write("Corredores")
    tabela = pd.DataFrame([
        {"Porta": f"v{u}–v{v}", "Minutos": t, "Aberta": (u, v) not in st.session_state.fechadas}
        for u, v, t in st.session_state.todas_portas
    ])
    tabela = st.data_editor(
        tabela, hide_index=True, disabled=["Porta"], height=300,
        column_config={"Minutos": st.column_config.NumberColumn(min_value=0.1, required=True)},
        key=f"tabela_{st.session_state.versao}",
    )
    pares = [(u, v) for u, v, _ in st.session_state.todas_portas]
    st.session_state.todas_portas = [(u, v, float(linha.Minutos))
                                     for (u, v), linha in zip(pares, tabela.itertuples())]
    st.session_state.fechadas = [(u, v) for (u, v), linha in zip(pares, tabela.itertuples())
                                 if not linha.Aberta]


# ---------------------------------------------------------------- cálculos

E, S, T = st.session_state.entrada, st.session_state.saida, st.session_state.limite
# A entrada e a saída nunca ficam bloqueadas.
st.session_state.bloqueadas = [b for b in st.session_state.bloqueadas if b not in (E, S)]

abertas = [(u, v, t) for u, v, t in st.session_state.todas_portas
           if (u, v) not in st.session_state.fechadas]
G = criar_grafo(abertas, st.session_state.bloqueadas, n)
rapido = dijkstra(G, E, S)
poucas_portas = bfs(G, E, S)
obrigatorias = salas_obrigatorias(G, E, S) if rapido else []

# ---------------------------------------------------------------- página

st.title("Simulador")
aba_sim, aba_mat = st.tabs(["Simulação", "Matrizes"])

with aba_sim:
    if E == S:
        st.warning("Escolha uma entrada diferente da saída.")
    elif rapido is None:
        st.error("Não existe caminho da entrada até a saída.")
    elif tempo_do_caminho(G, rapido) <= T:
        st.success(f"Dá para escapar: {tempo_do_caminho(G, rapido):g} de {T} min.")
    else:
        st.error(f"Não dá tempo: o caminho mais rápido leva {tempo_do_caminho(G, rapido):g} min.")

    svg = desenhar(G, n, st.session_state.bloqueadas, rapido, poucas_portas, obrigatorias, E, S,
                   st.session_state.posicoes, st.session_state.nomes)
    sala = mapa_clicavel(data=svg, key="mapa", on_clique_change=lambda: None).clique

    # Clique numa sala: bloqueia se estiver livre, libera se estiver bloqueada.
    if sala and sala not in (E, S):
        if sala in st.session_state.bloqueadas:
            st.session_state.bloqueadas.remove(sala)
        else:
            st.session_state.bloqueadas.append(sala)
        st.rerun()

    legenda = [(VERDE, "●", "Entrada e saída"), (LARANJA, "●", "Sala obrigatória"),
               (VERMELHO, "●", "Bloqueada"), (AZUL, "━━", "Menor tempo (Dijkstra)"),
               (ROXO, "━━", "Menos portas (BFS)")]
    st.markdown(" &nbsp;&nbsp; ".join(f'<span style="color:{cor}">{simbolo}</span> {texto}'
                                      for cor, simbolo, texto in legenda),
                unsafe_allow_html=True)
    st.caption("Clique numa sala para bloquear ou liberar.")

    if rapido:
        st.dataframe(pd.DataFrame([
            {"Critério": "Menor tempo (Dijkstra)", "Portas": len(rapido) - 1,
             "Minutos": f"{tempo_do_caminho(G, rapido):g}",
             "Caminho": " → ".join(f"v{v}" for v in rapido)},
            {"Critério": "Menos portas (BFS)", "Portas": len(poucas_portas) - 1,
             "Minutos": f"{tempo_do_caminho(G, poucas_portas):g}",
             "Caminho": " → ".join(f"v{v}" for v in poucas_portas)},
        ]), hide_index=True)
        nomes_salas = st.session_state.nomes or {}
        st.write("Salas obrigatórias: " + (", ".join(
            f"v{v} ({nomes_salas[v]})" if v in nomes_salas else f"v{v}" for v in obrigatorias)
            or "nenhuma"))

with aba_mat:
    nomes = [f"v{i}" for i in range(1, n + 1)]
    st.subheader("Matriz de adjacência")
    st.dataframe(pd.DataFrame(matriz_adjacencia(G, n), index=nomes, columns=nomes))

    st.subheader("Matriz de pesos (minutos)")
    pesos = pd.DataFrame([["∞" if x == INF else f"{x:g}" for x in linha]
                          for linha in matriz_pesos(G, n)], index=nomes, columns=nomes)
    st.dataframe(pesos)
    st.download_button("Baixar matriz de pesos (CSV)", pesos.to_csv().encode("utf-8-sig"),
                       "matriz_pesos.csv", "text/csv")

    st.subheader("Importar matriz de pesos")
    st.caption("Uma linha por sala, valores separados por vírgula, ponto e vírgula ou espaço. "
               "Fora da diagonal, 0 ou ∞ significa que não há porta. Até 25 salas.")
    st.file_uploader("Arquivo CSV ou TXT", type=["csv", "txt"], key="arquivo_matriz")
    st.text_area("Ou cole a matriz", height=160, key="texto_matriz",
                 placeholder="0 3 4\n3 0 2\n4 2 0")
    st.text_input("Nome do cenário", key="nome_importado")
    st.button("Importar como novo cenário", on_click=importar_matriz,
              disabled=not st.session_state.nome_importado.strip())
    if st.session_state.erro_importacao:
        st.error(st.session_state.erro_importacao)
