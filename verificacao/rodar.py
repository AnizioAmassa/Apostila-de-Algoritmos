#!/usr/bin/env python3
"""Roda todas as verificações: a integridade dos exercícios e os scripts
verificacao/cap*.py, que recalculam os números dos exemplos e das respostas.
Sai com código 1 se alguma falhar."""
import subprocess
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent


def main():
    scripts = [PASTA / "integridade.py"] + sorted(PASTA.glob("cap*.py"))
    falhas = []
    for s in scripts:
        r = subprocess.run([sys.executable, str(s)])
        if r.returncode != 0:
            falhas.append(s.name)
    print()
    if falhas:
        print(f"{len(falhas)} verificação(ões) falharam: {', '.join(falhas)}")
        sys.exit(1)
    print(f"Todas as {len(scripts)} verificações passaram.")


if __name__ == "__main__":
    main()
