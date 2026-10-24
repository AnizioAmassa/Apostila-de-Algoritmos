#!/usr/bin/env python3
"""Resume o apostila.log: erros, avisos, referências indefinidas, rótulos
duplicados e caixas estouradas. Sai com código 1 se houver qualquer um deles.

Uso: python3 verificacao/log.py [apostila.log]"""
import re
import sys
from pathlib import Path

PADROES = [
    ("erros", re.compile(r"^! ")),
    ("referências indefinidas", re.compile(r"(Reference|Citation) `[^']*' on page .* undefined")),
    ("rótulos duplicados", re.compile(r"Label `[^']*' multiply defined")),
    ("linhas estouradas (overfull)", re.compile(r"^Overfull \\[hv]box")),
    ("caixas frouxas (underfull)", re.compile(r"^Underfull \\[hv]box")),
    ("avisos", re.compile(r"Warning", re.I)),
]


def main():
    log = Path(sys.argv[1] if len(sys.argv) > 1 else "apostila.log")
    if not log.exists():
        sys.exit(f"{log} não existe: compile antes com 'make -C AI-helper pdf'.")
    linhas = log.read_text(encoding="latin-1").splitlines()
    achados = {nome: [] for nome, _ in PADROES}
    for i, linha in enumerate(linhas):
        if linha.startswith("Package: infwarerr"):
            continue  # nome de pacote, não é aviso
        for nome, padrao in PADROES:
            if padrao.search(linha):
                contexto = " ".join(linhas[i:i + 2]).strip()
                achados[nome].append(contexto[:160])
                break
    problemas = 0
    for nome, lista in achados.items():
        print(f"{nome}: {len(lista)}")
        for item in lista[:15]:
            print("   ", item)
        if len(lista) > 15:
            print(f"    ... e mais {len(lista) - 15}")
        problemas += len(lista)
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
