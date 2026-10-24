#!/usr/bin/env python3
"""Capítulo 2 (heaps binários): exemplos e respostas de simulação."""
from itertools import permutations
from math import comb, floor, log2

from comum import Verificador, lista

v = Verificador("02_heaps.tex", "respostas/02.tex")


# --- heap de máximo em vetor indexado a partir de 1 (posição 0 ignorada) ---
def eh_heap(s):
    return all(s[i - 1] <= s[i // 2 - 1] for i in range(2, len(s) + 1))


def subir(t, i, trocas):
    while i > 1 and t[i] > t[i // 2]:
        t[i], t[i // 2] = t[i // 2], t[i]
        trocas.append((t[i], t[i // 2]))
        i //= 2


def descer(t, i, n, trocas):
    while 2 * i <= n:
        j = 2 * i
        if j < n and t[j + 1] > t[j]:
            j += 1
        if t[i] < t[j]:
            trocas.append((t[i], t[j]))
            t[i], t[j] = t[j], t[i]
            i = j
        else:
            break


def vet(t):
    return t[1:]


def inserir(h, x):
    t = [None] + list(h) + [x]
    tr = []
    subir(t, len(t) - 1, tr)
    return vet(t), tr


def remover(h):
    t = [None] + list(h)
    t[1] = t[-1]
    t.pop()
    tr = []
    descer(t, 1, len(t) - 1, tr)
    return vet(t), tr


def alterar(h, i, p):
    t = [None] + list(h)
    antiga, t[i] = t[i], p
    tr = []
    if p > antiga:
        subir(t, i, tr)
    else:
        descer(t, i, len(t) - 1, tr)
    return vet(t), tr


def arranjar(s):
    t = [None] + list(s)
    n = len(s)
    passos = []
    for i in range(n // 2, 0, -1):
        tr = []
        descer(t, i, n, tr)
        passos.append((i, tr, vet(t)))
    return vet(t), passos


def heapsort(s):
    h, _ = arranjar(s)
    t = [None] + h
    linhas = []
    for m in range(len(s), 1, -1):
        t[1], t[m] = t[m], t[1]
        descer(t, 1, m - 1, [])
        linhas.append(vet(t))
    return h, linhas


def num_heaps(n):
    if n <= 1:
        return 1
    h = floor(log2(n))
    u = n - (2 ** h - 1)
    L = (2 ** (h - 1) - 1) + min(u, 2 ** (h - 1))
    return comb(n - 1, L) * num_heaps(L) * num_heaps(n - 1 - L)


# --- Texto do capítulo ---
H = [95, 60, 78, 39, 28, 66, 70, 33]
v.igual(eh_heap(H), True, "o vetor da Figura 2.1 é heap")
v.tem(r"o caminho da raiz até a posição 8 é $95\ge60\ge39\ge33$", "caminho até a posição 8")
v.igual([H[i - 1] for i in (1, 2, 4, 8)], [95, 60, 39, 33], "caminho até a posição 8")
v.igual(H[4:], [28, 66, 70, 33], "valores das folhas 5..8")
v.tem("com valores $28,66,70,33$, e o mínimo, $28$", "folhas e mínimo")
ordem = sorted(H, reverse=True)
v.igual((ordem[1], H.index(ordem[1]) + 1, ordem[2], H.index(ordem[2]) + 1), (78, 3, 70, 7),
        "segundo e terceiro maiores e suas posições")

v.igual(eh_heap([9, 7, 8, 3, 5, 6]), True, "[9,7,8,3,5,6] é heap")
v.igual(eh_heap([9, 5, 8, 6, 4, 7]), False, "[9,5,8,6,4,7] não é heap")
n = 10
v.igual((7 // 2, (8, 9), list(range(n // 2 + 1, n + 1)), floor(log2(9)) + 1, floor(log2(10)) + 1),
        (3, (8, 9), [6, 7, 8, 9, 10], 4, 4), "contas com índices, n=10")

r, tr = inserir(H, 73)
v.tem(lista(r), "inserção de 73 (Exemplo 2.6)")
v.igual(len(tr), 2, "a inserção de 73 faz duas trocas")
r, tr = remover(H)
v.tem("[33,60,78,39,28,66,70]", "33 vai para a raiz")
v.tem(lista(r), "remoção do máximo (Exemplo 2.7)")
r, _ = alterar(H, 6, 98)
v.tem(lista(r), "aumento de 66 para 98")
r, _ = alterar(H, 1, 37)
v.tem(lista(r), "diminuição de 95 para 37")

final, passos = arranjar([7, 2, 15, 9, 1, 20, 13])
for i, tr, vetor in passos:
    v.tem(lista(vetor), f"arranjar de [7,2,15,9,1,20,13], i={i}")
v.tem(r"$4\cdot1+2\cdot2+1\cdot3=11$", "trocas máximas do arranjar com 15 nós")

for ent in ([18, 25, 41, 34, 14, 10, 52, 50, 48], [20, 15, 30, 40, 10, 25, 5]):
    final, passos = arranjar(ent)
    v.tem("Resultado: " + lista(final), f"construção de {ent}")
v.tem(lista(sorted([18, 25, 41, 34, 14, 10, 52, 50, 48])), "heapsort do vetor de 9 elementos")

h, linhas = heapsort([5, 2, 9, 4, 7])
v.tem("o heap é " + lista(h), "heap inicial do heapsort de [5,2,9,4,7]")
for lin in linhas:
    v.igual(lin in ([7, 4, 5, 2, 9], [5, 4, 2, 7, 9], [4, 2, 5, 7, 9], [2, 4, 5, 7, 9]), True,
            f"linha {lin} da Figura do heapsort")
v.tem(r"0/{9,7,5,4,2}/5", "Figura do heapsort, heap inicial")
for k, lin in enumerate(linhas, 1):
    v.tem(f"{k}/{{{','.join(map(str, lin))}}}/", f"Figura do heapsort, linha {k}")

v.tem(r"$\floor{\log_2 10^6}+1=20$", "níveis de um heap com um milhão de elementos")
v.igual(floor(log2(10 ** 6)) + 1, 20, "níveis de um heap com 10^6 elementos")

S = [10, 9, 1, 8, 7, 0, 0, 6]
T = S[:]
T[2], T[3] = T[3], T[2]
v.igual((eh_heap(S), eh_heap(T)), (True, False), "contraexemplo da troca s3<s4")
v.tem(lista(T), "vetor depois da troca")

valores = [num_heaps(k) for k in range(1, 11)]
v.tem(",".join(map(str, valores)), "número de heaps para n=1..10")
for k in range(1, 9):  # força bruta confirma a fórmula
    bruto = sum(eh_heap(p) for p in permutations(range(1, k + 1)))
    v.igual(bruto, valores[k - 1], f"número de heaps com {k} elementos (força bruta)")
heaps4 = sorted(p for p in permutations(range(1, 5)) if eh_heap(p))
v.igual(heaps4, [(4, 2, 3, 1), (4, 3, 1, 2), (4, 3, 2, 1)], "os três heaps de {1,2,3,4}")

# --- Respostas ---
a = [33, 32, 28, 31, 26, 29, 25, 30, 27]
b = [33, 32, 28, 31, 29, 26, 25, 30, 27]
v.igual((eh_heap(a), eh_heap(b)), (False, True), "hp-l1")
v.tem("a posição 6 ($29$) tem pai na posição 3 ($28$)", "hp-l1 (a)")
final, passos = arranjar([18, 25, 41, 34, 14, 10, 52, 50, 48])
trocas = [tr for _, tr, _ in passos]
v.igual(trocas, [[(34, 50)], [(41, 52)], [(25, 50), (25, 48)], [(18, 52), (18, 41)]], "hp-l5: trocas")
v.tem(lista(final), "hp-l5", "respostas/02.tex")
r, _ = alterar(H, 6, 98)
v.tem(lista(r), "hp-r2 (a)", "respostas/02.tex")
r, _ = remover(H)
v.tem(lista(r), "hp-r2 (b)", "respostas/02.tex")
for ent in ([20, 15, 30, 40, 10, 25, 5], [7, 2, 15, 9, 1, 20, 13]):
    final, _ = arranjar(ent)
    v.tem(lista(final), f"hp-r2 ({ent})", "respostas/02.tex")

h, vetores = [], []
for x in (15, 40, 25, 50, 10, 45):
    h, _ = inserir(h, x)
    vetores.append(lista(h))
v.tem(";".join(vetores[:3]), "hp-ins, três primeiras inserções", "respostas/02.tex")
for vetor in vetores[3:]:
    v.tem(vetor, "hp-ins", "respostas/02.tex")
h1, _ = remover([90, 70, 80, 30, 60, 50, 40, 10, 20])
h2, _ = remover(h1)
v.tem(lista(h1), "hp-rem2, primeira remoção", "respostas/02.tex")
v.tem(lista(h2), "hp-rem2, segunda remoção", "respostas/02.tex")
h, linhas = heapsort([4, 10, 3, 5, 1])
v.tem("Após o \\emph{arranjar}: " + lista(h), "hp-sort5, arranjar", "respostas/02.tex")
partes = []
for k, lin in enumerate(linhas):
    m = len(lin) - 1 - k
    partes.append("[" + ",".join(map(str, lin[:m])) + "|" + ",".join(map(str, lin[m:])) + "]")
v.tem(",".join(partes), "hp-sort5, passos do laço", "respostas/02.tex")

# hp-estavel: [1, 2a, 2b] sai com 2b antes de 2a
t = [None, (1, ""), (2, "a"), (2, "b")]
chave = lambda x: x[0]
# arranjar com comparação só pela chave
def descer_chave(t, i, n):
    while 2 * i <= n:
        j = 2 * i
        if j < n and chave(t[j + 1]) > chave(t[j]):
            j += 1
        if chave(t[i]) < chave(t[j]):
            t[i], t[j] = t[j], t[i]
            i = j
        else:
            break
descer_chave(t, 1, 3)
for m in (3, 2):
    t[1], t[m] = t[m], t[1]
    descer_chave(t, 1, m - 1)
v.igual(t[1:], [(1, ""), (2, "b"), (2, "a")], "hp-estavel: saída [1, 2b, 2a]")

v.fim()
