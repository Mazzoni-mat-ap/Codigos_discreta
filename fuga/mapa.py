# Dados do mapa da Fuga do Laboratório (ver docs/Fuga_do_Laboratorio.pdf).

N_SALAS = 25
ENTRADA = 1
SAIDA = 25
TEMPO_LIMITE = 40  # minutos

# Cada porta: (sala, sala, tempo do corredor em minutos). São 40 portas.
PORTAS = [
    (1, 2, 3), (1, 3, 4), (2, 3, 3), (2, 4, 3), (3, 4, 4),
    (4, 5, 3), (4, 6, 2), (4, 8, 5), (5, 8, 3), (6, 8, 3),
    (7, 8, 5), (7, 10, 3), (8, 9, 2), (8, 10, 6), (9, 11, 2),
    (10, 11, 3), (10, 12, 2), (11, 12, 2), (12, 13, 3), (12, 14, 4),
    (13, 14, 4), (13, 15, 2), (14, 15, 3), (15, 16, 4), (15, 17, 4),
    (15, 18, 7), (16, 18, 2), (16, 19, 4), (17, 18, 3), (17, 20, 4),
    (18, 20, 4), (18, 21, 6), (19, 21, 5), (20, 21, 2), (21, 22, 4),
    (21, 23, 3), (22, 24, 4), (23, 24, 4), (23, 25, 3), (24, 25, 4),
]

# Nome de cada sala. As cinco obrigatórias da história são v4, v8, v12, v15 e v21.
NOMES = {
    1: "Entrada", 2: "Recepção", 3: "Sala de espera", 4: "Portaria",
    5: "Vestiário", 6: "Almoxarifado",
    7: "Laboratório de química", 8: "Sala das máscaras", 9: "Laboratório de biologia",
    10: "Laboratório de física", 11: "Laboratório de microscopia", 12: "Sala de limpeza",
    13: "Arquivo de documentos", 14: "Arquivo de amostras", 15: "Sala das câmeras",
    16: "Depósito de reagentes", 17: "Depósito de equipamentos", 18: "Depósito central",
    19: "Câmara fria", 20: "Depósito de vidraria", 21: "Sala de controle",
    22: "Corredor de serviço", 23: "Hall de saída", 24: "Sala de segurança", 25: "Saída",
}

# Posição (x, y) de cada sala no desenho.
POSICOES = {
    1: (0, 0), 2: (1, 1), 3: (1, -1), 4: (2, 0),
    5: (3, 1), 6: (3, -1), 8: (4, 0),
    9: (5, 1), 7: (5, -1), 11: (6, 1), 10: (6, -1), 12: (7, 0),
    13: (8, 1), 14: (8, -1), 15: (9, 0),
    17: (10, 1), 16: (10, -1), 18: (11, 0), 20: (12, 1), 19: (12, -1), 21: (13, 0),
    23: (14, 1), 22: (14, -1), 24: (15, -0.4), 25: (16, 0.3),
}
