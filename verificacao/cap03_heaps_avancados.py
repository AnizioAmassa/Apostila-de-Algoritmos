#!/usr/bin/env python3
"""Capítulo 3 (heaps binomiais e de Fibonacci, análise amortizada)."""
from math import comb, log2

from comum import Verificador

v = Verificador("03_heaps_avancados.tex", "respostas/03.tex")


# Árvore = (chave, [filhos]); a ordem (grau da raiz) é len(filhos).
def link(a, b):
    """Subordina a árvore de raiz menor à de raiz maior (heap de máximo)."""
    if a[0] < b[0]:
        a, b = b, a
    return (a[0], [b] + a[1])


def tamanho(t):
    return 1 + sum(tamanho(f) for f in t[1])


def fusao(h1, h2):
    """Soma binária das listas de árvores (ordenadas por ordem). Com três árvores
    de mesma ordem, a primeira (o ``vai um'') fica e as outras duas se juntam.
    Devolve a lista resultante e o número de links."""
    por_ordem = {}
    for t in h1 + h2:
        por_ordem.setdefault(len(t[1]), []).append(t)
    res, vai, links, k = [], None, 0, 0
    maior = max(por_ordem) if por_ordem else -1
    while k <= maior or vai is not None:
        grupo = ([vai] if vai is not None else []) + por_ordem.get(k, [])
        vai = None
        if len(grupo) == 1:
            res.append(grupo[0])
        elif len(grupo) == 2:
            vai, links = link(*grupo), links + 1
        elif len(grupo) == 3:
            res.append(grupo[0])
            vai, links = link(grupo[1], grupo[2]), links + 1
        k += 1
    return res, links


def forma(n):
    return [k for k in range(n.bit_length()) if n >> k & 1]


def arvore_binomial(k):
    t = (0, [])
    for _ in range(k):
        t = link(t, (0, [f for f in t[1]]))  # cópia de mesma forma
    return t


def niveis(t, d=0, acc=None):
    acc = {} if acc is None else acc
    acc[d] = acc.get(d, 0) + 1
    for f in t[1]:
        niveis(f, d + 1, acc)
    return acc


# Propriedades de B_k
for k in range(6):
    b = arvore_binomial(k)
    v.igual(tamanho(b), 2 ** k, f"B_{k} tem 2^{k} nós")
    v.igual([niveis(b)[j] for j in range(k + 1)], [comb(k, j) for j in range(k + 1)],
            f"nós por profundidade em B_{k}")

v.igual(forma(13), [0, 2, 3], "13 = 1101_2")
v.igual(forma(26), [1, 3, 4], "26 = 11010_2")
v.tem("$26=11010_2$ dá $H=\\{B_1,B_3,B_4\\}$", "forma com 26 elementos")
arvs = [(12, []), (41, [(33, [(17, [])]), (28, [])]),
        (50, [(44, [(31, [(10, [])]), (25, [])]), (37, [(29, [])]), (6, [])])]
v.igual([tamanho(t) for t in arvs], [1, 4, 8], "tamanhos das árvores da Figura 3.2")
v.igual(max(t[0] for t in arvs), 50, "máximo do heap com 13 elementos")

# Fusão passo a passo (Exemplo 3.3)
H1 = [(7, []), (9, [(3, [])])]
H2 = [(5, []), (8, [(6, [])])]
r, links = fusao(H1, H2)
v.igual(r, [(7, [(5, [])]), (9, [(8, [(6, [])]), (3, [])])], "fusão de H1 e H2")
v.igual(sum(tamanho(t) for t in r), 6, "a fusão tem 6 elementos")

# Fusão de formas {B0,B2,B4} + {B0,B1}
def formas(ordens):
    return [arvore_binomial(k) for k in ordens]
r, links = fusao(formas([0, 2, 4]), formas([0, 1]))
v.igual(([len(t[1]) for t in r], links), ([3, 4], 3), "fusão {B0,B2,B4}+{B0,B1}")
v.tem("$\\{B_3,B_4\\}$, isto é, $24=11000_2=10101_2+11_2$", "resultado da fusão por formas")

# Remoção do máximo (Exemplo 3.4)
h = [(7, [(5, [])]), (9, [(8, [(6, [])]), (3, [])])]
filhos = sorted(h[1][1], key=lambda t: len(t[1]))
r, _ = fusao([h[0]], filhos)
v.igual(r, [(3, []), (8, [(7, [(5, [])]), (6, [])])], "remoção do máximo 9")
v.igual(sum(tamanho(t) for t in r), 5, "sobram 5 = 101_2 elementos")

# Contador binário
custos, total, totais, phi = [], 0, [], []
x = 0
for _ in range(8):
    y = x + 1
    t = bin(x ^ y).count("1")
    custos.append(t)
    total += t
    totais.append(total)
    phi.append(bin(y).count("1"))
    x = y
v.igual(custos, [1, 2, 1, 3, 1, 2, 1, 4], "custos reais do contador")
v.tem("(1, 2, 1, 3, 1, 2, 1, 4)", "custos reais citados no texto")
v.igual(totais, [1, 3, 4, 7, 8, 10, 11, 15], "totais reais")
v.igual(phi, [1, 1, 2, 1, 2, 2, 3, 1], "potencial (bits 1)")
v.tem("na tabela, $15\\le16$", "total de 8 incrementos")

# Pilha com desempilhamento múltiplo
ks = [0, 0, 0, 3, 0]
v.igual(([1 + k for k in ks], sum(1 + k for k in ks), 2 * len(ks)), ([1, 1, 1, 4, 1], 8, 10),
        "pilha com k=0,0,0,3,0")
v.tem("os custos reais são $1,1,1,4,1$, o total é $8$", "pilha com desempilhamento múltiplo")


# Consolidação do heap de Fibonacci (Exemplo 3.5)
def consolida(raizes):
    A, links = {}, 0
    for t in raizes:
        while len(t[1]) in A:
            u = A.pop(len(t[1]))
            t = link(t, u)
            links += 1
        A[len(t[1])] = t
    return [A[g] for g in sorted(A)], links


raizes = [(k, []) for k in (3, 8, 5, 12, 6, 9, 2)]
v.igual(max(r[0] for r in raizes), 12, "o máximo depois das inserções é 12")
resto = [r for r in raizes if r[0] != 12]
final, links = consolida(resto)
v.igual(final, [(9, [(2, [])]), (8, [(6, [(5, [])]), (3, [])])], "árvores depois da consolidação")
v.igual(links, 4, "a consolidação faz 4 links")
v.tem("examinou 6 raízes e fez 4 links, mas terminou com $t=2$", "potencial na consolidação")
v.tem("$\\Delta\\Phi=3-2\\cdot2=-1$, e o custo amortizado é $3+(-1)=2$", "potencial dos cortes")

# Menores árvores de grau k num heap de Fibonacci: F_{k+2}
s = [1, 2]
for k in range(2, 6):
    s.append(1 + 1 + sum(s[i - 2] for i in range(2, k + 1)))
v.igual(s, [1, 2, 3, 5, 8, 13], "menores árvores de grau 0..5")
v.tem("têm $1,2,3,5,8,13$ nós", "menores árvores no texto")

# --- Respostas ---
r, _ = fusao(formas(forma(3)), formas(forma(5)))
v.igual(len(r), 1, "hb-l11: 3 + 5 = 8 dá uma única árvore")
r, links = fusao(formas([0, 2, 4]), formas([0, 1]))
v.tem("$\\{B_3,B_4\\}$, isto é, $24=11000_2$", "hb-m1", "respostas/03.tex")
b2a = (10, [(12, [(13, [])]), (14, [])])  # heap de mínimo: troque o sinal
v.igual(tamanho(link((-10, [(-12, [(-13, [])]), (-14, [])]), (-15, [(-16, [(-17, [])]), (-18, [])]))), 8,
        "hb-r6 (c): o link de duas B_2 tem 8 nós")
v.igual((forma(100), forma(101), forma(104)), ([2, 5, 6], [0, 2, 5, 6], [3, 5, 6]), "hb-forma")
links_ins = []
for n in range(100, 104):
    _, l = fusao(formas(forma(n)), formas([0]))
    links_ins.append(l)
v.igual(links_ins, [0, 1, 0, 3], "hb-forma: links das inserções de 100 a 104")
v.tem("fazem $0,1,0,3$ links", "hb-forma", "respostas/03.tex")
v.igual((2 * 10 ** 6 * 16, 40 * 2 * 10 ** 6, 40 * 2 ** 20), (32_000_000, 80_000_000, 41_943_040),
        "hb-t2: memória")
v.igual(round(32_000_000 / 2 ** 20, 1), 30.5, "hb-t2: 32·10^6 bytes ≈ 30,5 MB")
total = 5e6 + 8e7 + 5e6 * log2(5e6)
v.igual((round(total / 1e8), round(log2(5e6)), round(8e7 * 22 / 1e9)), (2, 22, 2), "hb-t3: estimativas")

v.fim()
