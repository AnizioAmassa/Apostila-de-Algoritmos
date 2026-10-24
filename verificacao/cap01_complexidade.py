#!/usr/bin/env python3
"""Capítulo 1 (complexidade): contas dos exemplos e das respostas."""
from fractions import Fraction
from itertools import permutations
from math import floor, log2, log10, sqrt

from comum import Verificador, dec

v = Verificador("01_complexidade.tex", "respostas/01.tex")


def comparacoes_insercao(seq):
    """Comparações da ordenação por inserção do Exemplo 1.1: compara o elemento
    com os anteriores, do mais próximo ao mais distante, até achar um menor ou
    chegar ao início. Devolve a lista de comparações de cada inserção."""
    a = list(seq)
    por_passo = []
    for j in range(1, len(a)):
        x, i, c = a[j], j - 1, 0
        while i >= 0:
            c += 1
            if a[i] > x:
                a[i + 1] = a[i]
                i -= 1
            else:
                break
        a[i + 1] = x
        por_passo.append(c)
    return por_passo


passos = comparacoes_insercao([3, 1, 4, 2])
v.igual(passos, [1, 1, 3], "comparações por linha da figura de [3,1,4,2]")
v.tem("0/{3,1,4,2}/2/{1 comparação},1/{1,3,4,2}/3/{1 comparação},2/{1,3,4,2}/4/{3 comparações}",
      "figura da ordenação por inserção")
todas = [sum(comparacoes_insercao(p)) for p in permutations(range(1, 5))]
media = Fraction(sum(todas), len(todas))
v.igual((min(todas), max(todas), media), (3, 6, Fraction(59, 12)), "três casos para n=4")
v.tem(f"$59/12\\approx{dec(float(media), 2)}$", "caso médio para n=4")
v.tem("(a entrada $[3,1,4,2]$ da figura faz 5)", "comparações de [3,1,4,2]")

# Tabela da soma com laço, a 10^9 iterações por segundo
dias = 10 ** 15 / 1e9 / 86400
anos = 10 ** 30 / 1e9 / (365.25 * 86400)
v.tem(f"$\\approx {dec(dias, 1)}$ dias", "10^15 iterações")
v.igual(round(anos / 1e13), 3, "10^30 iterações em anos (3·10^13)")

# f(n) = n^2 + 10n + 20
f = lambda n: n * n + 10 * n + 20
n0 = min(n for n in range(1, 100) if all(f(k) <= 2 * k * k for k in range(n, 200)))
v.igual(n0, 12, "n0 para c=2")
v.tem("para $n=12$: $140\\le144$", "verificação em n=12")
v.igual((10 * 12 + 20, 12 * 12), (140, 144), "10n+20 e n^2 em n=12")
v.igual(all(f(k) <= 31 * k * k for k in range(1, 1000)), True, "c=31, n0=1")
v.tem("$10n+20$ vale $10\\,020$", "termos menores em n=1000")
v.tem(f"\\approx{dec(1 / log2(10), 3)}\\log_2n", "log10 n em função de log2 n")

# Tabela de tempos a 10^9 passos por segundo
v.tem("$4\\cdot10^{13}$ anos", "2^100 ns em anos")
v.igual(round(2 ** 100 / 1e9 / (365.25 * 86400) / 1e13), 4, "2^100 ns ≈ 4·10^13 anos")
v.igual(round(10 ** 12 / 1e9 / 60), 17, "n^2 com n=10^6: 17 min")
v.igual(round(10 ** 18 / 1e9 / (365.25 * 86400)), 32, "n^3 com n=10^6: 32 anos")
v.igual(round(100 * log2(100)), 664, "n log n com n=100: 664 ns")

# Escada e busca binária
v.igual(sum(range(1, 7)), 21, "1+...+6")
vetor = [2, 5, 8, 12, 15, 16, 19, 21, 23, 25, 27, 30, 34, 40, 41, 47]
a, b, linhas = 1, 16, []
while True:
    m = (a + b) // 2
    linhas.append((a, b, m))
    if vetor[m - 1] == 27:
        break
    if 27 > vetor[m - 1]:
        a = m + 1
    else:
        b = m - 1
v.igual(linhas, [(1, 16, 8), (9, 16, 12), (9, 11, 10), (11, 11, 11)], "busca binária de 27")
v.tem("0/1/16/8,1/9/16/12,2/9/11/10,3/11/11/11", "figura da busca binária")

# Máquina 10 vezes mais rápida
v.tem(f"$\\sqrt{{10}}\\,N\\approx{dec(sqrt(10), 2)}\\,N$", "fator do custo n^2")
v.tem(f"$\\sqrt[3]{{10}}\\,N\\approx{dec(10 ** (1 / 3), 2)}\\,N$", "fator do custo n^3")
v.tem(f"$N+{dec(log2(10), 1)}$", "acréscimo do custo 2^n")
v.tem("passaremos a resolver $3160$", "N=1000 quadrático")
v.tem("passaremos a resolver $43$", "N=40 exponencial")
v.igual(floor(40 + log2(10)), 43, "40 + log2 10")

# Exemplo de 2n^2+1
v.igual(all(2 * n * n + 1 <= 3 * n * n for n in range(1, 10 ** 4)), True, "2n^2+1 <= 3n^2")

# --- Respostas ---
v.tem("$\\sqrt{10}\\approx3{,}16$", "cx-tec", "respostas/01.tex")
v.tem("$n'=n+\\log_210\\approx n+3{,}3$", "cx-tec", "respostas/01.tex")
v.igual(round(log2(3), 3), 1.585, "log2 3 (cx-ordem)")
# cx-def3: 2n^3 <= 3n^3-100n^2+7 <= 4n^3 para n >= 100
g = lambda n: 3 * n ** 3 - 100 * n ** 2 + 7
v.igual(all(2 * n ** 3 <= g(n) <= 4 * n ** 3 for n in range(100, 5000)), True, "cx-def3")
v.igual(2 * 99 ** 3 <= g(99), False, "cx-def3: n0=100 é o primeiro")
# cx-triplo: n(n+1)(n+2)/6
for n in range(1, 30):
    corpo = sum(1 for i in range(1, n + 1) for j in range(i, n + 1) for k in range(i, j + 1))
    v.igual(corpo, n * (n + 1) * (n + 2) // 6, f"cx-triplo, n={n}")
v.tem("(para $n=1$ e $n=2$ dá 1 e 4)", "cx-triplo", "respostas/01.tex")
# cx-binaria
for n, esperado in ((1000, 10), (10 ** 6, 20)):
    v.igual(floor(log2(n)) + 1, esperado, f"cx-binaria, n={n}")
v.tem(f"$\\floor{{{dec(log2(1000), 2)}}}+1=10$", "cx-binaria n=1000", "respostas/01.tex")
v.tem(f"$\\floor{{{dec(log2(10**6), 2)}}}+1=20$", "cx-binaria n=10^6", "respostas/01.tex")
# cx-lacos (a): total < 2n
for n in range(1, 300):
    i, total = 1, 0
    while i <= n:
        total += i
        i *= 2
    v.igual(total < 2 * n, True, f"cx-lacos (a), n={n}")

v.fim()
