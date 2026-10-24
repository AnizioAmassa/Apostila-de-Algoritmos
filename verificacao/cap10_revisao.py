#!/usr/bin/env python3
"""Capítulo 10 (escolha de estruturas e algoritmos): estimativas e exemplos."""
from fractions import Fraction
from functools import cmp_to_key
from math import ceil, log2

from comum import Verificador

v = Verificador("10_revisao.tex", "respostas/10.tex")
OPS = 1e8  # operações por segundo

# Tabela de tempos
v.igual((round(1e3 * log2(1e3), -4), 1e6 / OPS), (1e4, 0.01), "n=10^3")
v.igual((round(1e6 * log2(1e6) / 1e7), round(1e6 * log2(1e6) / OPS, 1)), (2, 0.2), "n=10^6, n log n")
v.igual(round(1e12 / OPS / 3600, 1), 2.8, "n=10^6, n^2: quase 3 horas")
v.igual((round(1e9 * log2(1e9) / 1e10), round(1e9 * log2(1e9) / OPS / 60)), (3, 5), "n=10^9, n log n")
v.igual(1e18 / OPS / (365.25 * 86400) > 300, True, "n=10^9, n^2: mais de 300 anos")

# Painel de servidores
v.igual(round(1e4 * log2(1e4) / 1e5, 1), 1.3, "10^4 log2 10^4 ≈ 1,3·10^5")

# Par mais próximo numa reta
pos = [17, 3, 42, 25, 9, 40]
o = sorted(pos)
dif = [b - a for a, b in zip(o, o[1:])]
v.tem("a ordem é $" + ",".join(map(str, o)) + "$", "postes em ordem")
v.tem("são $" + ",".join(map(str, dif)) + "$", "diferenças entre vizinhos")
v.igual(min(dif), 2, "menor distância")
n = 10 ** 6
v.igual((n * (n - 1) // 2 / 1e11, n * (n - 1) / 2 / OPS > 3600), (4.999995, True), "versão quadrática")

# Juntando dois catálogos
a, b = [3, 8, 15, 21], [5, 8, 9, 21, 30]
i = j = 0
out = []
while i < len(a) and j < len(b):
    if a[i] < b[j]:
        out.append(a[i]); i += 1
    elif a[i] > b[j]:
        out.append(b[j]); j += 1
    else:
        out.append(a[i]); i += 1; j += 1
out += a[i:] + b[j:]
v.tem("dão $(" + ",".join(map(str, out)) + ")$", "intercalação sem repetidos")

# Frações com pouca memória: n log2 n com n = 10^5
v.igual(round(1e5 * log2(1e5) / 1e6, 1), 1.7, "heapsort de 10^5 frações: cerca de 1,7·10^6 comparações")
v.tem("cerca de $1{,}7\\cdot10^6$, sem memória extra", "estimativa no texto")
fr = [(3, 7), (-1, 2), (5, 11), (2, 9), (6, 14)]
compara = lambda a, b: (a[0] * b[1] > b[0] * a[1]) - (a[0] * b[1] < b[0] * a[1])
v.igual([Fraction(*t) for t in sorted(fr, key=cmp_to_key(compara))], sorted(Fraction(*t) for t in fr),
        "p/q < r/s se e somente se ps < rq (denominadores positivos)")

# --- Respostas ---
v.igual(round(1e8 * log2(1e8) / 1e9, 1), 2.7, "rv-idades: n log2 n ≈ 2,7·10^9")
v.igual(ceil(500 / 12), 42, "rv-externo: 42 blocos de 12 GB")

v.fim()
