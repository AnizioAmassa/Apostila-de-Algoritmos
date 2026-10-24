#!/usr/bin/env python3
"""Capítulo 12 (Floyd-Warshall)."""
from math import inf, log2

from comum import Verificador

v = Verificador("12_floyd_warshall.tex", "respostas/12.tex")
R = "respostas/12.tex"


def matriz(n, arestas, diag=0):
    W = [[inf] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        W[i][i] = diag
    for a, b, p in arestas:
        W[a][b] = p
    return W


def floyd(W):
    n = len(W) - 1
    D = [row[:] for row in W]
    P = [[i if i != j and W[i][j] < inf else None for j in range(n + 1)] for i in range(n + 1)]
    etapas, mudancas = [], []
    for k in range(1, n + 1):
        mud = []
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if D[i][k] + D[k][j] < D[i][j]:
                    mud.append((i, j, D[i][j], D[i][k] + D[k][j]))
                    D[i][j] = D[i][k] + D[k][j]
                    P[i][j] = P[k][j]
        etapas.append([row[:] for row in D])
        mudancas.append(mud)
    return D, P, etapas, mudancas


def caminho(P, i, j):
    if i == j:
        return [i]
    return caminho(P, i, P[i][j]) + [j]


def fmt(x):
    return "\\infty" if x == inf else str(x)


def linha(D, i):
    return "(" + ",".join(fmt(x) for x in D[i][1:]) + ")"


W = matriz(5, [(1, 2, 1), (1, 3, 3), (1, 5, 6), (2, 3, 1), (2, 4, 3), (3, 1, 1), (3, 2, 2),
               (3, 4, 1), (4, 1, 3), (4, 5, 2), (5, 4, 1)])
for i in range(1, 6):
    v.tem(f"{i}\\,($" + "abcde"[i - 1] + "$) & " + " & ".join(fmt(x) if x != inf else "$\\infty$"
          for x in W[i][1:]), f"linha {i} da matriz W")
D, P, etapas, mudancas = floyd(W)
# Exemplo da iteração k = 1
D1 = etapas[0]
for i in range(1, 6):
    v.tem(f"{i}/{{" + ",".join(fmt(x) for x in D1[i][1:]) + "}", f"figura de D^1, linha {i}")
v.igual([(i, j) for i, j, _, _ in mudancas[0]], [(3, 5), (4, 2), (4, 3)], "entradas que mudam com k=1")
# Tabela das mudanças por iteração
for k, mud in enumerate(mudancas, 1):
    if mud:
        txt = ";".join(f"$D({i},{j})\\!:{fmt(a)}\\to{b}$" for i, j, a, b in mud)
        v.tem(f"{k} & " + txt, f"mudanças com k={k}")
    else:
        v.tem(f"{k} & nenhuma", f"mudanças com k={k}")
for i in range(1, 6):
    v.tem(f"{i} & " + " & ".join(str(x) for x in D[i][1:]), f"linha {i} de D^5")
    v.tem(f"{i} & " + " & ".join("--" if x is None else str(x) for x in P[i][1:]), f"linha {i} de P^5")
v.igual((caminho(P, 5, 3), D[5][3]), ([5, 4, 1, 2, 3], 6), "caminho de 5 a 3")
v.tem("$P(5,3)=2$, $P(5,2)=1$, $P(5,1)=4$ e $P(5,4)=5$", "reconstrução do caminho de 5 a 3")
v.igual(round(20 ** 2 * 2 ** 20 / 1e8, 1), 4.2, "n^2 2^n com n=20")

# Pesos negativos
D2, *_ = floyd(matriz(3, [(1, 2, 4), (2, 3, -2), (1, 3, 3)]))
v.igual((D2[1][3], [D2[i][i] for i in range(1, 4)]), (2, [0, 0, 0]), "aresta negativa sem ciclo")
D3, *_ = floyd(matriz(3, [(1, 2, 1), (2, 3, -4), (3, 1, 2)]))
v.igual((D3[1][1] < 0, D3[2][2] < 0, D3[3][3] < 0, D3[1][1]), (True, True, True, -1), "ciclo negativo")

# --- Respostas ---
for i in range(1, 6):
    v.tem("(" + ",".join(map(str, D[i][1:])) + ")", f"fw-slide: linha {i}", R)
v.igual((caminho(P, 2, 1), D[2][1]), ([2, 3, 1], 2), "fw-slide: caminho de 2 a 1")
Dn, Pn, *_ = floyd(matriz(5, [(1, 2, 3), (1, 3, 8), (1, 5, -4), (2, 4, 1), (2, 5, 7), (3, 2, 4),
                             (4, 1, 2), (4, 3, -5), (5, 4, 6)]))
for i in range(1, 6):
    v.tem(linha(Dn, i), f"fw-neg: linha {i}", R)
v.igual(caminho(Pn, 1, 2), [1, 5, 4, 3, 2], "fw-neg: caminho de 1 a 2")
T = matriz(5, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (3, 4, 1)])
Dt, *_ = floyd(T)
alc = {i: {j for j in range(1, 6) if Dt[i][j] < inf} for i in range(1, 6)}
v.igual(alc, {1: {1, 2, 3, 4}, 2: {1, 2, 3, 4}, 3: {1, 2, 3, 4}, 4: {4}, 5: {5}}, "fw-fecho")
Dc, *_ = floyd(matriz(4, [(1, 2, 2), (2, 3, 3), (3, 1, 1), (3, 4, 5), (4, 3, 2)], diag=inf))
v.igual([Dc[i][i] for i in range(1, 5)], [6, 6, 6, 7], "fw-ciclo")
W4 = matriz(4, [(1, 2, 4), (1, 4, 10), (2, 3, 3), (3, 4, 1), (4, 1, 2), (3, 1, 7)])
D4, P4, et4, _ = floyd(W4)
for k, Dk in enumerate(et4, 1):
    v.tem(f"$D^{k}$: " + ("linhas " if k == 1 else "") + ", ".join(f"${linha(Dk, i)}$" for i in range(1, 4))
          + f" e ${linha(Dk, 4)}$", f"fw-4v: D^{k}", R)
for i in range(1, 5):
    v.tem("(" + ",".join("-" if x is None else str(x) for x in P4[i][1:]) + ")", f"fw-4vcam: P^4 linha {i}", R)
v.igual((caminho(P4, 2, 1), D4[2][1], caminho(P4, 4, 3), D4[4][3]), ([2, 3, 4, 1], 6, [4, 1, 2, 3], 9),
        "fw-4vcam: caminhos")
_, _, etx, _ = floyd(matriz(2, [(1, 2, 1), (2, 1, -3)]))
v.igual((etx[0][2][2], etx[1][1][1]), (-2, -2), "fw-negex: D(2,2) com k=1 e D(1,1) com k=2")
exc = [max(D[i][1:]) for i in range(1, 6)]
v.igual((exc, max(exc), exc.index(min(exc)) + 1), ([5, 4, 3, 5, 6], 6, 3), "fw-diam")
n, m = 10 ** 4, 5 * 10 ** 4
v.igual((n ** 3, round(n * (n + m) * log2(n) / 1e9)), (10 ** 12, 8), "fw-dij")

v.fim()
