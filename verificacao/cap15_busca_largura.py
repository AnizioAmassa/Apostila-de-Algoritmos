#!/usr/bin/env python3
"""Capítulo 15 (busca em largura)."""
from collections import deque

from comum import Verificador

v = Verificador("15_busca_largura.tex", "respostas/15.tex")
R = "respostas/15.tex"


def grafo(arestas):
    g = {}
    for e in arestas:
        a, b = e
        g.setdefault(a, set()).add(b)
        g.setdefault(b, set()).add(a)
    return {x: sorted(n) for x, n in g.items()}


def bfs(g, raiz):
    """Busca em largura com a classificação das arestas do pseudocódigo."""
    L, nivel, pai = {raiz: 1}, {raiz: 0}, {raiz: None}
    F, t, tipos, saidas = deque([raiz]), 1, {}, []
    while F:
        x = F.popleft()
        for w in g[x]:
            if w not in L:
                t += 1
                L[w], nivel[w], pai[w] = t, nivel[x] + 1, x
                F.append(w)
                tipos[frozenset((x, w))] = "pai"
            elif nivel[w] == nivel[x] and w in F:
                tipos[frozenset((x, w))] = "irmão" if pai[w] == pai[x] else "primo"
            elif nivel[w] == nivel[x] + 1:
                tipos[frozenset((x, w))] = "tio"
        saidas.append((x, list(F)))
    return L, nivel, pai, tipos, saidas


def de_tipo(tipos, t):
    return sorted("".join(sorted(e)) for e, k in tipos.items() if k == t)


G = grafo(["ab", "ac", "bc", "bd", "cd", "ce", "de", "df", "dg", "ef", "eh", "fg", "gh"])
L, nivel, pai, tipos, saidas = bfs(G, "a")
for x in "abcdefgh":
    v.tem(f"of {x}] {{{L[x]}/{nivel[x]}}}", f"rótulo L/nível de {x}")
v.igual((de_tipo(tipos, "pai"), de_tipo(tipos, "irmão"), de_tipo(tipos, "primo"), de_tipo(tipos, "tio")),
        (["ab", "ac", "bd", "ce", "df", "dg", "eh"], ["bc", "fg"], ["de", "gh"], ["cd", "ef"]),
        "classificação das arestas da Figura 15.1")
for x, fila in saidas:
    v.tem(f"${x}$ & " if x != "a" else "$a$ & $b$ e $c$", f"tabela da fila: {x}")
    v.tem(",".join(fila) if fila else "vazia", f"fila depois de {x}")
v.igual(dict(saidas)["d"], ["e", "f", "g"], "depois que d sai, a fila é e,f,g")
v.igual((pai["h"], pai["e"], pai["c"]), ("e", "c", "a"), "caminho mínimo de a até h")

B = grafo([(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (2, 6)])
L, nivel, pai, tipos, _ = bfs(B, 1)
v.igual(({x for x in nivel if nivel[x] == 1}, {x for x in nivel if nivel[x] == 2}), ({2, 4}, {3, 5, 6}),
        "níveis do grafo bipartido")
v.igual([k for e, k in tipos.items() if k != "pai"], ["tio"], "só uma aresta-tio (43)")
v.igual(({x for x in nivel if nivel[x] % 2 == 0}, {x for x in nivel if nivel[x] % 2}), ({1, 3, 5, 6}, {2, 4}),
        "2-coloração pela paridade")


def esquema(g, raiz, pilha):
    marcado, D, ordem, arv = {raiz}, [raiz], [raiz], []
    while D:
        x = D[-1] if pilha else D[0]
        w = next((w for w in g[x] if w not in marcado), None)
        if w is None:
            D.pop(-1 if pilha else 0)
        else:
            marcado.add(w)
            ordem.append(w)
            arv.append((x, w))
            D.append(w)
    return ordem, arv


H = grafo([(1, 2), (1, 3), (2, 4), (3, 4), (3, 6), (4, 5)])
v.igual(esquema(H, 1, False), ([1, 2, 3, 4, 6, 5], [(1, 2), (1, 3), (2, 4), (3, 6), (4, 5)]), "esquema com fila")
v.igual(esquema(H, 1, True), ([1, 2, 4, 3, 6, 5], [(1, 2), (2, 4), (4, 3), (3, 6), (4, 5)]), "esquema com pilha")
v.tem("A ordem de marcação é $1,2,3,4,6,5$", "ordem com fila")
v.tem("A ordem é $1,2,4,3,6,5$", "ordem com pilha")

# --- Respostas ---
S = grafo(["rs", "rv", "sw", "wt", "wx", "tx", "tu", "xu", "xy", "uy"])
L, nivel, pai, tipos, _ = bfs(S, "s")
v.igual("".join(sorted(L, key=L.get)), "srwvtxuy", "bl-sim: ordem de visita")
v.igual((de_tipo(tipos, "irmão"), de_tipo(tipos, "tio"), de_tipo(tipos, "primo")), (["tx"], ["ux"], ["uy"]),
        "bl-sim: classificação")
v.igual({x: nivel[x] for x in "srwvtxuy"}, dict(s=0, r=1, w=1, v=2, t=2, x=2, u=3, y=3), "bl-sim: níveis")
T = grafo([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7)])
n1 = bfs(T, 1)[1]
a = max(n1, key=lambda x: (n1[x], x))
na = bfs(T, a)[1]
b = max(na, key=na.get)
v.igual((a, n1[a], b, na[b]), (7, 3, 6, 5), "bl-diam")
lab = ["S..#", "##.#", "....", "#.#E"]
livres = {(i, j) for i in range(4) for j in range(4) if lab[i][j] != "#"}
M = {c: sorted(d for d in livres if abs(d[0] - c[0]) + abs(d[1] - c[1]) == 1) for c in livres}
dist = bfs(M, (0, 0))[1]
v.igual(dist[(3, 3)], 6, "bl-grade: distância até E")
v.igual({c: dist[c] for c in [(0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 3), (2, 0), (3, 1)]},
        {(0, 1): 1, (0, 2): 2, (1, 2): 3, (2, 2): 4, (2, 1): 5, (2, 3): 5, (2, 0): 6, (3, 1): 6},
        "bl-grade: distâncias")
for n, bip in ((5, False), (6, True)):
    C = grafo([(i, i % n + 1) for i in range(1, n + 1)])
    tipos = bfs(C, 1)[3]
    v.igual(not any(k in ("irmão", "primo") for k in tipos.values()), bip, f"bl-bip: ciclo com {n}")
casas = {(c, l) for c in range(8) for l in range(8)}
saltos = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
Cav = {x: [(x[0] + a_, x[1] + b_) for a_, b_ in saltos if (x[0] + a_, x[1] + b_) in casas] for x in casas}
v.igual(bfs(Cav, (0, 0))[1][(7, 7)], 6, "bl-cavalo: a1 a h8 em 6 movimentos")


def jarros():
    ini = (0, 0)
    dist, F = {ini: 0}, deque([ini])
    while F:
        a_, b_ = F.popleft()
        prox = {(3, b_), (a_, 5), (0, b_), (a_, 0)}
        t = min(a_, 5 - b_); prox.add((a_ - t, b_ + t))
        t = min(b_, 3 - a_); prox.add((a_ + t, b_ - t))
        for e in prox:
            if e not in dist:
                dist[e] = dist[(a_, b_)] + 1
                F.append(e)
    return min(d for (a_, b_), d in dist.items() if 4 in (a_, b_))


v.igual(jarros(), 6, "bl-jarros")
K = grafo([(x, y) for x in "abc" for y in "xyz"])
L, nivel, pai, tipos, _ = bfs(K, "a")
v.igual((sorted(x for x in nivel if nivel[x] == 1), sorted(x for x in nivel if nivel[x] == 2), pai["b"], pai["c"]),
        (list("xyz"), list("bc"), "x", "x"), "bl-k33: níveis e pais")
v.igual(de_tipo(tipos, "tio"), ["by", "bz", "cy", "cz"], "bl-k33: arestas-tio")

v.fim()
