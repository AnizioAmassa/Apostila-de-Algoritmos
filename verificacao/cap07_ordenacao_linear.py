#!/usr/bin/env python3
"""Capítulo 7 (ordenação linear): counting, radix, bucket e American Flag."""
from math import floor, log2

from comum import Verificador, dec, lista, tupla

v = Verificador("07_ordenacao_linear.tex", "respostas/07.tex")


def counting(a, k):
    c = [0] * (k + 1)
    for x in a:
        c[x[0] if isinstance(x, tuple) else x] += 1
    contado = list(c)
    for i in range(1, k + 1):
        c[i] += c[i - 1]
    acumulado = list(c)
    b = [None] * len(a)
    passos = []
    for j in range(len(a) - 1, -1, -1):
        x = a[j]
        chave = x[0] if isinstance(x, tuple) else x
        b[c[chave] - 1] = x
        passos.append((j + 1, x, c[chave]))
        c[chave] -= 1
    return contado, acumulado, b, passos


def radix(nums, digitos, base=10):
    passadas, lista_ = [], list(nums)
    for d in range(digitos):
        filas = [[] for _ in range(base)]
        for x in lista_:
            filas[(x // base ** d) % base].append(x)
        lista_ = [x for f in filas for x in f]
        passadas.append(list(lista_))
    return passadas


def radix_str(palavras):
    L = max(map(len, palavras))
    passadas, lista_ = [], list(palavras)
    for pos in range(L - 1, -1, -1):
        lista_ = sorted(lista_, key=lambda w: w[pos] if pos < len(w) else "")  # sorted é estável
        passadas.append(list(lista_))
    return passadas


def baldes(nums, r=10):
    bs = {}
    for x in nums:
        bs.setdefault(floor(r * x), []).append(x)
    return bs


# Counting sort (Exemplo 7.1)
A = [(4, "a"), (1, "a"), (3, ""), (1, "b"), (0, ""), (4, "b"), (1, "c")]
contado, acumulado, B, passos = counting(A, 4)
v.tem("$C=" + tupla(contado) + "$", "contagem")
v.tem("$C=" + tupla(acumulado) + "$", "acumulação")
v.tem("\\vetorz{" + ",".join(map(str, contado)) + "}", "figura: C contado")
v.tem("\\vetorz{" + ",".join(map(str, acumulado)) + "}", "figura: C acumulado")
for j, (val, et), pos in passos:
    nome = f"{val}_{et}" if et else str(val)
    v.tem(f"$j={j}$: ${nome}$ vai para $B[C[{val}]]=B[{pos}]$; $C[{val}]:={pos - 1}$",
          f"distribuição, j={j}")
v.igual([f"{x}{e}" for x, e in B], ["0", "1a", "1b", "1c", "3", "4a", "4b"], "saída estável")

v.igual(round(1000 * log2(1000), -3), 10_000, "mergesort de 1000 números: cerca de 10^4")

# Radix sort na base 10 (Exemplo 7.2)
entrada = [102, 313, 690, 131, 222, 670, 690, 130, 79, 102]
p = radix(entrada, 3)
for nome, lst in zip(("unidades", "dezenas", "centenas"), p):
    v.tem(f"{nome}: $" + "\\ ".join(f"{x:03d}" for x in lst) + "$", f"radix: passada pelas {nome}")
v.igual(radix([23, 21, 13], 2), [[21, 23, 13], [13, 21, 23]], "radix de 23, 21, 13")
def digitos(x, b):
    d = 0
    while x:
        x, d = x // b, d + 1
    return d


for b, d in ((10, 6), (100, 3), (1000, 2), (10 ** 6, 1)):
    v.igual(digitos(10 ** 6 - 1, b), d, f"dígitos de números < 10^6 na base {b}")

# Chaves de tamanhos variados
grupos = {}
for x in (7, 42, 3, 105, 18):
    grupos.setdefault(len(str(x)), []).append(x)
v.igual([sorted(g) for _, g in sorted(grupos.items())], [[3, 7], [18, 42], [105]], "grupos por dígitos")
v.tem("a concatenação $3,7,18,42,105$", "concatenação dos grupos")
v.igual(radix_str(["ba", "a", "ab"]), [["a", "ba", "ab"], ["a", "ab", "ba"]], "strings com ⊥")

# Bucket sort (Exemplo 7.3)
nums = [0.42, 0.07, 0.93, 0.15, 0.48, 0.61, 0.11, 0.88, 0.44, 0.35]
bs = baldes(nums)
v.igual((len(bs[4]), len(bs[1]), sorted(set(range(10)) - set(bs))), (3, 2, [2, 5, 7]), "baldes cheios e vazios")
v.tem("; ".join(dec(x, 2) for x in sorted(nums)), "saída do bucket sort")
for b, conteudo in bs.items():
    v.tem(f"{b}/{{" + ",".join(dec(x, 2) for x in sorted(conteudo)) + "}", f"figura: balde {b}")

# American Flag (Exemplo 7.4)
A = [52, 17, 34, 19, 58, 31, 12, 36]
dig = lambda x: x // 10
cont = {d: sum(dig(x) == d for x in A) for d in sorted(set(map(dig, A)))}
inicio, acc = {}, 0
for d, c in cont.items():
    inicio[d], acc = acc, acc + c
prox = dict(inicio)
trocas = []
for d in cont:
    while prox[d] < inicio[d] + cont[d]:
        x = A[prox[d]]
        if dig(x) == d:
            prox[d] += 1
        else:
            e = dig(x)
            A[prox[d]], A[prox[e]] = A[prox[e]], A[prox[d]]
            trocas.append((x, A[prox[d]]))
            prox[e] += 1
v.igual(A, [12, 17, 19, 34, 36, 31, 52, 58], "vetor depois da passada pelas dezenas")
v.igual(trocas, [(52, 12), (34, 19), (58, 36)], "as três trocas")
v.igual([inicio[d] + 1 for d in cont], [1, 4, 7], "início dos blocos")
v.tem("2/{" + ",".join(map(str, A)) + "}", "figura do American Flag")

v.igual(round(10 ** 7 * log2(10 ** 7) / 1e8, 1), 2.3, "(A): n log2 n ≈ 2,3·10^8")

# --- Respostas ---
contado, acumulado, B, _ = counting([2, 5, 3, 0, 2, 3, 0, 3], 5)
v.tem("Contagens: $C=" + lista(contado) + "$", "sl-count: contagens", "respostas/07.tex")
v.tem("$C=" + lista(acumulado) + "$", "sl-count: acumuladas", "respostas/07.tex")
v.tem("$B=" + lista(B) + "$", "sl-count: saída", "respostas/07.tex")
p = radix([329, 457, 657, 839, 436, 720, 355], 3)
for nome, lst in zip(("unidades", "dezenas", "centenas"), p):
    v.tem(f"Pelas {nome}: $" + ",".join(map(str, lst)) + "$", f"sl-radix: {nome}", "respostas/07.tex")
pal = "COW DOG SEA RUG ROW MOB BOX TAB BAR EAR TAR DIG BIG TEA NOW FOX".split()
for nome, lst in zip(("terceira", "segunda", "primeira"), radix_str(pal)):
    v.tem(f"Pela {nome}" + (" letra" if nome == "terceira" else "") + ": " + " ".join(lst),
          f"sl-strtrace: {nome} letra", "respostas/07.tex")
nums = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
for b, conteudo in sorted(baldes(nums).items()):
    v.tem(f"Balde {b}: $" + ";".join(dec(x, 2) for x in conteudo) + "$", f"sl-buckettrace: balde {b}",
          "respostas/07.tex")
v.tem(";".join(dec(x, 2) for x in sorted(nums)), "sl-buckettrace: saída", "respostas/07.tex")
v.igual([32 // b for b in (4, 8, 16)], [8, 4, 2], "sl-base: passadas")
v.igual(12 * (10 ** 6 + 10), 12_000_120, "sl-t2 (B): 12 passadas ≈ 1,2·10^7")
v.igual(2 * 10 ** 9 < 2 ** 31, True, "sl-t2 (D): chaves em [0,2·10^9] têm cerca de 31 bits")

v.fim()
