#!/usr/bin/env python3
"""Capítulo 13 (algoritmos gulosos e matroides)."""
import heapq
from itertools import combinations, permutations

from comum import Verificador

v = Verificador("13_gulosos_matroides.tex", "respostas/13.tex")
R = "respostas/13.tex"


def troco_guloso(S, moedas):
    usadas = []
    for m in sorted(moedas, reverse=True):
        q, S = divmod(S, m)
        usadas += [m] * q
    return usadas


def troco_otimo(S, moedas):
    T = [0] + [float("inf")] * S
    for s in range(1, S + 1):
        T[s] = 1 + min(T[s - m] for m in moedas if m <= s)
    return T[S]


def guloso_otimo_ate(moedas, limite):
    return all(len(troco_guloso(S, moedas)) == troco_otimo(S, moedas) for S in range(1, limite))


def eh_floresta(arestas, n_vertices=None):
    pai = {}

    def f(x):
        pai.setdefault(x, x)
        while pai[x] != x:
            x = pai[x]
        return x
    for a, b in arestas:
        ra, rb = f(a), f(b)
        if ra == rb:
            return False
        pai[ra] = rb
    return True


def componentes(vertices, arestas):
    pai = {x: x for x in vertices}

    def f(x):
        while pai[x] != x:
            x = pai[x]
        return x
    for a, b in arestas:
        pai[f(a)] = f(b)
    return len({f(x) for x in vertices})


# Troco
g = troco_guloso(38, [10, 5, 2, 1])
v.igual((g, len(g)), ([10, 10, 10, 5, 2, 1], 6), "troco guloso de 38")
restos, s = [], 38
for m in g:
    s -= m
    restos.append(s)
v.tem(",".join(f"{p}/{m}/{r}" for p, m, r in zip(["0", "1.2", "2.4", "3.6", "4.8", "6"], g, restos)),
      "figura do troco de 38")
v.igual(guloso_otimo_ate([10, 5, 2, 1], 500), True, "guloso ótimo para {10,5,2,1}")
v.igual((len(troco_guloso(6, [4, 3, 1])), troco_otimo(6, [4, 3, 1])), (3, 2), "{4,3,1} com S=6")
v.igual((len(troco_guloso(30, [25, 10, 1])), troco_otimo(30, [25, 10, 1])), (6, 3), "{25,10,1} com S=30")
v.tem("Com $\\{25,10,1\\}$ e $S=30$, ele usa 6 moedas", "{25,10,1} no texto")

# Matroide pequena (Exemplo 13.3)
E = {"a": (1, 2), "b": (2, 3), "c": (1, 3), "d": (3, 4)}
indep = [set(c) for k in range(5) for c in combinations("abcd", k) if eh_floresta([E[x] for x in c])]
v.igual(len(indep), 14, "14 independentes na matroide gráfica")
bases = sorted("".join(sorted(I)) for I in indep if len(I) == 3)
v.igual(bases, ["abd", "acd", "bcd"], "bases")
vet = {"a": (1, 0, 0), "b": (0, 1, 0), "c": (1, 1, 0), "d": (0, 0, 1)}


def posto(vs):
    m = [list(x) for x in vs]
    r = 0
    for col in range(3):
        piv = next((i for i in range(r, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][col]:
                fat = m[i][col] / m[r][col]
                m[i] = [x - fat * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


indep_lin = [set(c) for k in range(5) for c in combinations("abcd", k) if posto([vet[x] for x in c]) == k]
v.igual(sorted(map(sorted, indep_lin)), sorted(map(sorted, indep)), "a matroide linear é a mesma")

# Axioma de aumento (Figura 13.3)
V5 = range(1, 6)
v.igual((componentes(V5, [(1, 2), (3, 4)]), componentes(V5, [(1, 3), (3, 5), (2, 4)])), (3, 2),
        "componentes de I1 e I2")
v.igual(eh_floresta([(1, 2), (3, 4), (3, 5)]), True, "I1 + 35 continua sem ciclo")

# Guloso na matroide gráfica (Exemplo 13.6)
G = {"AB": 7, "AC": 5, "BC": 8, "BD": 6, "CD": 9, "CE": 4, "DE": 3}
aceitas, rejeitadas = [], []
for e in sorted(G, key=lambda e: -G[e]):
    (aceitas if eh_floresta([tuple(x) for x in aceitas + [e]]) else rejeitadas).append(e)
v.igual((aceitas, rejeitadas), (["CD", "BC", "AB", "CE"], ["BD", "AC", "DE"]), "aceitas e rejeitadas")
melhor = max(sum(G[e] for e in T) for T in combinations(G, 4) if eh_floresta([tuple(e) for e in T]))
v.igual((sum(G[e] for e in aceitas), melhor), (28, 28), "árvore geradora de peso máximo")
v.tem("$9+8+7+4=28$", "peso da árvore máxima no texto")
v.igual(all((k + 1) ** 2 > k * (k + 2) for k in range(100)), True, "recíproca: (k+1)^2 > k(k+2)")

# --- Respostas ---
s = (1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12)
f = (4, 5, 6, 7, 9, 9, 10, 11, 12, 14, 16)
escolhidas, fim = [], -1
for i in sorted(range(11), key=lambda i: f[i]):
    if s[i] >= fim:
        escolhidas.append(i + 1)
        fim = f[i]
v.igual(escolhidas, [1, 4, 8, 11], "gm-ativ")
maximo = max(k for k in range(1, 12) for c in combinations(range(11), k)
             if all(f[a] <= s[b] or f[b] <= s[a] for a, b in combinations(c, 2)))
v.igual(maximo, 4, "gm-ativ: 4 é o máximo")
v.tem("as atividades $1,4,8,11$", "gm-ativ", R)
itens = [(10, 60), (20, 100), (30, 120)]
W, val = 50, 0
for p, vv in sorted(itens, key=lambda t: -t[1] / t[0]):
    leva = min(p, W)
    val += vv * leva / p
    W -= leva
v.igual(val, 240, "gm-frac")
d = (4, 2, 4, 3, 1, 4, 6)
w = (70, 60, 50, 40, 30, 20, 10)


def escalonavel(c):
    return all(sum(1 for i in c if d[i] <= t) <= t for t in range(1, 8))


aceitas = []
for i in sorted(range(7), key=lambda i: -w[i]):
    if escalonavel(aceitas + [i]):
        aceitas.append(i)
multa = sum(w[i] for i in range(7) if i not in aceitas)
v.igual((sorted(i + 1 for i in aceitas), multa), ([1, 2, 3, 4, 7], 50), "gm-tarefas")
v.igual([i + 1 for i in sorted(aceitas, key=lambda i: (d[i], i))], [2, 4, 1, 3, 7], "gm-tarefas: ordem")
freq = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}
h = [(fr, k) for k, fr in freq.items()]
heapq.heapify(h)
custo = 0
while len(h) > 1:
    a, ka = heapq.heappop(h)
    b, kb = heapq.heappop(h)
    custo += a + b
    heapq.heappush(h, (a + b, ka + kb))
v.igual(custo, 224, "gm-huffman: custo")
codigo = {"a": "0", "c": "100", "b": "101", "f": "1100", "e": "1101", "d": "111"}
v.igual(sum(freq[k] * len(c) for k, c in codigo.items()), 224, "gm-huffman: código da resposta")
v.igual(all(not a.startswith(b) for a, b in permutations(codigo.values(), 2)), True, "código livre de prefixo")


def soma_terminos(dur):
    t = tot = 0
    for x in dur:
        t += x
        tot += t
    return tot


v.igual((soma_terminos([1, 2, 3]), soma_terminos([3, 2, 1])), (10, 14), "gm-spt")
v.igual(min(soma_terminos(p) for p in permutations([3, 1, 2])), 10, "gm-spt: ordem crescente é ótima")
v.igual(componentes(range(6), [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5)]), 2, "gm-posto: 2 componentes")
cats = {"A": [9, 7, 4], "B": [8, 3], "C": [6, 5, 2]}
v.igual(sum(sum(sorted(x, reverse=True)[:2]) for x in cats.values()), 38, "gm-unifgul")
v.igual((len(troco_guloso(14, [1, 7, 10])), troco_otimo(14, [1, 7, 10])), (5, 2), "gm-moedas: S=14")
v.igual(guloso_otimo_ate([1, 5, 10, 25], 1000), True, "gm-moedas: {1,5,10,25}")

v.fim()
