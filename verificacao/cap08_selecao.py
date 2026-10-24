#!/usr/bin/env python3
"""Capítulo 8 (seleção: quickselect e mediana das medianas)."""
from math import ceil, floor, log2

from comum import Verificador, dec

v = Verificador("08_selecao.tex", "respostas/08.tex")


def quickselect(S, k, pivos):
    """Quickselect com os pivôs dados em sequência; devolve a resposta e o
    registro (pivô, S1, S2, S3, k) de cada chamada."""
    reg = []
    while True:
        m = pivos.pop(0) if pivos else S[-1]  # sem lista: o último elemento
        S1 = [s for s in S if s < m]
        S2 = [s for s in S if s == m]
        S3 = [s for s in S if s > m]
        reg.append((m, S1, S2, S3, k))
        if len(S1) >= k:
            S = S1
        elif len(S1) + len(S2) >= k:
            return m, reg
        else:
            S, k = S3, k - len(S1) - len(S2)


def medianas_de_grupos(S):
    grupos = [S[i:i + 5] for i in range(0, len(S), 5)]
    return grupos, [sorted(g)[(len(g) - 1) // 2] for g in grupos]


# Medianas de {9,4,7,1,8,2}
A = sorted([9, 4, 7, 1, 8, 2])
v.igual((A[floor(7 / 2) - 1], A[ceil(7 / 2) - 1], A[6 - 3]), (4, 7, 7), "medianas e terceiro maior")

# Quickselect passo a passo (Exemplo 8.2)
S = [15, 3, 22, 8, 11, 6, 19, 2, 13]
r, reg = quickselect(S, 5, [13, 3, 8, 11])
v.igual(r, 11, "o 5º menor é 11")
v.igual([(m, k) for m, _, _, _, k in reg], [(13, 5), (3, 5), (8, 3), (11, 1)], "pivôs e valores de k")
v.tem("$S_1=\\{3,8,11,6,2\\}$, $S_2=\\{13\\}$, $S_3=\\{15,22,19\\}$", "partição pelo pivô 13")
v.tem("$S_1=\\{2\\}$, $S_2=\\{3\\}$, $S_3=\\{8,11,6\\}$", "partição pelo pivô 3")
tamanhos = [len(S)] + [len(x[1]) if x[0] == 13 else len(x[3]) for x in reg[:-1]]
v.igual(tamanhos, [9, 5, 3, 1], "tamanhos examinados")
v.tem("$9+5+3+1=18$ elementos", "total examinado")
v.igual(round(9 * log2(9)), 29, "n log2 n para n=9")
v.igual(max(max(p - 1, 100 - p) for p in range(26, 76)), 74, "pivôs centrais deixam no máximo 74")
v.tem("deixam no máximo 74 elementos de cada lado, menos que $3n/4=75$: são 50", "pivôs bons entre 100")

# Mediana das medianas (Exemplo 8.3)
S = [24, 16, 85, 58, 43, 31, 26, 63, 81, 64, 99, 62, 38, 59, 34, 93, 33, 98, 42, 67,
     23, 94, 22, 78, 84, 47, 65, 75, 90, 28, 39, 97, 1, 44, 52]
grupos, med = medianas_de_grupos(S)
v.tem("$" + ",".join(map(str, med)) + "$", "medianas dos grupos")
v.tem("em ordem, $" + ",".join(map(str, sorted(med))) + "$", "medianas em ordem")
m = sorted(med)[(len(med) + 1) // 2 - 1]
S1 = [s for s in S if s < m]
S3 = [s for s in S if s > m]
v.igual((m, len(S1), len(S3), sorted(S)[17]), (63, 20, 14, 58), "pivô, |S1|, |S3| e mediana")
garantidos_maiores = sum(1 for g, md in zip(grupos, med) if md >= m for x in g if x >= md)
garantidos_menores = sum(1 for g, md in zip(grupos, med) if md <= m for x in g if x <= md)
v.igual((garantidos_maiores, garantidos_menores, 35 - 12), (12, 12, 23), "elementos garantidos de cada lado")
v.igual(dec(3 * 35 / 4, 2), "26,25", "3·35/4")
colunas = sorted((sorted(g, reverse=True) for g in grupos), key=lambda g: g[2])
for col, g in enumerate(colunas, 1):
    v.tem(f"{col}/{{" + ",".join(map(str, g)) + "}", f"figura: coluna {col}")

v.igual((3 * floor(1000 / 10), 1000 - 300), (300, 700), "n=1000")
v.igual(20 / 5 + 20 * 3 / 4 + 1, 20.0, "20c n/5 + 20c 3n/4 + cn = 20cn")

# --- Respostas ---
S = [12, 3, 25, 7, 18, 1, 22, 9, 15, 6, 20, 2, 11, 24, 5, 17, 8, 23, 4, 14, 10, 21, 13, 19, 16]
grupos, med = medianas_de_grupos(S)
m = sorted(med)[2]
S1 = [s for s in S if s < m]
S3 = [s for s in S if s > m]
v.tem("Medianas dos grupos: $" + ",".join(map(str, med)) + "$", "se-trace: medianas", "respostas/08.tex")
v.igual((m, len(S1), len(S3), 3 * floor(25 / 10)), (12, 11, 13, 6), "se-trace: pivô e tamanhos")
r, reg = quickselect([7, 2, 9, 4, 3, 8, 6, 1], 4, [])
v.igual(r, 4, "se-qstrace: resposta")
v.igual([(p, sorted(a), sorted(c), k) for p, a, _, c, k in reg],
        [(1, [], [2, 3, 4, 6, 7, 8, 9], 4), (6, [2, 3, 4], [7, 8, 9], 3), (3, [2], [4], 3), (4, [], [], 1)],
        "se-qstrace: chamadas")
v.tem("$S_3=\\{7,2,9,4,3,8,6\\}$", "se-qstrace: 1ª chamada", "respostas/08.tex")
v.tem("$S_1=\\{2,4,3\\}$, $S_2=\\{6\\}$, $S_3=\\{7,9,8\\}$", "se-qstrace: 2ª chamada", "respostas/08.tex")
for n, a, b in ((49, 37, "36{,}75"), (50, 35, "37{,}5")):
    v.igual(n - 3 * (n // 10), a, f"se-n49: n={n}")
v.tem("$49-3\\cdot4=37>36{,}75=3\\cdot49/4$", "se-n49", "respostas/08.tex")
v.tem("$50-3\\cdot5=35\\le37{,}5$", "se-n49", "respostas/08.tex")

v.fim()
