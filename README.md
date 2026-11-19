# Caminhos Mínimos com Matemática Discreta
### Otimização de rotas de fuga por meio de algoritmos aplicados em Teoria dos Grafos
Trabalho de Matemática Discreta (FGV EMAp). O objetivo é usar Teoria dos Grafos para
encontrar rotas de fuga: os lugares viram vértices, as ligações entre eles viram arestas
e o tempo de travessia vira o peso. Com esse modelo, o trabalho responde três perguntas:
se dá para sair a tempo, qual é a rota mais rápida (Dijkstra) e quais pontos não podem
ser bloqueados. Também compara essa rota com a de menos ligações (BFS).

O simulador funciona com qualquer matriz de pesos. Além do caso principal, há um exemplo
de evacuação de uma cidade hipotética durante uma enchente.

## Caso principal: Fuga do Laboratório

Um escape room de 25 salas e 40 portas. Cada sala é um vértice, cada porta uma aresta e o
peso é o tempo do corredor em minutos. O objetivo é ir de `v1` a `v25` em até 40 minutos.

| Critério | Algoritmo | Portas | Tempo |
|---|---|---|---|
| Menos portas | BFS | 11 | 43 min (fica preso) |
| Menor tempo | Dijkstra | 13 | 38 min (escapa) |

As salas `v4`, `v8`, `v12`, `v15` e `v21` são obrigatórias: bloquear qualquer uma
torna a fuga impossível.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py                 # simulador
python -m unittest discover tests    # testes
python -m fuga.relatorio             # regera figuras e tabelas do relatório
```

No simulador, clique numa sala do mapa para bloquear ou liberar. Na barra lateral dá
para trocar a entrada e a saída, mudar o tempo limite e o tempo de cada corredor, e fechar
portas. Na aba Matrizes dá para importar uma matriz de pesos (colando ou por arquivo CSV)
como um cenário novo; os cenários ficam em `cenarios.json`. O exemplo
`exemplos/enchente.csv` é a evacuação de uma cidade hipotética durante uma enchente.

## Estrutura

```text
app.py               simulador (Streamlit)
fuga/
  mapa.py            salas, portas e tempos do enunciado
  grafo.py           monta o grafo e as matrizes
  algoritmos.py      BFS, Dijkstra e salas obrigatórias
  desenho.py         desenho do mapa em SVG
  relatorio.py       gera figuras e tabelas do relatório
tests/               testes
relatorio/           relatório em LaTeX
docs/                enunciado com o mapa e as matrizes
```

## Relatório

Fonte em `relatorio/relatorio.tex`. Para compilar no Overleaf, envie a pasta
`relatorio/` inteira e compile com pdfLaTeX.

## Autores

Frederico Taveira Martins de Souza, Ian Luca Marinho Aguiar, João Vitor Neves Mazzoni,
Marcelo Maiato Neves.
