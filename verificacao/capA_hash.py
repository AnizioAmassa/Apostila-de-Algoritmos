#!/usr/bin/env python3
"""Apêndice A (tabelas hash)."""
from math import ceil, floor, prod, sqrt

from comum import Verificador

v = Verificador("A_hash.tex", "respostas/A.tex")
R = "respostas/A.tex"
A_OURO = 0.6180339887


def mult(k, m, A=A_OURO):
    return floor(m * ((k * A) % 1))


def horner(s, b, m):
    h, passos = 0, []
    for ch in s:
        h = (h * b + (ord(ch) - ord("a") + 1)) % m
        passos.append(h)
    return passos


def aberto(chaves, m, sonda):
    """Endereçamento aberto; sonda(k, i) dá a i-ésima posição. Devolve a tabela
    e o número de sondagens de cada inserção."""
    T, sond = [None] * m, {}
    for k in chaves:
        for i in range(m):
            p = sonda(k, i)
            if T[p] is None:
                T[p], sond[k] = k, i + 1
                break
    return T, sond


def encadeia(chaves, m):
    L = {}
    for k in chaves:
        L.setdefault(k % m, []).insert(0, k)  # inserção no início da lista
    return L


def primo(n):
    return n > 1 and all(n % d for d in range(2, int(sqrt(n)) + 1))


# Exemplo A.1
v.igual([k % 7 for k in (201345002, 731000006, 555777016)], [5, 2, 4], "matrículas mod 7")
v.tem("vão para os endereços 5, 2 e 4", "endereços no texto")
# Calculando endereços
v.igual((100 % 13, 2026 % 13), (9, 11), "divisão com m=13")
v.igual((mult(100, 16), mult(101, 16)), (12, 6), "multiplicação com m=16")
v.tem("$100A\\approx61{,}8034$", "100A")
v.tem("$101A\\approx62{,}4214$", "101A")
v.igual(horner("gato", 31, 97), [7, 24, 85, 31], "Horner para gato")
uni = lambda a, b, k: ((a * k + b) % 17) % 6
v.igual((uni(3, 4, 5), uni(3, 4, 9), uni(5, 1, 5), uni(5, 1, 9)), (2, 2, 3, 0), "hashing universal")
# Paradoxo do aniversário
v.igual(1 - prod((365 - i) / 365 for i in range(23)) > 0.5, True, "23 pessoas: mais de 50%")
v.igual(1 - prod((365 - i) / 365 for i in range(22)) > 0.5, False, "22 pessoas: menos de 50%")
# Encadeamento exterior
L = encadeia([12, 44, 13, 88, 23, 94, 11, 39, 20, 16, 5], 11)
for pos, lst in sorted(L.items()):
    v.tem(f"{pos}/{{" + ",".join(map(str, lst)) + "}", f"figura do encadeamento: lista {pos}")
v.igual(L[0], [11, 88, 44], "lista do endereço 0")
# Sondagem linear (Exemplo A.5)
T, sond = aberto([18, 41, 22, 44, 59, 32, 31, 73], 13, lambda k, i: (k % 13 + i) % 13)
v.tem("{" + ",".join("{}" if x is None else str(x) for x in T) + "}", "figura da sondagem linear")
v.tem("{" + ",".join(f"{T.index(k)}/{s}" for k, s in sorted(sond.items(), key=lambda t: T.index(t[0]))) + "}",
      "sondagens de cada chave na figura")
v.igual((sond[44], sond[32], sond[31], sond[73], T.index(31), T.index(73)), (2, 3, 6, 4, 10, 11),
        "sondagens citadas no texto")
v.igual([p for p in range(13) if T[p] is not None and 5 <= p <= 11], list(range(5, 12)), "agrupamento 5..11")
v.igual([(5 + i * i) % 13 for i in range(4)], [5, 6, 9, 1], "sondagem quadrática do 31")
h2 = 1 + 31 % 11
v.igual((h2, [(5 + i * h2) % 13 for i in range(6)]), (10, [5, 2, 12, 9, 6, 3]), "duplo hashing do 31")
# Dimensionando a tabela
v.igual((600 / 800, 1 / (1 - 600 / 800), round(1 / (1 - 600 / 650))), (0.75, 4.0, 13), "fator de carga")

# --- Respostas ---
ch = [10, 22, 31, 4, 15, 28, 17, 88, 59]
fmt = lambda T: ",".join("-" if x is None else str(x) for x in T)
lin, _ = aberto(ch, 11, lambda k, i: (k % 11 + i) % 11)
qua, _ = aberto(ch, 11, lambda k, i: (k % 11 + i + 3 * i * i) % 11)
dup, _ = aberto(ch, 11, lambda k, i: (k % 11 + i * (1 + k % 10)) % 11)
v.tem("Linear: $" + fmt(lin) + "$", "hs-abertos (a)", R)
v.tem("Quadrática: $" + fmt(qua) + "$", "hs-abertos (b)", R)
v.tem("Duplo hashing: $" + fmt(dup) + "$", "hs-abertos (c)", R)
L = {p: sorted(l, key=lambda k: [5, 28, 19, 15, 20, 33, 12, 17, 10].index(k))
     for p, l in encadeia([5, 28, 19, 15, 20, 33, 12, 17, 10], 9).items()}
v.igual(L, {5: [5], 1: [28, 19, 10], 6: [15, 33], 2: [20], 3: [12], 8: [17]}, "hs-encad")
v.igual(max(map(len, L.values())), 3, "hs-encad: maior lista")
v.igual((1000 / 500, 1 / (1 - 0.5), round(1 / (1 - 0.9))), (2.0, 2.0, 10), "hs-carga e hs-sondagens")
v.igual((mult(123456, 1000), mult(123457, 1000)), (4, 622), "hs-mult")
v.tem("$123456\\cdot A\\approx76300{,}0041$", "hs-mult", R)
v.tem("$123457\\cdot A\\approx76300{,}6221$", "hs-mult", R)
v.igual((round(123456 * A_OURO, 4), round(123457 * A_OURO, 4)), (76300.0041, 76300.6221), "hs-mult: produtos")
v.igual((ceil(10 ** 6 / 0.75), primo(1333357)), (1333334, True), "hs-tamanho")
v.igual(next(n for n in range(1333334, 1400000) if primo(n)), 1333357, "hs-tamanho: o primeiro primo acima")

v.fim()
