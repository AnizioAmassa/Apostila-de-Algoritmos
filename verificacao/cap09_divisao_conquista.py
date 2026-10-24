#!/usr/bin/env python3
"""Capítulo 9 (divisão e conquista)."""
from comum import Verificador

v = Verificador("09_divisao_conquista.tex", "respostas/09.tex")


def inversoes(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def conta_dc(a, log):
    """Contagem por divisão e conquista; registra as inversões cruzadas de cada
    intercalação (de baixo para cima, da esquerda para a direita)."""
    if len(a) <= 1:
        return list(a), 0
    m = (len(a) + 1) // 2
    e, x = conta_dc(a[:m], log)
    d, y = conta_dc(a[m:], log)
    i = j = c = 0
    out = []
    while i < len(e) and j < len(d):
        if e[i] <= d[j]:
            out.append(e[i]); i += 1
        else:
            out.append(d[j]); j += 1
            c += len(e) - i
    out += e[i:] + d[j:]
    log.append((len(a), c))
    return out, x + y + c


def max_sub(a):
    melhor = (a[0], 1, 1)
    for i in range(len(a)):
        s = 0
        for j in range(i, len(a)):
            s += a[j]
            if s > melhor[0]:
                melhor = (s, i + 1, j + 1)
    return melhor


v.igual(inversoes([4, 1, 3, 2]), 4, "(4,1,3,2)")
v.igual(inversoes([2, 1, 4, 5, 3]), 3, "filmes (2,1,4,5,3)")
_, c = conta_dc([2, 5, 8, 1, 3, 9], [])
v.igual(c - inversoes([2, 5, 8]) - inversoes([1, 3, 9]), 5, "inversões cruzadas de (2,5,8) e (1,3,9)")
v.tem("O total é $3+2=5$", "inversões cruzadas no texto")
v.igual(inversoes([1, 5, 4, 8, 10, 2, 6, 9, 12, 11, 3, 7]), 22, "sequência de 12 elementos")
v.tem("tem \\textbf{22} inversões", "22 inversões no texto")
log = []
_, total = conta_dc([6, 2, 8, 4, 1, 7, 3, 5], log)
v.igual(([c for _, c in log], total), ([1, 1, 1, 0, 0, 2, 10], 15), "recursão completa")
v.tem("$1+1+0+0+1+2+10=15$", "total da recursão")

A = [1, -4, 3, -2, 5, -1, -6, 2]
suf = [sum(A[i:4]) for i in range(3, -1, -1)]
pre = [sum(A[4:j + 1]) for j in range(4, 8)]
v.igual((suf, pre), ([-2, 1, -3, -2], [5, 4, -2, 0]), "sufixos e prefixos do subvetor cruzado")
v.igual((max_sub(A[:4])[0], max_sub(A[4:])[0], max_sub(A)), (3, 5, (6, 3, 5)), "subvetor máximo de A")
v.igual(max_sub([-8, -3, -6, -2, -5, -4])[0], -2, "todos negativos")
v.igual(max_sub([-2, 1, -3, 4, -1, 2, 1, -5, 4]), (6, 4, 7), "[-2,1,-3,4,-1,2,1,-5,4]")

# Strassen com números
a11, a12, a21, a22, b11, b12, b21, b22 = 1, 2, 3, 4, 5, 6, 7, 8
M = [(a11 + a22) * (b11 + b22), (a21 + a22) * b11, a11 * (b12 - b22), a22 * (b21 - b11),
     (a11 + a12) * b22, (a21 - a11) * (b11 + b12), (a12 - a22) * (b21 + b22)]
v.igual(M, [65, 35, -2, 8, 24, 22, -30], "M1..M7")
C = [M[0] + M[3] - M[4] + M[6], M[2] + M[4], M[1] + M[3], M[0] - M[1] + M[2] + M[5]]
v.igual(C, [19, 22, 43, 50], "C pelo Strassen")
v.igual(C, [a11 * b11 + a12 * b21, a11 * b12 + a12 * b22, a21 * b11 + a22 * b21, a21 * b12 + a22 * b22],
        "C pelo produto direto")
v.tem("$C_{11}=65+8-24-30=19$, $C_{12}=-2+24=22$, $C_{21}=35+8=43$ e $C_{22}=65-35-2+22=50$",
      "combinação de Strassen")
v.igual((round(8 ** 10 / 1e9, 2), round(7 ** 10 / 1e8, 1)), (1.07, 2.8), "8^10 e 7^10")

# Busca binária, potência e máximo e mínimo
V = [3, 8, 12, 17, 21, 30, 34, 41, 50]
ini, fim, comps = 1, 9, []
while True:
    m = (ini + fim) // 2
    comps.append(m)
    if V[m - 1] == 34:
        break
    ini, fim = (m + 1, fim) if 34 > V[m - 1] else (ini, m - 1)
v.igual(comps, [5, 7], "busca binária por 34")


def pot(a, n, cont):
    if n == 0:
        return 1
    t = pot(a, n // 2, cont)
    cont[0] += 1 if n % 2 == 0 else 2
    return t * t if n % 2 == 0 else t * t * a


cont = [0]
v.igual((pot(2, 10, cont), cont[0]), (1024, 6), "2^10 com 6 multiplicações")


def maxmin(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    m = (n + 1) // 2
    return maxmin(m) + maxmin(n - m) + 2


v.igual(maxmin(6), 8, "máximo e mínimo de 6 elementos")
v.tem("o total é $3+3+2=8$ comparações", "máximo e mínimo no texto")


def maj(a):
    if len(a) == 1:
        return a[0]
    m = (len(a) + 1) // 2
    for c in (maj(a[:m]), maj(a[m:])):
        if c is not None and a.count(c) > len(a) / 2:
            return c
    return None


V = [3, 1, 3, 3, 2, 3, 1, 3]
v.igual((maj(V), V.count(3), maj(V[:4]), maj(V[4:]), maj([3, 1])), (3, 5, 3, None, None),
        "elemento majoritário")

# --- Respostas ---
v.igual((inversoes([2, 4, 1, 3, 5]), inversoes([5, 4, 3, 2, 1]), inversoes([3, 1, 4, 1, 5, 9, 2, 6])),
        (3, 10, 8), "dc-contar")
v.igual([maxmin(n) for n in (2, 4, 8, 16)], [1, 4, 10, 22], "dc-maxmin")
v.tem("Os valores são $1,4,10,22$ para $n=2,4,8,16$", "dc-maxmin", "respostas/09.tex")
cont = [0]
pot(3, 13, cont)
v.igual(cont[0], 7, "dc-pot: 7 multiplicações para n=13")
v.igual(max_sub([5, 15, -30, 10, -5, 40, 10]), (55, 4, 7), "Kadane em 5,15,-30,10,-5,40,10 (pd-apa)")

v.fim()
