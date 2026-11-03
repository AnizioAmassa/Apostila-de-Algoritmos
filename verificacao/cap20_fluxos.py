#!/usr/bin/env python3
"""Capítulo 20 (fluxos em redes): fluxos, cortes, rede residual, Ford e Fulkerson e respostas."""
from collections import deque
from itertools import combinations

from comum import Verificador

v = Verificador("20_fluxos.tex", "respostas/20.tex")
T = "20_fluxos.tex"
R = "respostas/20.tex"


def rede(texto):
    """'sa:3 sb:2' -> {('s','a'): 3, ('s','b'): 2}"""
    c = {}
    for tok in texto.split():
        e, k = tok.split(":")
        c[(e[0], e[1])] = int(k)
    return c


def fluxo(c, valores):
    """Fluxo nas arestas de c, na ordem em que aparecem."""
    return dict(zip(c, valores))


def vertices(c):
    return sorted({x for e in c for x in e})


def eh_fluxo(c, f, s="s", t="t"):
    if any(not 0 <= f.get(e, 0) <= c[e] for e in c):
        return False
    for x in vertices(c):
        if x in (s, t):
            continue
        entra = sum(f.get(e, 0) for e in c if e[1] == x)
        sai = sum(f.get(e, 0) for e in c if e[0] == x)
        if entra != sai:
            return False
    return True


def valor(c, f, s="s"):
    return sum(f.get(e, 0) for e in c if e[0] == s)


def corte(c, S):
    mais = [e for e in c if e[0] in S and e[1] not in S]
    menos = [e for e in c if e[1] in S and e[0] not in S]
    return mais, menos, sum(c[e] for e in mais)


def fluxo_corte(c, f, S):
    mais, menos, _ = corte(c, S)
    return sum(f.get(e, 0) for e in mais) - sum(f.get(e, 0) for e in menos)


def residual(c, f):
    r = {}
    for (x, y), k in c.items():
        if k - f.get((x, y), 0) > 0:
            r[(x, y)] = r.get((x, y), 0) + k - f.get((x, y), 0)
        if f.get((x, y), 0) > 0:
            r[(y, x)] = r.get((y, x), 0) + f.get((x, y), 0)
    return r


def bfs(r, s="s", t="t"):
    V = sorted({x for e in r for x in e} | {s, t})
    pai = {s: None}
    F = deque([s])
    while F:
        x = F.popleft()
        for y in V:
            if (x, y) in r and y not in pai:
                pai[y] = x
                F.append(y)
    if t not in pai:
        return None, set(pai)
    cam = [t]
    while pai[cam[-1]] is not None:
        cam.append(pai[cam[-1]])
    return cam[::-1], set(pai)


def aumenta(c, f, cam, g):
    f = dict(f)
    for x, y in zip(cam, cam[1:]):
        if (x, y) in c and c[(x, y)] - f.get((x, y), 0) >= g:
            f[(x, y)] = f.get((x, y), 0) + g
        else:
            f[(y, x)] -= g
    return f


def edmonds_karp(c, f=None):
    f = dict(f or {})
    passos = []
    while True:
        r = residual(c, f)
        cam, alc = bfs(r)
        if cam is None:
            return f, alc, passos
        g = min(r[(x, y)] for x, y in zip(cam, cam[1:]))
        passos.append(("".join(cam), g))
        f = aumenta(c, f, cam, g)


def cortes(c, s="s", t="t"):
    meio = [x for x in vertices(c) if x not in (s, t)]
    for k in range(len(meio) + 1):
        for X in combinations(meio, k):
            S = {s, *X}
            yield "".join(sorted(S)), corte(c, S)[2]


# ---------- a rede dos slides ----------
D = rede("sc:4 sb:2 sa:3 ab:3 bc:1 cb:2 bd:4 da:3 ct:3 dt:5")
f4 = fluxo(D, [2, 2, 0, 1, 1, 1, 3, 1, 2, 2])
f6 = fluxo(D, [3, 2, 1, 2, 1, 1, 4, 1, 3, 3])
f7 = fluxo(D, [3, 2, 2, 2, 1, 1, 4, 0, 3, 4])
for nome, f, val in [("f4", f4, 4), ("f6", f6, 6), ("f7", f7, 7)]:
    v.igual((eh_fluxo(D, f), valor(D, f)), (True, val), f"fluxo {nome}")
v.tem(r"\redeslides{2,2,0,1,1,1,3,1,2,2}", "figura do fluxo de valor 4", T)
v.tem(r"\redeslides{3,2,1,2,1,1,4,1,3,3}", "figura do fluxo de valor 6", T)
v.tem(r"\redeslides{3,2,2,2,1,1,4,0,3,4}", "figura do fluxo de valor 7", T)
v.igual(sorted(e[0] + e[1] for e in D if f6[e] == D[e]), ["bc", "bd", "ct", "sb"], "arestas saturadas do fluxo maximal")
r6 = residual(D, f6)
v.igual(all(bfs({e: k for e, k in r6.items() if (e in D and D[e] - f6[e] > 0)})[0] is None for _ in [0]), True,
        "fluxo de valor 6 é maximal (sem caminho só com arestas de aumento)")
v.igual(edmonds_karp(D)[0] and valor(D, edmonds_karp(D)[0]), 7, "fluxo máximo da rede dos slides")

for S, mais, menos, cap in [({"s", "a", "b"}, ["sc", "bc", "bd"], ["cb", "da"], 9),
                            ({"s", "a", "b", "c", "d"}, ["ct", "dt"], [], 8),
                            ({"s", "a", "b", "c"}, ["bd", "ct"], ["da"], 7)]:
    m, n, k = corte(D, S)
    v.igual((sorted(x + y for x, y in m), sorted(x + y for x, y in n), k), (sorted(mais), sorted(menos), cap), f"corte {sorted(S)}")
    v.igual(fluxo_corte(D, f6, S), 6, f"fluxo de valor 6 no corte {sorted(S)}")
v.igual(min(k for _, k in cortes(D)), 7, "corte mínimo da rede dos slides")

# rede residual do fluxo de valor 4 e o caminho s,a,d,t
r4 = residual(D, f4)
v.igual(min(r4[e] for e in [("s", "a"), ("a", "d"), ("d", "t")]), 1, "gargalo de s,a,d,t")
f5 = aumenta(D, f4, ["s", "a", "d", "t"], 1)
v.igual((valor(D, f5), f5[("s", "a")], f5[("d", "a")], f5[("d", "t")]), (5, 1, 0, 3), "fluxo de valor 5")
v.tem(r"\redeslides{2,2,1,1,1,1,3,0,2,3}", "figura do fluxo de valor 5", T)

# Ford e Fulkerson (caminhos mais curtos) a partir de zero
fF, alc, passos = edmonds_karp(D)
v.igual(passos, [("sct", 3), ("sbdt", 2), ("sabdt", 2)], "aumentos do Exemplo do algoritmo")
v.igual(sorted(alc), ["a", "b", "c", "s"], "corte final {s,a,b,c}")

# exemplo do emparelhamento (cap. 19) como fluxo
EM = {("s", x): 1 for x in "abcde"}
EM.update({(x, y): 1 for x, y in [("a", "1"), ("a", "2"), ("b", "1"), ("c", "2"), ("c", "3"),
                                  ("d", "3"), ("d", "4"), ("e", "1"), ("e", "2")]})
EM.update({(y, "t"): 1 for y in "1234"})
v.igual(valor(EM, edmonds_karp(EM)[0]), 4, "fluxo do exemplo do método húngaro")
v.igual(corte(EM, {"s", "a", "b", "e"})[2], 7, "corte {s,a,b,e}")
v.igual(corte(EM, {"s", "a", "b", "e", "1", "2"})[2], 4, "corte {s,a,b,e,1,2}")

# ---------- respostas ----------
S = {"s", "c"}
m, n, k = corte(D, S)
v.igual((sorted(x + y for x, y in m), sorted(x + y for x, y in n), k, fluxo_corte(D, f7, S)),
        (["cb", "ct", "sa", "sb"], ["bc"], 10, 7), "fl-cortes")
cam, _ = bfs(residual(D, f6))
v.igual(cam, ["s", "a", "d", "t"], "fl-maximal: caminho aumentante")
v.igual(aumenta(D, f6, cam, 1), f7, "fl-maximal: novo fluxo é o de valor 7")

E1 = rede("sa:4 sb:2 ab:1 at:2 bt:3")
v.igual((eh_fluxo(E1, fluxo(E1, [3, 2, 1, 2, 3])), valor(E1, fluxo(E1, [3, 2, 1, 2, 3]))), (True, 5), "fl-def (a)")
v.igual(eh_fluxo(E1, fluxo(E1, [4, 1, 1, 2, 2])), False, "fl-def (b)")
v.igual(min(k for _, k in cortes(E1)), 5, "fl-def: corte mínimo")

E2 = rede("sa:8 sb:5 ab:2 ac:5 bd:6 cd:2 ct:4 dt:7")
f2, alc2, passos2 = edmonds_karp(E2)
v.igual(passos2, [("sact", 4), ("sbdt", 5), ("sabdt", 1), ("sacdt", 1)], "fl-ff: aumentos")
v.igual((valor(E2, f2), sorted(alc2), corte(E2, alc2)[2]), (11, ["a", "b", "s"], 11), "fl-ff: valor e corte")

E3 = rede("sa:3 sb:2 ab:1 at:2 bt:3")
v.igual(sorted(cortes(E3)), [("abs", 5), ("as", 5), ("bs", 6), ("s", 5)], "fl-corte")
v.igual(valor(E3, edmonds_karp(E3)[0]), 5, "fl-corte: fluxo máximo")
v.igual(valor(rede("sa:3 sb:2 ab:1 at:3 bt:3"), edmonds_karp(rede("sa:3 sb:2 ab:1 at:3 bt:3"))[0]), 5, "fl-aumenta")

E4 = rede("sa:2 sb:3 ab:1 at:3 bt:2")
h = fluxo(E4, [2, 2, 0, 2, 2])
cam, alc = bfs(residual(E4, h))
v.igual((eh_fluxo(E4, h), valor(E4, h), cam, sorted(alc), corte(E4, alc)[2]), (True, 4, None, ["b", "s"], 4), "fl-residualex")

C = 50
E5 = {("s", "a"): C, ("s", "b"): C, ("a", "b"): 1, ("a", "t"): C, ("b", "t"): C}
v.igual(len(edmonds_karp(E5)[2]), 2, "fl-pseudo: Edmonds e Karp faz 2 aumentos")
f, n_aum = {}, 0
for cam in [["s", "a", "b", "t"], ["s", "b", "a", "t"]] * C:
    f = aumenta(E5, f, cam, 1)
    n_aum += 1
v.igual((eh_fluxo(E5, f), valor(E5, f), n_aum), (True, 2 * C, 2 * C), "fl-pseudo: 2C aumentos de gargalo 1")

EB = rede("sa:1 sb:1 sc:1 a1:1 a2:1 b1:1 c2:1 c3:1 1t:1 2t:1 3t:1")
v.igual(valor(EB, edmonds_karp(EB)[0]), 3, "fl-emp")
EG = rede("sa:1 sb:1 ac:1 bc:1 ct:1 at:1 bd:1 dt:1")
v.igual((valor(EG, edmonds_karp(EG)[0]), min(k for _, k in cortes(EG))), (2, 2), "fl-menger")

# fl-decomp: caminhos s,c,t (3), s,b,d,t (2), s,a,b,d,t (2) e o ciclo b,c,b (1)
resto = dict(f7)
for cam, q in [("sct", 3), ("sbdt", 2), ("sabdt", 2), ("bcb", 1)]:
    for x, y in zip(cam, cam[1:]):
        resto[(x, y)] -= q
v.igual(all(q == 0 for q in resto.values()), True, "fl-decomp")

v.fim()
