#!/usr/bin/env python3
"""Capítulo 18 (busca em profundidade em digrafos, CFC e ordenação topológica)."""
from collections import deque
from itertools import permutations

from comum import Verificador

v = Verificador("18_profundidade_digrafos.tex", "respostas/18.tex")
R = "respostas/18.tex"


def digrafo(arestas, vertices=None):
    g = {x: [] for x in (vertices or [])}
    for a, b in arestas:
        g.setdefault(a, []).append(b)
        g.setdefault(b, [])
    return {x: sorted(n) for x, n in g.items()}


def busca(g, raizes):
    PE = {x: 0 for x in g}
    PS = {x: 0 for x in g}
    old, tipo, Q, cfcs, fortes = {}, {}, [], [], []
    t = [0]

    def P(x):
        t[0] += 1
        PE[x] = old[x] = t[0]
        Q.append(x)
        for w in g[x]:
            if PE[w] == 0:
                tipo[x, w] = "árvore"
                P(w)
                old[x] = min(old[x], old[w])
            elif PS[w] == 0:
                tipo[x, w] = "retorno"
                old[x] = min(old[x], PE[w])
            elif PE[x] < PE[w]:
                tipo[x, w] = "avanço"
            else:
                tipo[x, w] = "cruzamento"
                if w in Q:
                    old[x] = min(old[x], PE[w])
        t[0] += 1
        PS[x] = t[0]
        if old[x] == PE[x]:
            fortes.append((x, PS[x], list(Q)))
            comp = []
            while True:
                y = Q.pop()
                comp.append(y)
                if y == x:
                    break
            cfcs.append(sorted(comp))

    for r in raizes:
        if PE[r] == 0:
            P(r)
    return dict(PE=PE, PS=PS, old=old, tipo=tipo, cfcs=cfcs, fortes=fortes)


def de_tipo(r, t):
    return sorted("".join(map(str, e)) for e, k in r["tipo"].items() if k == t)


def topo(r):
    return sorted(r["PS"], key=lambda x: -r["PS"][x])


def kahn(g, chave=None):
    grau = {x: 0 for x in g}
    for x in g:
        for w in g[x]:
            grau[w] += 1
    fila = [x for x in sorted(g) if grau[x] == 0]
    ordem = []
    while fila:
        if chave:
            fila.sort(key=chave)
        x = fila.pop(0)
        ordem.append(x)
        for w in g[x]:
            grau[w] -= 1
            if grau[w] == 0:
                fila.append(w)
    return ordem


G = digrafo(["ab", "bc", "be", "bf", "cd", "cg", "dc", "dh", "ea", "ef", "fg", "gf", "gh"])
r = busca(G, "abcdefgh")
for x in "abcdefgh":
    v.tem(f"of {x}] {{{r['PE'][x]}/{r['PS'][x]}}}", f"PE/PS de {x}")
v.igual((de_tipo(r, "árvore"), de_tipo(r, "retorno"), de_tipo(r, "avanço"), de_tipo(r, "cruzamento")),
        (["ab", "bc", "be", "cd", "cg", "dh", "gf"], ["dc", "ea", "fg"], ["bf"], ["ef", "gh"]),
        "os quatro tipos de aresta")
v.igual({x: r["old"][x] for x in "abcdefgh"}, dict(a=1, b=1, e=1, c=3, d=3, g=8, f=8, h=5), "valores de old")
v.igual(r["cfcs"], [["h"], ["f", "g"], ["c", "d"], ["a", "b", "e"]], "componentes fortemente conexas")
for x, ps, q in r["fortes"]:
    v.tem(f"{ps} & ${x}$ & ${','.join(q)}$", f"tabela da pilha Q: {x}")
H = digrafo([(1, 2), (1, 3), (2, 4), (3, 4)])
v.igual(de_tipo(busca(H, [1]), "retorno"), [], "1→2, 1→3, 2→4, 3→4 é acíclico")
v.igual(de_tipo(busca(H, [1]), "cruzamento"), ["34"], "3→4 é de cruzamento")

T = digrafo(["ac", "ad", "dc", "bc", "eb", "ef", "eg", "fg", "hf", "ih", "ij", "jh", "jg"])
r = busca(T, "abcdefghij")
ordem = topo(r)
v.igual(ordem, list("ijhefgbadc"), "ordem topológica com raízes em ordem alfabética")
v.tem("{" + ",".join(f"{x}/{r['PS'][x]}" for x in ordem) + "}", "figura da ordem topológica com os PS")
v.igual(topo(busca(T, "icbeda")), list("adebcijhfg"), "ordem com raízes i,c,b,e,d,a")
v.igual(kahn(T), list("aeidbjchfg"), "algoritmo de Kahn")
for o in (list("ijhefgbadc"), list("adebcijhfg"), list("aeidbjchfg")):
    pos = {x: k for k, x in enumerate(o)}
    v.igual(all(pos[a] < pos[b] for a in T for b in T[a]), True, f"{''.join(o)} é topológica")

# --- Respostas ---
S = digrafo([(1, 2), (1, 3), (2, 3), (2, 4), (3, 1), (4, 5), (5, 6), (6, 4), (7, 3), (7, 6)])
r = busca(S, range(1, 8))
v.igual(([r["PE"][i] for i in range(1, 8)], [r["PS"][i] for i in range(1, 8)]),
        ([1, 2, 3, 5, 6, 7, 13], [12, 11, 4, 10, 9, 8, 14]), "dd-sim: PE e PS")
v.igual((de_tipo(r, "retorno"), de_tipo(r, "avanço"), de_tipo(r, "cruzamento")),
        (["31", "64"], ["13"], ["73", "76"]), "dd-sim: tipos")
v.igual(([r["old"][i] for i in range(1, 8)], r["cfcs"]),
        ([1, 1, 1, 5, 5, 5, 13], [[4, 5, 6], [1, 2, 3], [7]]), "dd-sim: old e componentes")
roupa = digrafo([("cueca", "calça"), ("cueca", "sapatos"), ("calça", "cinto"), ("calça", "sapatos"),
                 ("camisa", "cinto"), ("camisa", "gravata"), ("cinto", "paletó"), ("gravata", "paletó"),
                 ("meias", "sapatos")], ["relógio"])
o = topo(busca(roupa, sorted(roupa)))
v.igual(o, ["relógio", "meias", "cueca", "camisa", "gravata", "calça", "sapatos", "cinto", "paletó"], "dd-roupa")
v.tem("Relógio, meias, cueca, camisa, gravata, calça, sapatos, cinto, paletó", "dd-roupa", R)
C = digrafo([(1, 2), (1, 4), (2, 3), (3, 4), (4, 2), (5, 3), (5, 6), (6, 5)])
r = busca(C, range(1, 7))
v.igual(([r["PE"][i] for i in range(1, 7)], [r["PS"][i] for i in range(1, 7)]),
        ([1, 2, 3, 4, 9, 10], [8, 7, 6, 5, 12, 11]), "dd-classif: PE e PS")
v.igual((de_tipo(r, "árvore"), de_tipo(r, "retorno"), de_tipo(r, "avanço"), de_tipo(r, "cruzamento")),
        (["12", "23", "34", "56"], ["42", "65"], ["14"], ["53"]), "dd-classif: tipos")
v.igual(([r["old"][i] for i in range(1, 7)], r["cfcs"]),
        ([1, 2, 2, 2, 9, 9], [[2, 3, 4], [1], [5, 6]]), "dd-cfcex")
K = digrafo(["ab", "ac", "bd", "cd", "de", "fc"])
v.igual(kahn(K, chave=lambda x: x), list("abfcde"), "dd-kahn")
D = digrafo(["ac", "bc", "cd", "ce"])
tops = ["".join(p) for p in permutations("abcde")
        if all(p.index(a) < p.index(b) for a in D for b in D[a])]
v.igual(sorted(tops), ["abcde", "abced", "bacde", "baced"], "dd-conta")
pesos = {("s", "a"): 3, ("s", "b"): 2, ("a", "c"): 4, ("a", "t"): 2, ("b", "c"): 6, ("b", "t"): 3, ("c", "t"): 1}
Lm = {"s": 0}
for x in "abct":
    Lm[x] = max(Lm[a] + p for (a, b), p in pesos.items() if b == x and a in Lm)
v.igual((Lm["c"], Lm["t"]), (8, 9), "dd-longo")
pre = digrafo([("C1", "C2"), ("C2", "C3"), ("C1", "A1"), ("A1", "C3"), ("P1", "P2")])
sem = {}
for x in topo(busca(pre, sorted(pre))):
    sem[x] = 1 + max([sem[a] for a in pre if x in pre[a]], default=0)
v.igual(sem, dict(C1=1, P1=1, C2=2, A1=2, P2=2, C3=3), "dd-semestres")
P3 = digrafo(["ab", "ac", "bc"])
v.igual((busca(P3, "a")["tipo"][("a", "c")], ), ("avanço",), "dd-papel: ac de avanço visitando b primeiro")

v.fim()
