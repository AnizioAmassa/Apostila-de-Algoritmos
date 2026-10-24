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

# --- Exercícios novos ---
v.igual((round(5e5 ** 2 / OPS), round(5e5 * log2(5e5) / 1e6, 1), round(5e5 * log2(5e5) / OPS, 1), 2000 ** 3 / OPS),
        (2500, 9.5, 0.1, 80.0), "rv-estimativa")
pos = [31, 4, 18, 45, 12, 27, 40, 9]
o = sorted(pos)
dif = [b - a for a, b in zip(o, o[1:])]
v.igual((o, dif, min(dif), len(dif), len(pos) * (len(pos) - 1) // 2),
        ([4, 9, 12, 18, 27, 31, 40, 45], [5, 3, 6, 9, 4, 9, 5], 3, 7, 28), "rv-postes")
a, b = [2, 7, 11, 15, 20], [3, 7, 9, 15, 22, 30]
i = j = comps = 0
out = []
while i < len(a) and j < len(b):
    comps += 1
    if a[i] < b[j]:
        out.append(a[i]); i += 1
    elif a[i] > b[j]:
        out.append(b[j]); j += 1
    else:
        out.append(a[i]); i += 1; j += 1
out += a[i:] + b[j:]
v.igual((out, comps), ([2, 3, 7, 9, 11, 15, 20, 22, 30], 7), "rv-catalogos")
listas, onde = {}, {}
for s_, carga in zip("ABCDE", (70, 95, 70, 40, 95)):
    listas.setdefault(carga, []).insert(0, s_)
    onde[s_] = carga
v.igual(listas, {95: ["E", "B"], 70: ["C", "A"], 40: ["D"]}, "rv-painel (a)")
for s_, carga in (("C", 99), ("B", 60)):
    listas[onde[s_]].remove(s_)
    listas.setdefault(carga, []).insert(0, s_)
    onde[s_] = carga
relatorio = [s_ for c in range(100, -1, -1) for s_ in listas.get(c, [])]
v.igual((relatorio[:3], relatorio), (["C", "E", "A"], ["C", "E", "A", "B", "D"]), "rv-painel (c)")

v.fim()
