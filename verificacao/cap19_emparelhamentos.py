#!/usr/bin/env python3
"""Capítulo 19 (emparelhamentos): método húngaro, Hall e König, blossoms e respostas."""
from collections import deque
from itertools import combinations, permutations
from math import factorial

from comum import Verificador

v = Verificador("19_emparelhamentos.tex", "respostas/19.tex")
T = "19_emparelhamentos.tex"
R = "respostas/19.tex"


def arestas(texto):
    """'su uv va' -> [('s','u'), ('u','v'), ('v','a')]; vértices de um caractere."""
    return [(e[0], e[1]) for e in texto.split()]


def vizinhos(E):
    g = {}
    for a, b in E:
        g.setdefault(a, set()).add(b)
        g.setdefault(b, set()).add(a)
    return {x: sorted(n, key=str) for x, n in g.items()}


def eh_emparelhamento(S):
    vs = [x for e in S for x in e]
    return len(vs) == len(set(vs))


def nu(E):
    """Tamanho de um emparelhamento máximo, por força bruta."""
    V = {x for e in E for x in e}
    for k in range(len(V) // 2, -1, -1):
        for S in combinations(E, k):
            if eh_emparelhamento(S):
                return k
    return 0


def tau(E):
    V = sorted({x for e in E for x in e}, key=str)
    for k in range(len(V) + 1):
        for C in combinations(V, k):
            if all(a in C or b in C for a, b in E):
                return k, set(C)


def maximal(E, M):
    usados = {x for e in M for x in e}
    return all(a in usados or b in usados for a, b in E)


def norm(M):
    return {tuple(sorted(map(str, e))) for e in M}


def difsim(M, P):
    return norm(M) ^ norm(P)


def busca_alternante(g, par, r):
    """Busca em largura alternante do método húngaro a partir de r.
    Devolve (caminho aumentante ou None, vértices da árvore)."""
    pai = {r: None}
    F = deque([r])
    arvore = [r]
    while F:
        x = F.popleft()
        for y in g[x]:
            if y in pai:
                continue
            pai[y] = x
            arvore.append(y)
            if y not in par:
                cam = []
                while y is not None:
                    cam.append(y)
                    y = pai[y]
                return cam[::-1], arvore
            z = par[y]
            pai[z] = y
            arvore.append(z)
            F.append(z)
    return None, arvore


def hungaro(X, g, M0):
    par = {}
    for a, b in M0:
        par[a], par[b] = b, a
    log = []
    for r in X:
        if r in par:
            continue
        cam, arvore = busca_alternante(g, par, r)
        log.append((r, cam, arvore))
        if cam:
            for i in range(0, len(cam), 2):
                par[cam[i]], par[cam[i + 1]] = cam[i + 1], cam[i]
    return {(x, par[x]) for x in X if x in par}, log


def rotulos_edmonds(g, M, r):
    """Busca do algoritmo de Edmonds até a primeira aresta entre dois pares."""
    par = {}
    for a, b in M:
        par[a], par[b] = b, a
    lab = {r: "P"}
    F = deque([r])
    while F:
        x = F.popleft()
        for y in g[x]:
            if y not in lab:
                if y not in par:
                    return "livre", (x, y), lab
                lab[y], lab[par[y]] = "I", "P"
                F.append(par[y])
            elif lab[y] == "P" and par.get(x) != y:
                return "blossom", (x, y), lab
    return "nada", None, lab


# ---------- Exemplos 19.1 e 19.2: a grade 2x3 ----------
grade = [(1, 2), (2, 3), (4, 5), (5, 6), (1, 4), (2, 5), (3, 6)]
v.igual(nu(grade), 3, "nu da grade")
v.igual(maximal(grade, [(1, 2), (5, 6)]), True, "{12,56} é maximal")
v.igual(eh_emparelhamento([(1, 4), (2, 5), (3, 6)]), True, "{14,25,36} é emparelhamento")
v.igual(difsim([(1, 2), (5, 6)], [(4, 1), (1, 2), (2, 3)]), norm([(1, 4), (2, 3), (5, 6)]), "M△P na grade")
v.tem(r"o resultado, $\{14,23,56\}$", "resultado da ampliação", T)

# ---------- Exemplo do método húngaro, Hall e König ----------
g = vizinhos([("a", 1), ("a", 2), ("b", 1), ("c", 2), ("c", 3), ("d", 3), ("d", 4), ("e", 1), ("e", 2)])
final, log = hungaro("abcde", g, [("a", 1), ("c", 2), ("d", 3)])
v.igual(log[0][1], ["b", 1, "a", 2, "c", 3, "d", 4], "caminho a partir de b")
v.tem("$b,1,a,2,c,3,d,4$", "caminho aumentante no texto", T)
v.igual(log[1][1], None, "busca a partir de e falha")
v.igual(sorted(map(str, log[1][2])), sorted(["e", "1", "b", "2", "a"]), "árvore húngara de e")
v.tem(r"$\{e,1,b,2,a\}$", "árvore húngara no texto", T)
v.igual(final, {("a", 2), ("b", 1), ("c", 3), ("d", 4)}, "emparelhamento final do exemplo")
v.tem(r"$\{b1,a2,c3,d4\}$", "emparelhamento final no texto", T)
Eh = [(x, y) for x in g if isinstance(x, str) for y in g[x]]
v.igual(nu(Eh), 4, "nu do exemplo húngaro")
v.igual(tau(Eh)[0], 4, "tau do exemplo húngaro")
v.igual(all(a in {"c", "d", 1, 2} or b in {"c", "d", 1, 2} for a, b in Eh), True, "cobertura de König {c,d,1,2}")
v.tem(r"$\{c,d\}\cup\{1,2\}$", "cobertura no texto", T)

# ---------- Exemplo do blossom (ciclo de 7 vértices) ----------
Eb = arestas("su uv va ab bc cd de ef fv ct")
Mb = arestas("uv ab cd ef")
gb = vizinhos(Eb)
v.igual(nu(Eb), 5, "nu do exemplo do blossom")
parb = {}
for a, b in Mb:
    parb[a], parb[b] = b, a
cam, _ = busca_alternante(gb, parb, "s")
v.igual(cam, None, "a busca do método húngaro falha no exemplo do blossom")
tipo, aresta, lab = rotulos_edmonds(gb, Mb, "s")
v.igual((tipo, aresta), ("blossom", ("e", "d")), "aresta entre pares que fecha o blossom")
v.igual(lab, dict(s="P", u="I", v="P", a="I", b="P", f="I", e="P", c="I", d="P"), "rótulos da busca")
caminho = arestas("su uv vf fe ed dc ct")
v.igual(difsim(Mb, caminho), norm(arestas("su vf ed ct ab")), "emparelhamento depois da ampliação")
v.tem(r"$M=\{su,vf,ed,ct,ab\}$", "novo emparelhamento no texto", T)
v.tem("$s,u,v,f,e,d,c,t$", "caminho aumentante no texto", T)

# ---------- Respostas ----------
P6 = [(i, i + 1) for i in range(1, 6)]
v.igual((nu(P6), maximal(P6, [(2, 3), (4, 5)])), (3, True), "em-def")
v.igual(nu([(i, i + 1) for i in range(1, 7)]), 3, "em-def: caminho com 7 vértices")
v.igual(nu([(1, 2), (2, 3), (3, 4)]), 2, "em-metade: caminho 1234")
Ea = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 5)]
v.igual(difsim([(2, 3), (4, 5)], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]), norm([(1, 2), (3, 4), (5, 6)]), "em-aumenta")
v.igual(nu(Ea), 3, "em-aumenta: máximo")

g2 = vizinhos([("a", 1), ("a", 2), ("b", 2), ("b", 3), ("c", 3), ("c", 4), ("d", 4), ("d", 5), ("e", 1)])
final2, log2 = hungaro("abcde", g2, [])
v.igual([c for _, c, _ in log2], [["a", 1], ["b", 2], ["c", 3], ["d", 4],
                                  ["e", 1, "a", 2, "b", 3, "c", 4, "d", 5]], "em-hung: caminhos")
v.tem("$e,1,a,2,b,3,c,4,d,5$", "em-hung: caminho longo", R)
v.igual(final2, {("e", 1), ("a", 2), ("b", 3), ("c", 4), ("d", 5)}, "em-hung: final")
v.tem(r"$\{e1,a2,b3,c4,d5\}$", "em-hung: final no texto", R)

E3 = [("a", 1), ("a", 2), ("b", 2), ("c", 1), ("c", 2), ("d", 3), ("d", 4)]
v.igual(nu(E3), 3, "em-hallex: nu")
v.igual(tau(E3)[0], 3, "em-konig: tau")
v.igual(all(a in {"d", 1, 2} or b in {"d", 1, 2} for a, b in E3), True, "em-konig: {d,1,2} cobre")
v.tem(r"$\{d\}\cup\{1,2\}=\{d,1,2\}$", "em-konig no texto", R)

arv = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7)]
v.igual(nu(arv), 3, "em-arvore")
v.igual(eh_emparelhamento([(2, 4), (6, 7), (1, 3)]), True, "em-arvore: {24,67,13}")


def perfeitos(V, E):
    return sum(1 for S in combinations(E, len(V) // 2)
               if len({x for e in S for x in e}) == len(V))


v.igual(perfeitos(list("abcxyz"), [(a, b) for a in "abc" for b in "xyz"]), factorial(3), "em-conta: K33")
v.igual(perfeitos(list(range(6)), list(combinations(range(6), 2))), 15, "em-conta: K6")


def cobertura_arestas(E):
    V = {x for e in E for x in e}
    for k in range(1, len(E) + 1):
        for S in combinations(E, k):
            if {x for e in S for x in e} == V:
                return k


v.igual(cobertura_arestas(P6), 3, "em-cobertura: caminho")
v.igual(cobertura_arestas([(0, i) for i in range(1, 5)]), 4, "em-cobertura: estrela")
tri = [(1, 2), (2, 3), (1, 3)]
v.igual((nu(tri), tau(tri)[0]), (1, 2), "em-triangulo")
v.igual((4 + 1 - 3) // 2, 1, "em-tutte: cota da estrela")

Ef = arestas("ra ab bc cd dr cx")
tipo, aresta, lab = rotulos_edmonds(vizinhos(Ef), arestas("ab cd"), "r")
v.igual((tipo, aresta), ("blossom", ("b", "c")), "em-flor: blossom fechado por bc")
v.igual(lab, dict(r="P", a="I", b="P", d="I", c="P"), "em-flor: rótulos")
v.igual(difsim(arestas("ab cd"), arestas("rd dc cx")), norm(arestas("ab rd cx")), "em-flor: novo M")
v.tem(r"$\{ab,rd,cx\}$", "em-flor no texto", R)

C = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]
custos = sorted(sum(C[i][p[i]] for i in range(3)) for p in permutations(range(3)))
v.igual(custos, [5, 6, 6, 7, 9, 11], "em-atrib: custos")
v.tem("$5,6,6,7,9,11$", "em-atrib: custos no texto", R)
v.igual(min(permutations(range(3)), key=lambda p: sum(C[i][p[i]] for i in range(3))), (1, 0, 2), "em-atrib: designação")
v.igual(round(factorial(20) / 1e18, 1), 2.4, "em-atrib: 20!")

# em-slides: o exemplo de simulação dos slides
nomes = dict(a=(1, 2), b=(2, 3), c=(3, 4), d=(4, 5), e=(5, 6), f=(6, 7), g=(7, 8), h=(1, 8),
             i=(2, 8), j=(8, 9), k=(7, 9), x=(3, 9), y=(3, 6), z=(4, 6))
Es = list(nomes.values())
M1 = difsim([nomes["b"], nomes["g"]], [(1, 2), (2, 3), (3, 4)])
v.igual(M1, norm([nomes["a"], nomes["c"], nomes["g"]]), "em-slides: primeira ampliação")
M2 = M1 ^ norm([nomes["e"]])
v.igual(M2, norm([nomes[t] for t in "acge"]), "em-slides: segunda ampliação")
v.igual(nu(Es), 4, "em-slides: nu = 4")
v.tem(r"$M=\{a,c,g,e\}=\{12,34,78,56\}$", "em-slides no texto", R)

v.fim()
