#!/usr/bin/env python3
"""Capítulo 6 (ordenação por comparação)."""
from math import ceil, factorial, log, log2

from comum import Verificador, dec, lista

v = Verificador("06_ordenacao_comparacao.tex", "respostas/06.tex")


def mergesort(a, log_intercalacoes, contar=None):
    """Mergesort com meio = floor((ini+fim)/2); registra cada intercalação."""
    if len(a) <= 1:
        return list(a)
    meio = (len(a) + 1) // 2  # tamanho da metade esquerda: ini..floor((ini+fim)/2)
    e = mergesort(a[:meio], log_intercalacoes, contar)
    d = mergesort(a[meio:], log_intercalacoes, contar)
    i = j = comps = 0
    out = []
    while i < len(e) and j < len(d):
        comps += 1
        if e[i] <= d[j]:
            out.append(e[i]); i += 1
        else:
            out.append(d[j]); j += 1
    out += e[i:] + d[j:]
    log_intercalacoes.append((out, comps))
    if contar is not None:
        contar.append(comps)
    return out


def lomuto(a):
    a = list(a)
    x, i, linhas = a[-1], -1, []
    for j in range(len(a) - 1):
        if a[j] < x:
            i += 1
            a[i], a[j] = a[j], a[i]
        linhas.append(list(a))
    a[i + 1], a[-1] = a[-1], a[i + 1]
    return a, i + 2, linhas  # posição 1-indexada


def quicksort_comparacoes(a):
    if len(a) <= 1:
        return 0
    b, q, _ = lomuto(a)
    return len(a) - 1 + quicksort_comparacoes(b[:q - 1]) + quicksort_comparacoes(b[q:])


# Estabilidade (Exemplo 6.1)
turma = [("Ana", 8), ("Bia", 7), ("Caio", 8), ("Davi", 7)]
estavel = sorted(turma, key=lambda p: p[1])
v.igual(estavel, [("Bia", 7), ("Davi", 7), ("Ana", 8), ("Caio", 8)], "ordenação estável por nota")

# Substituição: 3c/4 + 1 <= c  <=>  c >= 4
v.igual(min(c for c in range(1, 10) if 3 * c / 4 + 1 <= c), 4, "constante da substituição")
v.tem(f"$E=\\log_23\\approx{dec(log2(3), 3)}$", "expoente do Karatsuba")
v.tem(f"$E=\\log_43\\approx{dec(log(3, 4), 2)}$", "expoente de 3T(n/4)+n log n")
v.tem(f"\\Theta(n^{{\\log_2 7}})\\approx\\Theta(n^{{{dec(log2(7), 3)}}})", "expoente de Strassen")

# Mergesort de (5,2,4,7,1,3,2,6)
inter = []
res = mergesort([5, 2, 4, 7, 1, 3, 2, 6], inter)
v.igual([x for x, _ in inter], [[2, 5], [4, 7], [2, 4, 5, 7], [1, 3], [2, 6], [1, 2, 3, 6],
                                [1, 2, 2, 3, 4, 5, 6, 7]], "intercalações da Figura 6.4")
v.igual(inter[-1][1], 7, "a última intercalação faz 7 comparações")
v.tem("Foram 7 comparações para 8 elementos", "comparações da última intercalação")

# Lomuto (Exemplo 6.6)
res, q, linhas = lomuto([6, 3, 9, 1, 8, 2, 5])
for k, lin in enumerate(linhas):
    v.tem(f"{k}/{{{','.join(map(str, lin))}}}/", f"Figura da partição de Lomuto, linha {k}")
v.tem(f"6/{{{','.join(map(str, res))}}}/", "Figura da partição de Lomuto, linha final")
v.igual(q, 4, "posição devolvida")
v.tem("$(3,1,2,\\,5,\\,8,9,6)$", "resultado da partição")

# O quicksort não é estável: Ana, Bruno e Carla com a mesma nota
def quicksort_rotulos(a):
    if len(a) <= 1:
        return a
    x, i = a[-1], -1
    for j in range(len(a) - 1):
        if a[j][1] < x[1]:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[-1] = a[-1], a[i + 1]
    return quicksort_rotulos(a[:i + 1]) + [a[i + 1]] + quicksort_rotulos(a[i + 2:])


saida = [n for n, _ in quicksort_rotulos([("Ana", 7), ("Bruno", 7), ("Carla", 7)])]
v.igual(saida, ["Carla", "Ana", "Bruno"], "saída do quicksort com três notas iguais")

# Limite inferior para n = 3, 4
v.igual((ceil(log2(6)), ceil(log2(24))), (3, 5), "limite inferior para n=3 e n=4")
from itertools import permutations
pior4 = 0
for p in permutations(range(4)):
    c = []
    mergesort(list(p), [], c)
    pior4 = max(pior4, sum(c))
v.igual(pior4, 5, "mergesort com 4 elementos faz no máximo 5 comparações")

# --- Respostas ---
def pior_merge(n):
    return 0 if n == 1 else 2 * pior_merge(n // 2) + n - 1


v.igual([pior_merge(n) for n in (2, 4, 8)], [1, 5, 17], "sc-pior8")
v.tem("$W(2)=1$, $W(4)=5$ e $W(8)=17$", "sc-pior8", "respostas/06.tex")
v.igual(all(pior_merge(2 ** k) == 2 ** k * k - 2 ** k + 1 for k in range(12)), True, "sc-pior8: fórmula")
inter = []
mergesort([38, 27, 43, 3, 9, 82, 10], inter)
for x, _ in inter:
    v.tem(lista(x), "sc-mtrace", "respostas/06.tex")
v.igual([x for x, _ in inter], [[27, 38], [3, 43], [3, 27, 38, 43], [9, 82], [9, 10, 82],
                                [3, 9, 10, 27, 38, 43, 82]], "sc-mtrace: ordem das intercalações")
res, q, _ = lomuto([2, 8, 7, 1, 3, 5, 6, 4])
v.tem("Resultado " + lista(res) + ", e a posição devolvida é " + str(q), "sc-lomuto", "respostas/06.tex")
v.igual(all(quicksort_comparacoes(list(range(n))) == n * (n - 1) // 2 for n in range(1, 40)), True,
        "sc-quickpior")
v.igual((ceil(log2(factorial(5))), ceil(log2(factorial(12))), round(log2(factorial(12)), 1)),
        (7, 29, 28.8), "sc-cinco")
v.tem("$\\ceil{\\log_2(12!)}=\\ceil{28{,}8}=29$", "sc-cinco", "respostas/06.tex")
# [2a,2b,1] com pivô 1 (compara só o valor)
a = [(2, "a"), (2, "b"), (1, "")]
x, i = a[-1], -1
for j in range(2):
    if a[j][0] < x[0]:
        i += 1
        a[i], a[j] = a[j], a[i]
a[i + 1], a[-1] = a[-1], a[i + 1]
v.igual(a, [(1, ""), (2, "b"), (2, "a")], "sc-estavel (b): 2a passa para depois de 2b")

v.fim()
