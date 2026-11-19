# Fuga do Laboratório - Caminhos Mínimos com Matemática Discreta

Trabalho de Matemática Discreta (FGV EMAp). Um escape room de 25 salas e 40 portas
modelado como grafo ponderado: cada sala é um vértice, cada porta uma aresta e o peso
é o tempo do corredor em minutos. O objetivo é ir de `v1` a `v25` em até 40 minutos.

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
