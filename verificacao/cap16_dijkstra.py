#!/usr/bin/env python3
"""Capítulo 16 (Dijkstra)."""
from math import inf, log2

from comum import Verificador

v = Verificador("16_dijkstra.tex", "respostas/16.tex")
R = "respostas/16.tex"


def dijkstra(arestas, s, nao_direcionado=False):
    """Versão do pseudocódigo: remove o menor rótulo (empate: ordem dos nomes),
    marca e relaxa as arestas para vértices desmarcados. Devolve as linhas da
    tabela (removido, rótulos depois dele, mudanças de pai)."""
    adj = {}
    for a, b, p in arestas:
        adj.setdefault(a, []).append((b, p))
        adj.setdefault(b, [])
        if nao_direcionado:
            adj[b].append((a, p))
    L = {x: inf for x in adj}
    pai = {x: None for x in adj}
    L[s] = 0
    marcado, linhas = set(), []
    while len(marcado) < len(adj):
        cand = [x for x in adj if x not in marcado and L[x] < inf]
        if not cand:
            break
        x = min(cand, key=lambda y: (L[y], str(y)))
        marcado.add(x)
        mud = []
        for w, p in adj[x]:
            if w not in marcado and L[x] + p < L[w]:
                L[w], pai[w] = L[x] + p, x
                mud.append(w)
        linhas.append((x, dict(L), mud))
    return L, pai, linhas


fmt = lambda x: "\\infty" if x == inf else str(x)
W = [("a", "b", 1), ("a", "c", 3), ("a", "e", 6), ("b", "c", 1), ("b", "d", 3), ("c", "a", 1),
     ("c", "b", 2), ("c", "d", 1), ("d", "a", 3), ("d", "e", 2), ("e", "d", 1)]
L, pai, linhas = dijkstra(W, "a")
ordem = []
for x, rot, mud in linhas:
    ordem.append(x)
    resto = [y for y in "abcde" if y not in ordem[:-1]]
    celulas = []
    for y in "abcde":
        if y in ordem[:-1]:
            celulas.append("")
        elif y == x:
            celulas.append(f"\\textbf{{{rot[y]}}}")
        else:
            celulas.append(f"${fmt(rot[y])}$" if rot[y] == inf else str(rot[y]))
    v.tem(f"${x}$ ({rot[x]}) & " + " & ".join(celulas), f"tabela do Dijkstra: {x}")
    v.tem(("$" + ",".join(mud) + "\\leftarrow " + x + "$") if mud else "---", f"mudanças de pai em {x}")
v.igual(([L[x] for x in "abcde"], [pai[x] for x in "bcde"]), ([0, 1, 2, 3, 5], ["a", "b", "c", "d"]),
        "distâncias e árvore a→b→c→d→e")
v.tem("$L(v)=4$, $W(v,w)=3$ e $L(w)=9$, o relaxamento faz $L(w):=7$", "exemplo de relaxamento")

# Heap binário de mínimo com vetor de posições, seguindo o pseudocódigo:
# w entra em D com o rótulo atual e é reposicionado (subir) depois do relaxamento.
def dijkstra_heap(arestas, s, parar_depois_de):
    adj = {}
    for a, b, p in arestas:
        adj.setdefault(a, []).append((b, p))
        adj.setdefault(b, [])
    L = {x: inf for x in adj}
    L[s] = 0
    H, pos, marcado = [s], {s: 0}, set()

    def troca(i, j):
        H[i], H[j] = H[j], H[i]
        pos[H[i]], pos[H[j]] = i, j

    def subir(i):
        while i > 0 and L[H[i]] < L[H[(i - 1) // 2]]:
            troca(i, (i - 1) // 2)
            i = (i - 1) // 2

    def descer(i):
        while 2 * i + 1 < len(H):
            j = 2 * i + 1
            if j + 1 < len(H) and L[H[j + 1]] < L[H[j]]:
                j += 1
            if L[H[j]] >= L[H[i]]:
                break
            troca(i, j)
            i = j

    while H:
        x = H[0]
        troca(0, len(H) - 1)
        H.pop()
        del pos[x]
        if H:
            descer(0)
        marcado.add(x)
        for w, p in adj[x]:
            if w in marcado:
                continue
            if w not in pos:
                H.append(w)
                pos[w] = len(H) - 1
            if L[x] + p < L[w]:
                L[w] = L[x] + p
                subir(pos[w])
        if x == parar_depois_de:
            return [(y, L[y]) for y in H], {y: pos[y] + 1 for y in H}


heap, posicoes = dijkstra_heap(W, "a", "b")
v.igual((heap, posicoes), ([("c", 2), ("e", 6), ("d", 4)], {"c": 1, "e": 2, "d": 3}),
        "heap e vetor de posições depois de remover b")
v.tem("$(" + ",\\ ".join(f"{y}{{:}}{l}" for y, l in heap) + ")$", "heap depois de remover b")
v.tem("$pos[c]=1$, $pos[e]=2$ e $pos[d]=3$", "vetor de posições no texto")

# Aresta negativa (Figura 16.3)
Ln, _, lin = dijkstra([("s", "a", 1), ("s", "b", 3), ("b", "a", -3), ("a", "c", 1)], "s")
v.igual(([x for x, _, _ in lin], Ln["a"], Ln["c"]), (["s", "a", "c", "b"], 1, 2), "Dijkstra com aresta negativa")
v.igual((3 - 3, 3 - 3 + 1), (0, 1), "distâncias corretas de a e c")

# Figura do custo: cruzamento perto de n^2/log2 n
n = 1000
v.igual(round(n * n / log2(n), -5), 1e5, "cruzamento das curvas")
v.tem("{(1000+x)*9.966}", "curva do heap na figura")
v.igual(round(log2(1000), 3), 9.966, "log2 1000")

# --- Respostas ---
Ls, ps, lin = dijkstra([("s", "t", 10), ("s", "y", 5), ("t", "x", 1), ("t", "y", 2), ("x", "z", 4),
                        ("y", "t", 3), ("y", "x", 9), ("y", "z", 2), ("z", "s", 7), ("z", "x", 6)], "s")
v.tem(", ".join(f"${x}\\,({Ls[x]})$" for x, _, _ in lin[:-1]) + f" e ${lin[-1][0]}\\,({Ls[lin[-1][0]]})$",
      "dj-sim: ordem de remoção", R)
v.igual({x: ps[x] for x in "yztx"}, dict(y="s", z="y", t="y", x="t"), "dj-sim: pais")
Lu, pu, lin = dijkstra([(1, 2, 7), (1, 3, 9), (1, 6, 14), (2, 3, 10), (2, 4, 15), (3, 4, 11), (3, 6, 2),
                        (4, 5, 6), (5, 6, 9)], 1, nao_direcionado=True)
v.tem(", ".join(f"${x}\\,({Lu[x]})$" for x, _, _ in lin[:-1]) + f" e ${lin[-1][0]}\\,({Lu[lin[-1][0]]})$",
      "dj-und: ordem de remoção", R)
v.igual({x: pu[x] for x in (2, 3, 6, 4, 5)}, {2: 1, 3: 1, 6: 3, 4: 3, 5: 6}, "dj-und: pais")
Lg, _, lin = dijkstra([("x", "y", 1), ("x", "z", 2), ("z", "y", -2)], "x")
v.igual((lin[1][0], Lg["y"]), ("y", 1), "dj-neg: y é fixado com rótulo 1")
v.igual((1 + 2, 2 + 2 + (-2 + 2)), (3, 4), "dj-neg: somar 2 muda o caminho ótimo")
n1, m1, n2, m2 = 10 ** 5, 3 * 10 ** 5, 10 ** 4, 5 * 10 ** 7
v.igual((round((n1 + m1) * log2(n1) / 1e6), round((n2 + m2) * log2(n2) / 1e8)), (7, 7), "dj-escolha")

v.fim()
