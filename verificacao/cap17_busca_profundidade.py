#!/usr/bin/env python3
"""Capítulo 17 (busca em profundidade em grafos não direcionados)."""
import sys

from comum import Verificador

sys.setrecursionlimit(10000)
v = Verificador("17_busca_profundidade.tex", "respostas/17.tex")
R = "respostas/17.tex"


def grafo(arestas):
    g = {}
    for a, b in arestas:
        g.setdefault(a, set()).add(b)
        g.setdefault(b, set()).add(a)
    return {x: sorted(n) for x, n in g.items()}


def busca(g, raizes):
    """O procedimento P do pseudocódigo, com back(v) e a pilha de arestas."""
    PE = {x: 0 for x in g}
    PS = {x: 0 for x in g}
    pai, back = {x: None for x in g}, {}
    t = [0]
    pilha, blocos, retornos, arvore, pilhas_ao_imprimir = [], [], [], [], []

    def P(x):
        t[0] += 1
        PE[x] = back[x] = t[0]
        for w in g[x]:
            if PE[w] == 0:
                pai[w] = x
                arvore.append((x, w))
                pilha.append((x, w))
                P(w)
                if back[w] >= PE[x]:
                    pilhas_ao_imprimir.append(list(pilha))
                    bloco = set()
                    while True:
                        e = pilha.pop()
                        bloco |= set(e)
                        if e == (x, w):
                            break
                    blocos.append(bloco)
                back[x] = min(back[x], back[w])
            elif PS[w] == 0 and w != pai[x]:
                pilha.append((x, w))
                retornos.append((x, w))
                back[x] = min(back[x], PE[w])
        t[0] += 1
        PS[x] = t[0]

    componentes = 0
    for r in raizes:
        if PE[r] == 0:
            componentes += 1
            P(r)
    raiz_filhos = {r: sum(1 for a, _ in arvore if a == r) for r in raizes if pai[r] is None}
    # v (não raiz) é articulação se tem um filho x com back(x) >= PE(v)
    artic = {pai[x] for x in g if pai[x] is not None and pai[pai[x]] is not None and back[x] >= PE[pai[x]]}
    artic |= {r for r, k in raiz_filhos.items() if k >= 2}
    pontes = [(pai[x], x) for x in g if pai[x] is not None and back[x] > PE[pai[x]]]
    return dict(PE=PE, PS=PS, pai=pai, back=back, blocos=blocos, retornos=retornos, arvore=arvore,
                artic=artic, pontes=pontes, componentes=componentes, pilhas=pilhas_ao_imprimir)


def fmt_blocos(blocos):
    return [sorted(b) for b in blocos]


G = grafo(["ac", "ab", "bc", "bd", "cd", "ce", "de", "ef", "eg", "fg"])
r = busca(G, "e")
for x in "abcdefg":
    v.tem(f"of {x}] {{{r['PE'][x]}/{r['PS'][x]}}}", f"PE/PS de {x} na Figura 17.1")
v.igual(sorted(map("".join, r["retornos"])), ["bc", "dc", "de", "ge"], "arestas de retorno")
v.igual(sorted(map("".join, r["arvore"])), ["ab", "bd", "ca", "ec", "ef", "fg"], "arestas de árvore")
v.tem("$(e\\,(c\\,(a\\,(b\\,(d\\ d)\\,b)\\,a)\\,c)\\,(f\\,(g\\ g)\\,f)\\,e)$", "parênteses")
eventos = sorted([(r["PE"][x], "(" + x) for x in G] + [(r["PS"][x], x + ")") for x in G])
v.igual("".join(e for _, e in eventos), "(e(c(a(b(dd)b)a)c)(f(gg)f)e)", "parênteses aninhados")
v.igual((set(r["back"].values()), r["artic"], fmt_blocos(r["blocos"])),
        ({1}, {"e"}, [list("abcde"), list("efg")]), "back, articulação e blocos com raiz e")
ra = busca(G, "a")
v.igual((ra["PE"]["e"], ra["back"]["f"], "e" in ra["artic"]), (5, 5, True), "busca a partir de a")
v.tem("$back(f)=5\\ge PE(e)=5$", "busca a partir de a no texto")
# Aplicações
v.igual((r["pai"]["a"], r["pai"]["c"]), ("c", "e"), "caminho de e até a")
cor = {"e": 0}
for a, b in r["arvore"]:
    cor[b] = 1 - cor[a]
v.igual([cor[x] for x in "cabd"], [1, 0, 1, 0], "2-coloração pela árvore")
v.igual(cor["b"] == cor["c"], True, "bc liga dois vértices de cor 1")

A = grafo(["ab", "bc", "cd", "da", "de", "ef", "fg", "ge", "bh"])
r = busca(A, "a")
v.igual([r["PE"][x] for x in "abcdefgh"], [1, 2, 3, 4, 5, 6, 7, 13], "PE do Exemplo 17.3")
v.igual([r["back"][x] for x in "abcdefgh"], [1, 1, 1, 1, 5, 5, 5, 13], "back do Exemplo 17.3")
v.igual((r["artic"], sorted(map("".join, r["pontes"]))), ({"b", "d", "e"}, ["bh", "de"]), "articulações e pontes")
v.igual(fmt_blocos(r["blocos"]), [list("efg"), list("de"), list("bh"), list("abcd")], "blocos na ordem")
for x in "abcdefg":
    v.tem(f"{x}/", f"figura da árvore: {x}")
v.tem("13/13", "rótulo de h na figura")

# --- Respostas ---
r = busca(G, "e")
v.igual([list(map("".join, p)) for p in r["pilhas"]],
        [["ec", "ca", "ab", "bc", "bd", "dc", "de"], ["ef", "fg", "ge"]], "bp-pilha")
r = busca(grafo([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7)]), [1])
v.igual(([r["PE"][i] for i in range(1, 8)], [r["PS"][i] for i in range(1, 8)]),
        ([1, 2, 3, 4, 5, 6, 7], [14, 13, 12, 11, 10, 9, 8]), "bp-sim: PE e PS")
v.igual(([r["back"][i] for i in range(1, 8)], r["artic"], sorted(r["pontes"])),
        ([1, 1, 1, 4, 4, 4, 7], {3, 4, 6}, [(3, 4), (6, 7)]), "bp-sim: back, articulações e pontes")
v.igual(sorted(sorted(b) for b in r["blocos"]), [[1, 2, 3], [3, 4], [4, 5, 6], [6, 7]], "bp-sim: blocos")
T = grafo([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 8), (6, 7), (7, 8)])
r = busca(T, [1])
v.tem("$PE$ de 1 a 8: $" + ",".join(str(r["PE"][i]) for i in range(1, 9)) + "$", "bp-trace: PE", R)
v.tem("$PS$: $" + ",".join(str(r["PS"][i]) for i in range(1, 9)) + "$", "bp-trace: PS", R)
v.igual((sorted(r["arvore"]), sorted(r["retornos"]), r["artic"]),
        (sorted([(1, 2), (2, 4), (4, 8), (8, 5), (8, 7), (7, 3), (3, 6)]), sorted([(5, 2), (3, 1), (6, 7)]), set()),
        "bp-trace: árvore, retornos e articulações")
v.igual(r["retornos"][0], (5, 2), "bp-cicloex: primeira aresta de retorno")
x, cic = 5, [5]
while x != 2:
    x = r["pai"][x]
    cic.append(x)
v.igual(cic, [5, 8, 4, 2], "bp-cicloex: subida de 5 até 2")
C = grafo([(1, 2), (2, 3), (3, 1), (4, 5), (6, 7), (7, 8), (8, 9), (9, 6)])
for i in range(1, 10):
    C.setdefault(i, [])
r = busca(C, range(1, 10))
v.igual((r["componentes"], [i for i in range(1, 10) if r["pai"][i] is None]), (3, [1, 4, 6]), "bp-comp")
r = busca(grafo([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]), [1])
cor = {1: 0}
for a, b in r["arvore"]:
    cor[b] = 1 - cor[a]
v.igual(([cor[i] for i in range(1, 5)], (3, 1) in r["retornos"]), ([0, 1, 0, 1], True), "bp-bipex")
r = busca(grafo([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 4), (4, 7)]), [1])
v.igual((r["artic"], sorted(r["pontes"]), sorted(sorted(b) for b in r["blocos"])),
        ({3, 4}, [(3, 4), (4, 7)], [[1, 2, 3], [3, 4], [4, 5, 6], [4, 7]]), "bp-blocos")
r = busca(grafo([(1, 2), (2, 3), (3, 4), (1, 4)]), [1])
v.igual(r["pai"][4], 3, "bp-labirinto: a busca chega a 4 por 1,2,3,4")

v.fim()
