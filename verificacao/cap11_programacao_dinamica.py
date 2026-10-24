#!/usr/bin/env python3
"""Capítulo 11 (programação dinâmica): LCS, cadeia de matrizes, mochila e respostas."""
from functools import lru_cache
from itertools import combinations, permutations

from comum import Verificador

v = Verificador("11_programacao_dinamica.tex", "respostas/11.tex")
R = "respostas/11.tex"


# ---------- Fibonacci ----------
def chamadas(n, cont):
    cont[n] = cont.get(n, 0) + 1
    if n > 1:
        chamadas(n - 1, cont)
        chamadas(n - 2, cont)


cont = {}
chamadas(5, cont)
v.igual((sum(cont.values()), cont[3], cont[2], cont[1]), (15, 2, 3, 5), "chamadas para F_5")
c = [1, 1]
for n in range(2, 41):
    c.append(c[-1] + c[-2] + 1)
v.igual((c[30], c[40]), (2692537, 331160281), "c(30) e c(40)")
v.tem("$c(30)=2\\,692\\,537$ e $c(40)=331\\,160\\,281$", "c(30) e c(40) no texto")


# ---------- LCS ----------
def lcs_tabela(x, y):
    C = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            C[i][j] = C[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(C[i - 1][j], C[i][j - 1])
    return C


def lcs_reconstroi(x, y, C):
    i, j, z, visitadas, casadas = len(x), len(y), [], [], []
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            casadas.append((i, j))
            z.insert(0, x[i - 1])
            i, j = i - 1, j - 1
        else:
            visitadas.append((i, j))
            if C[i - 1][j] >= C[i][j - 1]:
                i -= 1
            else:
                j -= 1
    return z, visitadas, casadas


def todas_lcs(x, y):
    C = lcs_tabela(x, y)

    @lru_cache(None)
    def rec(i, j):
        if i == 0 or j == 0:
            return {()}
        if x[i - 1] == y[j - 1]:
            return {s + (x[i - 1],) for s in rec(i - 1, j - 1)}
        r = set()
        if C[i - 1][j] >= C[i][j - 1]:
            r |= rec(i - 1, j)
        if C[i][j - 1] >= C[i - 1][j]:
            r |= rec(i, j - 1)
        return r
    return sorted("".join(map(str, s)) if isinstance(x, str) else s for s in rec(len(x), len(y)))


X, Y = "ABCBDAB", "BDCABA"
C = lcs_tabela(X, Y)
z, visitadas, casadas = lcs_reconstroi(X, Y, C)
v.igual((C[7][6], "".join(z)), (4, "BCBA"), "LCS de ABCBDAB e BDCABA")
v.igual((C[2][1], C[2][4], C[1][4], C[2][3]), (1, 1, 1, 1), "células citadas")
for i in range(len(X) + 1):
    v.tem(f"{i}/{{" + ",".join(map(str, C[i])) + "}", f"figura da LCS, linha {i}")
v.tem(",".join(f"{i}/{j}" for i, j in visitadas), "células amarelas da reconstrução")
v.tem(",".join(f"{i}/{j}" for i, j in casadas), "células verdes da reconstrução")
v.igual(todas_lcs(X, Y), ["BCAB", "BCBA", "BDAB"], "todas as LCS de tamanho 4")
v.tem("são exatamente BCAB, BCBA e BDAB", "todas as LCS no texto")
x2, y2 = (5, 2, 1, 3, 9, 10, 14), (2, 3, 1, 10)
v.igual((lcs_tabela(x2, y2)[-1][-1], todas_lcs(x2, y2)), (3, [(2, 1, 10), (2, 3, 10)]),
        "LCS de 5,2,1,3,9,10,14 e 2,3,1,10")


# ---------- Cadeia de matrizes ----------
def cadeia(r):
    n = len(r) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    for d in range(1, n):
        for i in range(1, n - d + 1):
            j = i + d
            m[i][j] = float("inf")
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + r[i - 1] * r[k] * r[j]
                if q < m[i][j]:
                    m[i][j], s[i][j] = q, k
    return m, s


def parentiza(s, i, j, letra="M"):
    if i == j:
        return f"{letra}_{i}"
    return "(" + parentiza(s, i, s[i][j], letra) + parentiza(s, s[i][j] + 1, j, letra) + ")"


def custo_arvore(expr, r):
    """Custo de uma parentização dada como árvore aninhada de índices."""
    if isinstance(expr, int):
        return 0, (r[expr - 1], r[expr])
    ce, (a, b) = custo_arvore(expr[0], r)
    cd, (_, c) = custo_arvore(expr[1], r)
    return ce + cd + a * b * c, (a, c)


r = (20, 50, 10, 1, 100)
m, s = cadeia(r)
v.igual((m[1][4], parentiza(s, 1, 4)), (3500, "((M_1(M_2M_3))M_4)"), "ordem ótima do Exemplo 11.4")
custos = {
    "((M_1M_2)M_3)M_4": custo_arvore((((1, 2), 3), 4), r)[0],
    "(M_1(M_2M_3))M_4": custo_arvore(((1, (2, 3)), 4), r)[0],
    "(M_1M_2)(M_3M_4)": custo_arvore(((1, 2), (3, 4)), r)[0],
    "M_1((M_2M_3)M_4)": custo_arvore((1, ((2, 3), 4)), r)[0],
    "M_1(M_2(M_3M_4))": custo_arvore((1, (2, (3, 4))), r)[0],
}
v.igual(custos, {"((M_1M_2)M_3)M_4": 12200, "(M_1(M_2M_3))M_4": 3500, "(M_1M_2)(M_3M_4)": 31000,
                 "M_1((M_2M_3)M_4)": 105500, "M_1(M_2(M_3M_4))": 151000}, "as cinco parentizações")
v.tem("$1000+50\\,000+100\\,000=\\mathbf{151\\,000}$", "custo da pior ordem")
v.tem("$10\\,000+200+2000=\\mathbf{12\\,200}$", "custo de ((M1M2)M3)M4")
v.tem("$500+1000+2000=\\mathbf{3500}$", "custo da melhor ordem")
for (i, j), txt in {(1, 2): "10\\,000 (1)", (1, 3): "1500 (1)", (1, 4): "\\textbf{3500 (3)}",
                    (2, 3): "500 (2)", (2, 4): "5500 (3)", (3, 4): "1000 (3)"}.items():
    v.tem(txt, f"tabela m[{i},{j}]")
    v.igual(f"{m[i][j]} ({s[i][j]})", txt.replace("\\,", "").replace("\\textbf{", "").rstrip("}"),
            f"m[{i},{j}] e s[{i},{j}]")
v.tem("$0+500+20\\cdot50\\cdot1=1500$", "m[1,3] com k=1")
v.tem("$10\\,000+0+20\\cdot10\\cdot1=10\\,200$", "m[1,3] com k=2")
for dims, custo, ordem in (((10, 100, 5, 50), 7500, "((M_1M_2)M_3)"),
                           ((5, 10, 3, 12, 5, 50, 6), 2010, "((M_1M_2)((M_3M_4)(M_5M_6)))"),
                           ((30, 35, 15, 5, 10, 20, 25), 15125, "((M_1(M_2M_3))((M_4M_5)M_6))")):
    m2, s2 = cadeia(dims)
    n = len(dims) - 1
    v.igual((m2[1][n], parentiza(s2, 1, n)), (custo, ordem), f"cadeia {dims}")
    v.tem(ordem, f"ordem ótima de {dims}")
v.tem("$m[1,2]=5000$ e $m[2,3]=25\\,000$", "células de (10,100,5,50)")


# ---------- Mochila ----------
def mochila(itens, W):
    n = len(itens)
    M = [[0] * (n + 1) for _ in range(W + 1)]
    for i, (p, val) in enumerate(itens, 1):
        for w in range(W + 1):
            M[w][i] = M[w][i - 1]
            if p <= w and val + M[w - p][i - 1] > M[w][i]:
                M[w][i] = val + M[w - p][i - 1]
    w, escolhidos = W, []
    for i in range(n, 0, -1):
        if M[w][i] != M[w][i - 1]:
            escolhidos.append(i)
            w -= itens[i - 1][0]
    return M, M[W][n], sorted(escolhidos)


def guloso_razao(itens, W):
    tot = 0
    for p, val in sorted(itens, key=lambda t: -t[1] / t[0]):
        if p <= W:
            W -= p
            tot += val
    return tot


itens = [(1, 2), (3, 7), (2, 1)]
M, otimo, esc = mochila(itens, 4)
v.igual((otimo, esc), (9, [1, 2]), "mochila do Exemplo 11.6")
for w in range(5):
    v.tem(f"{w}/{{" + ",".join(str(M[w][i]) for i in range(4)) + "}", f"figura da mochila, w={w}")
v.tem("$M(4,2)=\\max\\{M(4,1),\\,7+M(1,1)\\}=\\max\\{2,\\,9\\}=9$", "célula M(4,2)")
itens = [(10, 60), (20, 100), (30, 120)]
_, otimo, esc = mochila(itens, 50)
v.igual((otimo, esc, guloso_razao(itens, 50)), (220, [2, 3], 160), "mochila com W=50")
# w decrescente x crescente
K = [0] * 5
for w in range(4, 1, -1):
    K[w] = max(K[w], K[w - 2] + 3)
K2 = [0] * 5
for w in range(2, 5):
    K2[w] = max(K2[w], K2[w - 2] + 3)
v.igual((K, K2), ([0, 0, 3, 3, 3], [0, 0, 3, 3, 6]), "vetor único decrescente e crescente")

# ---------- Respostas ----------
a = [5, 2, 8, 6, 3, 6, 9, 7]
L = []
for i, x in enumerate(a):
    L.append(1 + max([L[j] for j in range(i) if a[j] < x], default=0))
v.igual((L, max(L)), ([1, 1, 2, 2, 2, 3, 4, 4], 4), "pd-lis")
v.tem("dá $L=1,1,2,2,2,3,4,4$ e resposta 4", "pd-lis", R)


def pal(s):
    @lru_cache(None)
    def P(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        return 2 + P(i + 1, j - 1) if s[i] == s[j] else max(P(i + 1, j), P(i, j - 1))
    return P(0, len(s) - 1)


v.igual(pal("character"), 5, "pd-pal")
v.igual("carac" == "carac"[::-1] and all(ch in "character" for ch in "carac"), True, "carac é palíndromo")
K = [0] * 11
for w in range(11):
    K[w] = max([0] + [K[w - p] + val for p, val in [(3, 5), (4, 7), (2, 3)] if p <= w])
v.igual(K[10], 17, "pd-ilim")


def corte(n, pontos):
    L = [0] + sorted(pontos) + [n]

    @lru_cache(None)
    def C(i, j):
        if j == i + 1:
            return 0
        return L[j] - L[i] + min(C(i, k) + C(k, j) for k in range(i + 1, j))
    return C(0, len(L) - 1)


def custo_ordem(n, ordem):
    pedacos, total = [(0, n)], 0
    for c in ordem:
        for a_, b_ in pedacos:
            if a_ < c < b_:
                total += b_ - a_
                pedacos.remove((a_, b_))
                pedacos += [(a_, c), (c, b_)]
                break
    return total


v.igual(corte(20, [2, 8, 10]), 38, "pd-corte: ótimo")
v.igual(sorted(custo_ordem(20, o) for o in permutations([2, 8, 10])), [38, 38, 40, 40, 46, 50],
        "pd-corte: as seis ordens")
v.igual((custo_ordem(20, [2, 8, 10]), custo_ordem(20, [10, 8, 2])), (50, 38), "pd-corte: do enunciado")
v.tem("as seis ordens custam $50,46,40,40,38,38$", "pd-corte", R)
v.igual(todas_lcs("dacdba", "cadcda"), ["acda", "dcda"], "pd-apa (a)")
itens = [(20, 50), (30, 70), (40, 90), (50, 120), (60, 140)]
_, otimo, esc = mochila(itens, 100)
v.igual((otimo, esc), (240, [1, 2, 4]), "pd-apa (b)")
m2, s2 = cadeia((5, 10, 3, 12, 5, 50, 6))
v.igual((m2[1][6], parentiza(s2, 1, 6, "A")), (2010, "((A_1A_2)((A_3A_4)(A_5A_6)))"), "pd-l6a (a)")
v.tem("((A_1A_2)((A_3A_4)(A_5A_6)))", "pd-l6a (a)", R)

pal_ = ["case", "else", "end", "if", "of", "then"]
freq = [15, 5, 5, 35, 5, 35]


@lru_cache(None)
def abb(i, j):
    if i > j:
        return 0, None
    melhor = None
    for r_ in range(i, j + 1):
        cst = abb(i, r_ - 1)[0] + abb(r_ + 1, j)[0]
        if melhor is None or cst < melhor[0]:
            melhor = (cst, r_)
    return melhor[0] + sum(freq[i:j + 1]), melhor[1]


v.igual((abb(0, 5)[0], pal_[abb(0, 5)[1]]), (185, "if"), "pd-l6b (b): custo 185 com raiz if")
v.igual((pal_[abb(0, 2)[1]], pal_[abb(1, 2)[1]], pal_[abb(4, 5)[1]]), ("case", "else", "then"),
        "pd-l6b (b): subárvores")
a = [1, 101, 2, 3, 100, 4, 5]
S = []
for i, x in enumerate(a):
    S.append(x + max([S[j] for j in range(i) if a[j] < x], default=0))
v.igual(max(S), 106, "pd-l6c (a)")
f = [None, 2, 2]
for n in range(3, 8):
    f.append(f[-1] + f[-2])
v.igual(f[1:], [2, 2, 4, 6, 10, 16, 26], "pd-l6c (d)")


def bandeiras(n):
    """Força bruta: sem faixas vizinhas iguais e azul entre branca e vermelha."""
    tot = 0
    for s in __import__("itertools").product("BAV", repeat=n):
        if any(s[i] == s[i + 1] for i in range(n - 1)):
            continue
        ok = all(0 < i < n - 1 and {s[i - 1], s[i + 1]} == {"B", "V"} for i in range(n) if s[i] == "A")
        tot += ok
    return tot


v.igual([bandeiras(n) for n in range(1, 8)], f[1:], "pd-l6c (d) por força bruta")
pesos = [2, 7, 5, 2]
alc = [{0}]
for p in pesos:
    alc.append(alc[-1] | {x + p for x in alc[-1]})
for i in (3, 4):
    linha = []
    for w in range(15):
        if w in alc[i - 1]:
            linha.append("O")
        elif w - pesos[i - 1] in alc[i - 1]:
            linha.append("I")
        else:
            linha.append("-")
    v.tem("\\texttt{" + " ".join(linha) + "}", f"pd-mc458 (a), item {i}", R)


def edicao(x, y):
    D = [[i + j if i * j == 0 else 0 for j in range(len(y) + 1)] for i in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (x[i - 1] != y[j - 1]))
    return D[-1][-1]


v.igual(edicao("kitten", "sitting"), 3, "pd-edit")
T = [0]
for s_ in range(1, 11):
    T.append(1 + min(T[s_ - c_] for c_ in (1, 3, 4) if c_ <= s_))
v.tem("são $" + ",".join(map(str, T)) + "$", "pd-troco", R)
p = [1, 5, 8, 9, 10, 17, 17, 20]
rr = [0]
for n in range(1, 9):
    rr.append(max(p[i - 1] + rr[n - i] for i in range(1, n + 1)))
v.tem("são $" + ",".join(map(str, rr[1:])) + "$", "pd-haste", R)


def caminhos(bloq):
    P = [[0] * 5 for _ in range(5)]
    for i in range(1, 5):
        for j in range(1, 5):
            if (i, j) in bloq:
                continue
            P[i][j] = 1 if (i, j) == (1, 1) else P[i - 1][j] + P[i][j - 1]
    return P[4][4]


v.igual((caminhos(set()), caminhos({(2, 2)})), (20, 8), "pd-grade")


def particao(a):
    s = sum(a)
    return s % 2 == 0 and any(sum(c_) == s // 2 for k in range(len(a) + 1) for c_ in combinations(a, k))


v.igual((particao([3, 1, 1, 2, 2, 1]), particao([2, 3, 7])), (True, False), "pd-part")
P = [None, 1]
for n in range(2, 7):
    P.append(sum(P[k] * P[n - k] for k in range(1, n)))
v.tem("são $" + ",".join(map(str, P[1:])) + "$", "pd-catalan", R)


def formas(S, moedas=(1, 2, 5)):
    F = [1] + [0] * S
    for c_ in moedas:
        for s_ in range(c_, S + 1):
            F[s_] += F[s_ - c_]
    return F[S]


v.igual((formas(5), formas(10)), (4, 10), "pd-formas")


def maior_substring(x, y):
    melhor = (0, "")
    L = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
                if L[i][j] > melhor[0]:
                    melhor = (L[i][j], x[i - L[i][j]:i])
    return melhor


v.igual(maior_substring("ABABC", "BABCA"), (4, "BABC"), "pd-substring")

v.fim()
