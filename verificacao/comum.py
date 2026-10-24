"""Funções comuns aos scripts de verificação.

Cada script recalcula, em Python, os números de um capítulo (exemplos e
respostas de simulação) e confere que o valor escrito no .tex é o calculado.
A comparação é feita sobre o texto "normalizado": sem espaços, sem $, sem
\\allowbreak, sem chaves e com {,} trocado por vírgula, para que diferenças só
de tipografia não atrapalhem. Exemplo: o trecho $[52,50,41,48,$\\allowbreak$14]$
do .tex vira [52,50,41,48,14].

Uso típico:

    from comum import Verificador
    v = Verificador("02_heaps.tex", "respostas/02.tex")
    v.tem("[78,60,70,39,28,66,33]", "remoção do máximo do Exemplo 2.7")
    v.fim()
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAP = RAIZ / "capitulos"

_SUBS = [(r"\,", ""), (r"\;", ""), (r"\!", ""), (r"\ ", ""), ("~", ""), ("{,}", ",")]
_COMANDOS = re.compile(r"\\(allowbreak|quad|qquad|textbf|mathbf|emph|left|right|"
                       r"displaystyle|small|scriptsize)(?![A-Za-z])")
_RETICENCIAS = re.compile(r"\\[lc]?dots(?![A-Za-z])")


def normaliza(texto):
    texto = re.sub(r"(?<!\\)%.*", "", texto)          # comentários
    for a, b in _SUBS:
        texto = texto.replace(a, b)
    texto = _COMANDOS.sub("", texto)
    texto = _RETICENCIAS.sub("...", texto)
    texto = texto.replace("$", "").replace("{", "").replace("}", "")
    return re.sub(r"\s+", "", texto)


def lista(seq, abre="[", fecha="]", sep=","):
    """[1,2,3] no formato usado no texto."""
    return abre + sep.join(str(x) for x in seq) + fecha


def tupla(seq):
    return lista(seq, "(", ")")


def dec(x, casas=1):
    """Número decimal com vírgula, como no texto: 4,92."""
    return f"{x:.{casas}f}".replace(".", ",")


class Verificador:
    def __init__(self, *arquivos):
        self.nome = Path(sys.argv[0]).stem
        self.textos = {}
        for a in arquivos:
            self.textos[a] = normaliza((CAP / a).read_text(encoding="utf-8"))
        self.ok = 0
        self.falhas = []

    def _onde(self, arquivo):
        return self.textos.items() if arquivo is None else [(arquivo, self.textos[arquivo])]

    def tem(self, trecho, descricao, arquivo=None):
        """Confere que o trecho (já calculado) aparece no .tex."""
        alvo = normaliza(trecho)
        for _, txt in self._onde(arquivo):
            if alvo in txt:
                self.ok += 1
                return True
        lugar = arquivo or ", ".join(self.textos)
        self.falhas.append(f"{descricao}: não encontrei «{trecho}» em {lugar}")
        return False

    def igual(self, calculado, esperado, descricao):
        """Confere um valor calculado contra um valor fixo (usado quando o
        número aparece no texto de forma difícil de procurar)."""
        if calculado == esperado:
            self.ok += 1
            return True
        self.falhas.append(f"{descricao}: calculado {calculado!r}, esperado {esperado!r}")
        return False

    def fim(self):
        if self.falhas:
            print(f"{self.nome}: {len(self.falhas)} divergência(s)")
            for f in self.falhas:
                print("  -", f)
            sys.exit(1)
        print(f"{self.nome}: ok ({self.ok} conferências)")
