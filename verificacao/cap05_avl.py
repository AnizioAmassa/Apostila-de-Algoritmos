#!/usr/bin/env python3
"""Capítulo 5 (ABB e AVL): inserções, remoções e rotações dos exemplos e respostas."""
import re
from math import floor, log2

from comum import Verificador, normaliza

v = Verificador("05_avl.tex", "respostas/05.tex")
# Versão do texto sem os balanços sobrescritos (20^{+1}(...) vira 20(...)),
# para conferir só a forma das árvores escritas por extenso.
SEM_BAL = {a: re.sub(r"\^[+-]?\d", "", t) for a, t in v.textos.items()}


def tem_forma(trecho, descricao, arquivo=None):
    alvo = re.sub(r"\^[+-]?\d", "", normaliza(trecho))
    lugares = SEM_BAL.values() if arquivo is None else [SEM_BAL[arquivo]]
    if any(alvo in t for t in lugares):
        v.ok += 1
    else:
        v.falhas.append(f"{descricao}: não encontrei a árvore «{trecho}»")


class No:
    def __init__(self, k, e=None, d=None):
        self.k, self.e, self.d = k, e, d


def h(t):
    return 0 if t is None else 1 + max(h(t.e), h(t.d))


def bal(t):
    return h(t.d) - h(t.e)


def ser(t, balancos=False):
    """Forma textual usada no livro: 20(10,30(\\cdot,40)); \\cdot = filho vazio."""
    if t is None:
        return r"\cdot"
    b = ""
    if balancos:
        x = bal(t)
        b = "^" + ("+" if x > 0 else "") + str(x)
    if t.e is None and t.d is None:
        return f"{t.k}{b}"
    return f"{t.k}{b}({ser(t.e, balancos)},{ser(t.d, balancos)})"


def rot_dir(p):
    u = p.e
    p.e, u.d = u.d, p
    return u


def rot_esq(p):
    z = p.d
    p.d, z.e = z.e, p
    return z


def rebalanceia(p, log):
    b = bal(p)
    if b == -2:
        if bal(p.e) <= 0:
            log.append(("simples à direita", p.k))
            return rot_dir(p)
        log.append(("dupla à direita", p.k))
        p.e = rot_esq(p.e)
        return rot_dir(p)
    if b == 2:
        if bal(p.d) >= 0:
            log.append(("simples à esquerda", p.k))
            return rot_esq(p)
        log.append(("dupla à esquerda", p.k))
        p.d = rot_dir(p.d)
        return rot_esq(p)
    return p


def ins(t, x, log, avl=True):
    if t is None:
        return No(x)
    if x < t.k:
        t.e = ins(t.e, x, log, avl)
    elif x > t.k:
        t.d = ins(t.d, x, log, avl)
    return rebalanceia(t, log) if avl else t


def rem(t, x, log):
    if t is None:
        return None
    if x < t.k:
        t.e = rem(t.e, x, log)
    elif x > t.k:
        t.d = rem(t.d, x, log)
    else:
        if t.e is None or t.d is None:
            return t.e or t.d
        pred = t.e
        while pred.d is not None:
            pred = pred.d
        t.k = pred.k
        t.e = rem(t.e, pred.k, log)
    return rebalanceia(t, log)


def arvore(chaves, avl=True, base=None):
    log = []
    for x in chaves:
        base = ins(base, x, log, avl)
    return base, log


def de_texto(s):
    """Lê uma árvore no formato 50(30(20(10,25),40),70(60,80))."""
    s = s.replace(" ", "").replace(r"\cdot", ".")
    pos = 0

    def no():
        nonlocal pos
        if s[pos] == ".":
            pos += 1
            return None
        m = re.match(r"\d+", s[pos:])
        pos += m.end()
        t = No(int(m.group()))
        if pos < len(s) and s[pos] == "(":
            pos += 1
            t.e = no()
            pos += 1  # vírgula
            t.d = no()
            pos += 1  # fecha
        return t
    return no()


def emordem(t):
    return [] if t is None else emordem(t.e) + [t.k] + emordem(t.d)


# --- ABB: busca, inserção e remoção (Exemplos 5.1 e 5.2) ---
abb, _ = arvore([50, 30, 70, 20, 40, 60, 80, 10, 25], avl=False)


def caminho(t, x):
    c = []
    while t is not None:
        c.append(t.k)
        t = t.e if x < t.k else (t.d if x > t.k else None)
    return c


v.igual(caminho(abb, 25), [50, 30, 20, 25], "busca por 25: quatro comparações")
v.igual(caminho(abb, 65), [50, 70, 60], "busca por 65 fracassa depois de 60")
abb, _ = arvore([65], avl=False, base=abb)
v.tem("obtemos $10,20,25,30,40,50,60,65,70,80$", "percurso em ordem")
v.igual(emordem(abb), [10, 20, 25, 30, 40, 50, 60, 65, 70, 80], "percurso em ordem")


def rem_abb(t, x):
    if t is None:
        return None
    if x < t.k:
        t.e = rem_abb(t.e, x)
    elif x > t.k:
        t.d = rem_abb(t.d, x)
    else:
        if t.e is None or t.d is None:
            return t.e or t.d
        p = t.e
        while p.d:
            p = p.d
        t.k, t.e = p.k, rem_abb(t.e, p.k)
    return t


for x, forma in ((10, "50(30(20(.,25),40),70(60(.,65),80))"),
                 (60, "50(30(20(10,25),40),70(65,80))"),
                 (30, "50(25(20(10,.),40),70(60(.,65),80))")):
    t = de_texto("50(30(20(10,25),40),70(60(.,65),80))")
    v.igual(ser(rem_abb(t, x)), ser(de_texto(forma)), f"remoção de {x} na ABB")
v.igual((h(arvore([10, 20, 30, 40, 50], avl=False)[0]), h(arvore([30, 20, 40, 10, 50], avl=False)[0])),
        (5, 3), "alturas das duas ordens de inserção")

# Balanços (Exemplo 5.3)
a = de_texto("8(4(2,6),10(.,12))")
b = de_texto("8(4(2(1,.),6),10(.,12(.,14)))")
v.igual((bal(a), bal(a.d), bal(b.d), bal(b)), (0, 1, 2, 0), "balanços das árvores da Figura 5.4")

# Árvores de Fibonacci
N = [None, 1, 2]
for k in range(3, 31):
    N.append(1 + N[-1] + N[-2])
v.tem("$N(1),\\dots,N(8)=" + ",".join(map(str, N[1:9])) + "$", "N(1..8)")
v.igual(max(k for k in range(1, 31) if N[k] <= 10 ** 6), 28, "altura máxima de uma AVL com 10^6 nós")
v.igual(floor(log2(10 ** 6)) + 1, 20, "altura de uma árvore completa com 10^6 nós")
v.igual(max(k for k in range(1, 31) if N[k] <= 32), 6, "AVL com 32 nós")

# Exemplo 5.4: as três linhas da tabela
t = de_texto("20(10,30(.,40))")
log = []
t = ins(t, 5, log)
v.igual((log, ser(t)), ([], "20(10(5,\\cdot),30(\\cdot,40))"), "inserir 5 em 20(10,30(.,40))")
t = ins(t, 50, log)
v.igual((log, ser(t.d)), ([("simples à esquerda", 30)], "40(30,50)"), "inserir 50: rotação em 30")

# Os quatro casos com três chaves
for ordem, rot in (((30, 20, 10), "simples à direita"), ((30, 10, 20), "dupla à direita"),
                   ((10, 20, 30), "simples à esquerda"), ((10, 30, 20), "dupla à esquerda")):
    t, log = arvore(ordem)
    v.igual((ser(t), log[0][0]), ("20(10,30)", rot), f"inserção de {ordem}")

# Remoções pequenas (Exemplo 5.6)
log = []
t = rem(de_texto("20(10,40(30,50))"), 10, log)
v.igual((ser(t, True), log), ("40^-1(20^+1(\\cdot,30^0),50^0)", [("simples à esquerda", 20)]),
        "remover 10 de 20(10,40(30,50))")
tem_forma(r"40^{-1}(20^{+1}(\cdot,30),50)", "remoção de 10, árvore resultante")
log = []
t = rem(de_texto("20(10(.,15),30)"), 30, log)
v.igual((ser(t), log), ("15(10,20)", [("dupla à direita", 20)]), "remover 30 de 20(10(.,15),30)")

# Exemplo 5.7 (= Exercício avl-t5)
t = de_texto("50(30(20(10,25),40),70(60,80))")
logs = []
for x in (5, 15, 35, 45):
    log = []
    t = ins(t, x, log)
    logs.append(log)
v.igual(logs, [[("simples à direita", 30)], [], [("dupla à direita", 50)], []],
        "rotações ao inserir 5, 15, 35 e 45")
final_t5 = ser(t)
tem_forma(final_t5, "árvore final do Exemplo 5.7 / avl-t5", "respostas/05.tex")

# Exemplo 5.8: 40, 20, 10, 30, 35
t, log = arvore([40, 20, 10, 30, 35])
v.igual(log, [("simples à direita", 40), ("dupla à direita", 40)], "rotações de 40,20,10,30,35")
tem_forma(ser(t), "árvore final de 40,20,10,30,35")
# Exemplo 5.9: 10..50 e depois 49
t, log = arvore([10, 20, 30, 40, 50])
v.igual(log, [("simples à esquerda", 10), ("simples à esquerda", 30)], "rotações de 10..50")
tem_forma(ser(t), "árvore depois de 10..50")
t, log = arvore([49], base=t)
v.igual(log, [("simples à esquerda", 20)], "inserir 49")
tem_forma(ser(t), "árvore depois de 49")

# Rubro-negra da Figura 5.10: altura negra 2 em todos os caminhos
rn = {13: ("P", 8, 17), 8: ("V", 1, 11), 17: ("V", 15, 25), 1: ("P", None, 6), 11: ("P", None, None),
      15: ("P", None, None), 25: ("P", 22, 27), 6: ("V", None, None), 22: ("V", None, None),
      27: ("V", None, None)}


def alturas_negras(k):
    if k is None:
        return {1}
    cor, e, d = rn[k]
    return {x + (cor == "P") for x in alturas_negras(e) | alturas_negras(d)}


v.igual({x - 1 for x in alturas_negras(13)}, {2}, "bh(13)=2 (sem contar o 13, contando o nulo)")

# --- Respostas ---
t, log = arvore([1, 2, 3, 4, 5, 6, 7])
v.igual((ser(t), [k for _, k in log]), ("4(2(1,3),6(5,7))", [1, 3, 2, 5]), "avl-1a7")
t17 = t
t, log = arvore([10, 20, 30, 25, 28, 27])
v.igual(log, [("simples à esquerda", 10), ("dupla à direita", 30), ("dupla à esquerda", 20)], "avl-3rot")
tem_forma(ser(t), "avl-3rot: árvore final", "respostas/05.tex")
v.igual(ser(t, True), "25^0(20^-1(10^0,\\cdot),28^0(27^0,30^0))", "avl-3rot com balanços")
logs, t = [], t17
for x in (1, 3, 2):
    log = []
    t = rem(t, x, log)
    logs.append((ser(t, True), log))
v.igual(logs[0], ("4^0(2^+1(\\cdot,3^0),6^0(5^0,7^0))", []), "avl-rem: remover 1")
for forma, _ in logs:
    tem_forma(forma, "avl-rem: árvore depois de cada remoção", "respostas/05.tex")
v.igual(logs[1], ("4^+1(2^0,6^0(5^0,7^0))", []), "avl-rem: remover 3")
v.igual(logs[2], ("6^-1(4^+1(\\cdot,5^0),7^0)", [("simples à esquerda", 4)]), "avl-rem: remover 2")
v.tem("$N(1),\\dots,N(7)=1,2,4,7,12,20,33$", "avl-altmax", "respostas/05.tex")


def catalan(n):
    c = [1]
    for k in range(1, n + 1):
        c.append(sum(c[i] * c[k - 1 - i] for i in range(k)))
    return c


v.igual(catalan(6), [1, 1, 2, 5, 14, 42, 132], "avl-catalan")
log = []
t = rem(de_texto(final_t5), 30, log)
v.igual(log, [("simples à direita", 20)], "avl-rem30: rotação")
tem_forma(ser(t), "avl-rem30: árvore final", "respostas/05.tex")
t, log = arvore([3, 2, 1, 4, 5, 6, 7, 16, 15, 14])
v.igual(log, [("simples à direita", 3), ("simples à esquerda", 3), ("simples à esquerda", 2),
              ("simples à esquerda", 5), ("dupla à esquerda", 7), ("dupla à esquerda", 6)], "avl-seq")
v.igual(ser(t, True), "4^+1(2^0(1^0,3^0),7^0(6^-1(5^0,\\cdot),15^0(14^0,16^0)))", "avl-seq: árvore final")
tem_forma(ser(t), "avl-seq: árvore final", "respostas/05.tex")


# avl-l3: árvore de Fibonacci de altura 7 (33 nós), removendo a folha 33
def fib(hh, prox):
    if hh == 0:
        return None
    if hh == 1:
        return No(next(prox))
    e = fib(hh - 1, prox)
    t = No(next(prox))
    t.e, t.d = e, fib(hh - 2, prox)
    return t


t = fib(7, iter(range(1, 34)))
v.igual((len(emordem(t)), t.k, caminho(t, 33)), (33, 21, [21, 29, 32, 33]), "avl-l3: a árvore")
log = []
rem(t, 33, log)
v.igual([k for _, k in log], [32, 29, 21], "avl-l3: rotações em todos os ancestrais")

v.fim()
