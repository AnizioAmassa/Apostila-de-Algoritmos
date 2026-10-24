#!/usr/bin/env python3
"""Capítulo 4 (Union-Find)."""
from math import floor, log2

from comum import Verificador, lista

v = Verificador("04_unionfind.tex", "respostas/04.tex")


class Floresta:
    """União por rank (no empate, a raiz do primeiro argumento vence) e
    compressão de caminhos opcional."""

    def __init__(self, elementos, comprime=True):
        self.pai = {x: x for x in elementos}
        self.rank = {x: 0 for x in elementos}
        self.comprime = comprime

    def find(self, x):
        caminho = []
        while self.pai[x] != x:
            caminho.append(x)
            x = self.pai[x]
        if self.comprime:
            for y in caminho:
                self.pai[y] = x
        return x

    def union(self, x, y):
        r, s = self.find(x), self.find(y)
        if r == s:
            return False
        if self.rank[r] < self.rank[s]:
            self.pai[r] = s
        elif self.rank[r] > self.rank[s]:
            self.pai[s] = r
        else:
            self.pai[s] = r
            self.rank[r] += 1
        return True

    def conjuntos(self):
        grupos = {}
        for x in self.pai:
            grupos.setdefault(self.find(x), set()).add(x)
        return sorted(sorted(g) for g in grupos.values())


# Exemplo 4.1: a rede de computadores
f = Floresta(range(1, 8))
for a, b in [(1, 2), (3, 4), (2, 4), (5, 6)]:
    f.union(a, b)
v.igual(f.conjuntos(), [[1, 2, 3, 4], [5, 6], [7]], "partição depois dos quatro cabos")
v.igual(f.union(1, 3), False, "o cabo 1-3 não muda nada")

# Vetor de representantes
rep = [1, 1, 1, 1, 5, 5, 7]
novo = [1 if r == 5 else r for r in rep]
v.tem("\\vetor{1,1,1,1,5,5,7}", "vetor rep antes")
v.tem("\\vetor[5,6]{" + ",".join(map(str, novo)) + "}", "vetor rep depois de Union(1,6)")

# A sequência ruim com listas e união ponderada
v.igual(sum(range(1, 5)), 10, "uniões ruins com n=5")
v.igual(floor(log2(1000)), 9, "com n=1000, no máximo 9 mudanças / altura 9")

# Logaritmo iterado
x, passos, valores = 1000.0, 0, []
while x > 1:
    x = log2(x)
    valores.append(round(x, 2))
    passos += 1
v.igual(passos, 4, "lg* 1000")
v.tem("$1000\\to9{,}97\\to3{,}32\\to1{,}73\\to0{,}79$", "sequência de logaritmos de 1000")
v.igual(valores, [9.97, 3.32, 1.73, 0.79], "valores da sequência")
F = [1, 2, 4, 16, 65536, 2 ** 65536]  # F(k) = 2^F(k-1)


def lgs(n):
    return next(k for k, fk in enumerate(F) if fk >= n)


v.igual([lgs(n) for n in (1, 2, 3, 4, 5, 16, 17, 65536, 65537)], [0, 1, 2, 2, 3, 3, 4, 4, 5],
        "tabela de lg*")
v.igual(round(log2(10 ** 80)), 266, "10^80 ≈ 2^266")


def grupo(r):
    return 0 if r <= 1 else next(b for b in range(1, len(F)) if F[b - 1] < r <= F[b])


ranks = [0, 1, 3, 4, 7, 12, 20]
v.igual([grupo(r) for r in ranks], [0, 0, 2, 2, 3, 3, 4], "grupos dos ranks")
v.tem("Os grupos são $0,0,2,2,3,3,4$", "grupos no texto")

# Solução offline de trás para frente
f = Floresta(range(1, 5))
resp = [4]
for a, b in [(3, 4), (2, 3), (1, 2)]:
    f.union(a, b)
    resp.append(len(f.conjuntos()))
v.igual(resp[::-1][1:], [2, 3, 4], "componentes depois de cada destruição")
v.tem("são $2$, $3$ e $4$ componentes", "respostas do exemplo offline")

# Exemplo 4.2: uniões por rank
f = Floresta("ABCDEF")
for a, b in ["AB", "CD", "AC", "EF"]:
    f.union(a, b)
v.igual((f.rank["A"], f.rank["C"], f.rank["E"], f.pai["C"], f.pai["D"]), (2, 1, 1, "A", "C"),
        "uniões por rank do Exemplo 4.2")
v.igual(f.conjuntos(), [list("ABCD"), list("EF")], "dois conjuntos ao final")

# --- Respostas ---
f = Floresta(range(1, 9))
for a, b in [(1, 2), (3, 4), (5, 6), (7, 8), (1, 3), (5, 7), (1, 5)]:
    f.union(a, b)
antes = [f.pai[i] for i in range(1, 9)]
v.tem("é $" + ",".join(map(str, antes)) + "$", "uf-sim: pai antes do Find", "respostas/04.tex")
f.find(8)
depois = [f.pai[i] for i in range(1, 9)]
v.tem("$pai=" + ",".join(map(str, depois)) + "$", "uf-sim: pai depois do Find", "respostas/04.tex")
v.igual((f.rank[1], f.rank[5], f.rank[3], f.rank[7]), (3, 2, 1, 1), "uf-sim: ranks")


def listas_ponderadas(rodadas):
    """Número de atualizações de ponteiro unindo listas aos pares."""
    tamanhos, total = rodadas, 0
    while len(tamanhos) > 1:
        novos = []
        for i in range(0, len(tamanhos), 2):
            a, b = tamanhos[i], tamanhos[i + 1]
            total += min(a, b)
            novos.append(a + b)
        tamanhos = novos
    return total


v.igual(listas_ponderadas([1] * 8), 12, "uf-listas com n=8")
v.igual(all(listas_ponderadas([1] * 2 ** k) == 2 ** k // 2 * k for k in range(1, 11)), True,
        "uf-listas: (n/2) log2 n")
v.igual([lgs(n) for n in (2, 16, 65536, 2 ** 65536, 10 ** 80)], [1, 3, 4, 5, 5], "uf-logstar")

f = Floresta(range(1, 11))
efetivas, ciclos = [], []
for e in ["12", "34", "23", "56", "78", "89", "65", "97"]:
    (efetivas if f.union(int(e[0]), int(e[1])) else ciclos).append(e)
v.igual((efetivas, ciclos, len(f.conjuntos())),
        (["12", "34", "23", "56", "78", "89"], ["65", "97"], 4), "uf-comp")
v.tem("ou seja, $10-6=4$ componentes", "uf-comp", "respostas/04.tex")

f = Floresta("abcdef")
for a, b in ["ab", "cd", "bc", "ef"]:
    f.union(a, b)
v.igual(f.conjuntos(), [list("abcd"), list("ef")], "uf-equiv")
v.igual(round(log2(10 ** 7)), 23, "uf-t4: log2 10^7 ≈ 23")

v.fim()
