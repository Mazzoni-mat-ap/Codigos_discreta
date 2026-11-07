# Escape Room: análise de rotas e riscos com Teoria dos Grafos

Projeto acadêmico de Teoria dos Grafos desenvolvido em Python. A proposta é representar ambientes como grafos e estudar caminhos entre uma entrada e uma saída, pontos de articulação e efeitos do bloqueio de salas ou passagens.

> **Escopo:** protótipo didático. Os resultados não substituem projetos, normas ou sistemas profissionais de evacuação e segurança.

## Objetivos

- Representar salas como vértices e portas/passagens como arestas.
- Construir um grafo a partir de uma matriz de adjacência.
- Encontrar um menor caminho entre entrada e saída.
- Identificar pontos de articulação e salas cuja remoção desconecta entrada e saída.
- Simular bloqueios e comparar cenários.
- Visualizar os grafos e os resultados.

O modelo atual considera grafos simples e não direcionados, com limite de até 25 salas. A matriz de adjacência deve ser quadrada, simétrica e ter apenas 0 e 1.

## Tecnologias

- Python 3.14 (ou versão compatível)
- [NetworkX](https://networkx.org/) para representação e análise de grafos
- [Matplotlib](https://matplotlib.org/) para visualização

## Estrutura do projeto

```text
Codigos_discreta/
├── README.md
├── requirements.txt
├── .gitignore
└── escape_room/
    ├── main.py
    ├── algoritmos/
    │   ├── grafo.py
    │   └── rotas.py
    ├── simulacao/
    │   └── cenarios.py
    └── visualizacao/
        └── graficos.py
```

## Como executar

1. Clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/Mazzoni-mat-ap/Codigos_discreta.git
   cd Codigos_discreta
   ```

2. (Recomendado) Crie e ative um ambiente virtual:

   **Windows PowerShell**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```bash
   py -m pip install -r requirements.txt
   ```

4. Execute o programa a partir da pasta `escape_room`:

   ```powershell
   cd escape_room
   py main.py
   ```

## Organização do código

- `algoritmos/grafo.py`: valida a matriz de adjacência e constrói o grafo.
- `algoritmos/rotas.py`: reúne as funções de caminhos, pontos de articulação e bloqueio de salas.
- `visualizacao/graficos.py`: funções de representação visual.
- `simulacao/cenarios.py`: espaço destinado à implementação dos cenários de risco.
- `main.py`: ponto de entrada e execução dos testes atuais.

## Estado atual

A versão publicada contém uma matriz pequena de teste para validar a construção do grafo, a busca de menor caminho, a identificação de pontos de articulação e a simulação de bloqueio de uma sala. A visualização e a camada de cenários ainda estão em desenvolvimento. O mapa definitivo de até 25 salas será integrado posteriormente.

## Colaboração

O projeto é desenvolvido em equipe. Para novas funcionalidades, prefira criar uma branch, testar as alterações e abrir um Pull Request para revisão antes de integrar à `main`.
