# Escape Room: anÃ¡lise de rotas e riscos com Teoria dos Grafos

Projeto acadÃªmico de Teoria dos Grafos desenvolvido em Python. A proposta Ã© representar ambientes como grafos e estudar caminhos entre uma entrada e uma saÃ­da, pontos de articulaÃ§Ã£o e efeitos do bloqueio de salas ou passagens.

> **Escopo:** protÃ³tipo didÃ¡tico. Os resultados nÃ£o substituem projetos, normas ou sistemas profissionais de evacuaÃ§Ã£o e seguranÃ§a.

## Objetivos

- Representar salas como vÃ©rtices e portas/passagens como arestas.
- Construir um grafo ponderado a partir de uma matriz de adjacÃªncia.
- Encontrar caminhos de menor custo entre entrada e saÃ­da.
- Identificar pontos de articulaÃ§Ã£o e salas cuja remoÃ§Ã£o desconecta entrada e saÃ­da.
- Simular bloqueios de salas e passagens.
- Comparar cenÃ¡rios de risco, como alagamentos e interdiÃ§Ãµes.
- Visualizar os grafos, os pesos das arestas e os caminhos encontrados.

## Modelo matemÃ¡tico

O modelo utiliza grafos simples, ponderados e nÃ£o direcionados, com limite de atÃ© 25 salas.

- Cada vÃ©rtice representa uma sala.
- Cada aresta representa uma passagem entre duas salas.
- O peso da aresta representa o custo de percorrer aquela passagem.
- Como o grafo Ã© nÃ£o direcionado, as passagens podem ser percorridas nos dois sentidos.

A matriz de adjacÃªncia ponderada deve ser quadrada e simÃ©trica.

- Valores positivos representam o custo de uma passagem.
- Zero na diagonal representa ausÃªncia de laÃ§os.
- Infinito (`inf`) representa ausÃªncia de conexÃ£o entre duas salas.
- Pesos negativos nÃ£o sÃ£o permitidos.

## Algoritmos e funcionalidades

- **Menor caminho:** utiliza o algoritmo de caminho mÃ­nimo ponderado do NetworkX.
- **Pontos de articulaÃ§Ã£o:** identifica vÃ©rtices cuja remoÃ§Ã£o aumenta o nÃºmero de componentes conexos.
- **Salas crÃ­ticas:** identifica salas cuja remoÃ§Ã£o desconecta especificamente a entrada da saÃ­da.
- **Bloqueios:** simula a remoÃ§Ã£o de salas e passagens.
- **VisualizaÃ§Ã£o:** destaca entrada, saÃ­da, salas crÃ­ticas, caminhos e pesos das arestas.

## Tecnologias

- Python 3.14 (ou versÃ£o compatÃ­vel)
- [NetworkX](https://networkx.org/) para representaÃ§Ã£o e anÃ¡lise de grafos.
- [NumPy](https://numpy.org/) para manipulaÃ§Ã£o de matrizes.
- [Matplotlib](https://matplotlib.org/) para visualizaÃ§Ã£o.

## Estrutura do projeto

```text
Codigos_discreta/
â”œâ”€â”€ README.md
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .gitignore
â””â”€â”€ escape_room/
    â”œâ”€â”€ main.py
    â”œâ”€â”€ algoritmos/
    â”‚   â”œâ”€â”€ grafo.py
    â”‚   â”œâ”€â”€ matriz_de_adjacencia.py
    â”‚   â””â”€â”€ rotas.py
    â””â”€â”€ visualizacao/
        â””â”€â”€ graficos.py
```

## Como executar

1. Clone o repositÃ³rio e entre na pasta:

   ```bash
   git clone https://github.com/Mazzoni-mat-ap/Codigos_discreta.git
   cd Codigos_discreta
   ```

2. Instale as dependÃªncias:

   ```bash
   py -m pip install -r requirements.txt
   ```

3. Execute o projeto:

   ```bash
   py -m escape_room.main
   ```

## AplicaÃ§Ãµes

O projeto demonstra como a Teoria dos Grafos pode auxiliar na anÃ¡lise de rotas e na identificaÃ§Ã£o de pontos crÃ­ticos em ambientes sujeitos a situaÃ§Ãµes de risco.

Entre as aplicaÃ§Ãµes simuladas estÃ£o:

- EvacuaÃ§Ã£o de ambientes.
- Bloqueio de salas e passagens.
- InterdiÃ§Ã£o de rotas por alagamentos.
- IdentificaÃ§Ã£o de gargalos e pontos de articulaÃ§Ã£o.
- ComparaÃ§Ã£o de rotas alternativas considerando seus custos.
