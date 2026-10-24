#!/usr/bin/env python3
"""Capítulo 14 (árvores geradoras mínimas: Kruskal e Prim)."""
from itertools import combinations
from math import inf, log2

from comum import Verificador

v = Verificador("14_agm.tex", "respostas/14.tex")
R = "respostas/14.tex"


class UF:
    def __init__(self, xs):
        self.p = {x: x for x in xs}

    def f(self, x):
        while self.p[x] != x:
            x = self.p[x]
        return x

    def u(self, a, b):
        ra, rb = self.f(a), self.f(b)
        if ra == rb:
            return False
        self.p[ra] = rb
        return True

    def grupos(self):
        g = {}
        for x in self.p:
            g.setdefault(self.f(x), set()).add(x)
        return sorted("".join(sorted(c)) for c in g.values() if len(c) > 1)


def kruskal(arestas, maximo=False):
    """arestas: lista de (nome, peso) na ordem do texto; empates seguem essa ordem."""
    vs = {c for nome, _ in arestas for c in nome}
    uf = UF(vs)
    aceitas, rejeitadas, passos = [], [], []
    for nome, p in sorted(arestas, key=lambda e: -e[1] if maximo else e[1]):
        if uf.u(nome[0], nome[1]):
            aceitas.append(nome)
        else:
            rejeitadas.append(nome)
        passos.append((nome, nome in aceitas, uf.grupos()))
    return aceitas, rejeitadas, passos


def prim(arestas, raiz):
    vs = sorted({c for nome, _ in arestas for c in nome})
    W = {}
    for nome, p in arestas:
        W[nome[0], nome[1]] = W[nome[1], nome[0]] = p
    chave = {x: inf for x in vs}
    quando = {x: inf for x in vs}  # instante em que a chave foi definida (desempate)
    pai, dentro, t = {}, set(), 0
    chave[raiz], quando[raiz] = 0, 0
    ordem, linhas = [], []
    while len(dentro) < len(vs):
        u = min((x for x in vs if x not in dentro), key=lambda x: (chave[x], quando[x]))
        dentro.add(u)
        if u != raiz:
            ordem.append(pai[u] + u)
        for w in vs:
            if w not in dentro and (u, w) in W and W[u, w] < chave[w]:
                t += 1
                chave[w], pai[w], quando[w] = W[u, w], u, t
        linhas.append((u, ordem[-1] if u != raiz else None,
                       ["*" if x in dentro else chave[x] for x in vs]))
    return ordem, linhas


def peso(arestas, nomes):
    d = dict(arestas)
    return sum(d[n] for n in nomes)


def arvores_geradoras(arestas):
    vs = {c for nome, _ in arestas for c in nome}
    for T in combinations(arestas, len(vs) - 1):
        uf = UF(vs)
        if all(uf.u(n[0], n[1]) for n, _ in T):
            yield [n for n, _ in T], sum(p for _, p in T)


# Árvores geradoras do grafo pequeno (Exemplo 14.1)
peq = [("PQ", 4), ("QR", 2), ("RS", 5), ("SP", 3), ("PR", 1)]
arv = list(arvores_geradoras(peq))
pesos = [p for _, p in arv]
v.igual((len(arv), min(pesos), max(pesos)), (8, 6, 12), "8 árvores, pesos de 6 a 12")
v.igual(sorted(next(t for t, p in arv if p == 6)), ["PR", "QR", "SP"], "a mínima")
v.igual((peso(peq, ["PQ", "QR", "RS"]), peso(peq, ["PQ", "QR", "SP"])), (11, 9), "pesos citados")

# O grafo da Figura 14.2, com os empates na ordem da tabela do Exemplo 14.3
G = [("hg", 1), ("ic", 2), ("gf", 2), ("ab", 4), ("cf", 4), ("ig", 6), ("cd", 7), ("hi", 7),
     ("ah", 8), ("bc", 8), ("de", 9), ("ef", 10), ("bh", 11), ("df", 14)]
aceitas, rejeitadas, passos = kruskal(G)
v.igual(aceitas, ["hg", "ic", "gf", "ab", "cf", "cd", "ah", "de"], "Kruskal: aceitas")
v.igual(rejeitadas, ["ig", "hi", "bc", "ef", "bh", "df"], "Kruskal: rejeitadas")
v.igual(peso(G, aceitas), 37, "custo 37")
v.igual(min(p for _, p in arvores_geradoras(G)), 37, "37 é o mínimo (força bruta)")
for nome, aceita, grupos in passos[:11]:
    txt = "sem mudança" if not aceita else ", ".join("$\\{" + ",".join(g) + "\\}$" for g in grupos)
    if aceita and len(grupos) == 1 and len(grupos[0]) == 9:
        txt = "todos os 9 vértices"
    v.tem(f"${nome}$ & {dict(G)[nome]} & " + ("" if aceita else ""), f"Kruskal passo a passo: {nome}")
    v.tem(txt, f"conjuntos depois de {nome}")
ordem, linhas = prim(G, "a")
v.igual(ordem, ["ab", "ah", "hg", "gf", "fc", "ci", "cd", "de"], "Prim a partir de a")
v.tem(", ".join(f"${o}\\,({dict(G).get(o, dict(G).get(o[::-1]))})$" for o in ordem[:-1]) +
      f" e ${ordem[-1]}\\,(9)$", "ordem do Prim no texto")
for u, aresta, chaves in linhas:
    cel = " & ".join("$\\ast$" if c == "*" else ("$\\infty$" if c == inf else str(c)) for c in chaves)
    v.tem(f"${u}$ & " + (f"${aresta}$" if aresta else "---") + " & " + cel, f"tabela do Prim: {u}")
v.tem("$4+8+1+2+4+2+7+9=37$", "soma das arestas do Prim")
v.igual((round((1000 + 5e5) * log2(1000), -6), round(4000 * log2(1000), -4), 1e6 / 4e4), (5e6, 4e4, 25),
        "vetor ou heap")

# --- Respostas ---
S = [("AB", 6), ("AC", 1), ("AD", 5), ("BC", 5), ("BE", 3), ("CD", 5), ("CE", 6), ("CF", 4),
     ("DF", 2), ("EF", 6)]
aceitas, rejeitadas, _ = kruskal(S)
v.igual((aceitas, peso(S, aceitas)), (["AC", "DF", "BE", "CF", "BC"], 15), "agm-sim: Kruskal")
v.igual(rejeitadas, ["AD", "CD", "AB", "CE", "EF"], "agm-sim: rejeitadas")
v.igual(prim(S, "A")[0], ["AC", "CF", "FD", "CB", "BE"], "agm-sim: Prim")
v.igual(sum(1 for _, p in arvores_geradoras(S) if p == 15), 1, "agm-sim: a AGM é única")
P7 = [("AB", 7), ("AD", 5), ("BC", 8), ("BD", 9), ("BE", 7), ("CE", 5), ("DE", 15), ("DF", 6),
      ("EF", 8), ("EG", 9), ("FG", 11)]
aceitas, rejeitadas, _ = kruskal(P7)
v.igual((aceitas, rejeitadas), (["AD", "CE", "DF", "AB", "BE", "EG"], ["BC", "EF", "BD", "FG", "DE"]),
        "agm-prim7: Kruskal")
v.igual((prim(P7, "A")[0], peso(P7, aceitas)), (["AD", "DF", "AB", "BE", "EC", "EG"], 39), "agm-prim7: Prim")
aceitas, _, _ = kruskal(G, maximo=True)
v.igual((peso(G, aceitas), max(p for _, p in arvores_geradoras(G))), (71, 71), "agm-l7: árvore máxima = 71")
v.igual((2 + 3, 2 + 2), (5, 4), "agm-dijk: árvore de caminhos mínimos x AGM")

v.fim()
