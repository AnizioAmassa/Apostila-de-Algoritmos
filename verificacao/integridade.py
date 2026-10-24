#!/usr/bin/env python3
"""Integridade dos exercícios e das respostas.

Compara, com o commit de referência 9a09ba5, a seção "Exercícios" de cada
capítulo e os arquivos de capitulos/respostas/. As únicas mudanças aceitas são:

  * o argumento opcional <...> acrescentado ao cabeçalho de um exercício,
    logo depois de \\begin{exercicio}{rótulo}[origem] (ele só imprime
    "ver §X", sem tocar no enunciado);
  * exercícios novos (com rótulos novos) acrescentados ao FIM da seção;
  * respostas novas acrescentadas ao FIM do arquivo de respostas do capítulo,
    na mesma ordem dos exercícios novos.

Além disso, confere que todo exercício tem exatamente uma resposta, e que as
respostas aparecem na mesma ordem dos exercícios.

Uso: python3 verificacao/integridade.py   (sai com código 1 se algo divergir)
"""
import re
import subprocess
import sys
from pathlib import Path

REF = "9a09ba5"
RAIZ = Path(__file__).resolve().parent.parent

CAPITULOS = {
    "01": "01_complexidade", "02": "02_heaps", "03": "03_heaps_avancados",
    "04": "04_unionfind", "05": "05_avl", "06": "06_ordenacao_comparacao",
    "07": "07_ordenacao_linear", "08": "08_selecao", "09": "09_divisao_conquista",
    "10": "10_revisao", "11": "11_programacao_dinamica", "12": "12_floyd_warshall",
    "13": "13_gulosos_matroides", "14": "14_agm", "15": "15_busca_largura",
    "16": "16_dijkstra", "17": "17_busca_profundidade",
    "18": "18_profundidade_digrafos", "A": "A_hash",
}

CABECALHO = re.compile(r"(\\begin\{exercicio\}\{([^}]*)\}(?:\[[^\]]*\])?)(<[^>\n]*>)?")
EXERCICIO = re.compile(r"\\begin\{exercicio\}\{([^}]*)\}.*?\\end\{exercicio\}", re.S)
RESP = re.compile(r"\\resp\{([^}]*)\}")


def no_commit(caminho):
    r = subprocess.run(["git", "-C", str(RAIZ), "show", f"{REF}:{caminho}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERRO: não consegui ler {caminho} no commit {REF} "
                 f"(o clone precisa do histórico completo).\n{r.stderr}")
    return r.stdout


def secao_exercicios(texto, nome):
    i = texto.find(r"\section{Exercícios}")
    if i < 0:
        raise ValueError(f"{nome}: seção Exercícios não encontrada")
    return texto[i:]


def rotulos(secao):
    return [m.group(1) for m in EXERCICIO.finditer(secao)]


def compara_capitulo(cod, arq, erros):
    caminho = f"capitulos/{arq}.tex"
    antigo = secao_exercicios(no_commit(caminho), caminho)
    novo = secao_exercicios((RAIZ / caminho).read_text(encoding="utf-8"), caminho)

    # 1. Tira o argumento <...> dos cabeçalhos (a única mudança permitida neles).
    novo_sem = CABECALHO.sub(lambda m: m.group(1), novo)

    # 2. Separa os exercícios novos, que só podem vir depois do último antigo.
    velhos = rotulos(antigo)
    fim_antigo = antigo.rstrip()
    ultimo = list(EXERCICIO.finditer(novo_sem))
    pos = None
    for m in ultimo:
        if m.group(1) == velhos[-1]:
            pos = m.end()
    if pos is None:
        erros.append(f"{caminho}: o último exercício antigo ({velhos[-1]}) sumiu")
        return [], []
    prefixo, resto = novo_sem[:pos], novo_sem[pos:]
    if prefixo != fim_antigo:
        # aponta a primeira diferença, para facilitar a correção
        k = next((i for i, (a, b) in enumerate(zip(prefixo, fim_antigo)) if a != b),
                 min(len(prefixo), len(fim_antigo)))
        trecho_a = fim_antigo[max(0, k - 60):k + 60].replace("\n", "\\n")
        trecho_n = prefixo[max(0, k - 60):k + 60].replace("\n", "\\n")
        erros.append(f"{caminho}: a seção de exercícios mudou perto do caractere {k}.\n"
                     f"   referência: ...{trecho_a}...\n   atual:      ...{trecho_n}...")
    novos = rotulos(resto)
    sobra = EXERCICIO.sub("", resto)
    if sobra.strip():
        erros.append(f"{caminho}: há texto fora de exercícios depois do último "
                     f"exercício antigo: {sobra.strip()[:80]!r}")
    for r in novos:
        if r in velhos:
            erros.append(f"{caminho}: o rótulo {r} já existia e foi repetido no fim")
    return velhos, novos


def compara_respostas(cod, velhos, novos, erros):
    caminho = f"capitulos/respostas/{cod}.tex"
    antigo = no_commit(caminho).rstrip()
    novo = (RAIZ / caminho).read_text(encoding="utf-8")
    if not novo.startswith(antigo):
        k = next((i for i, (a, b) in enumerate(zip(novo, antigo)) if a != b),
                 min(len(novo), len(antigo)))
        erros.append(f"{caminho}: uma resposta existente mudou perto do caractere {k}: "
                     f"...{novo[max(0, k - 50):k + 50]!r}...")
        return
    resto = novo[len(antigo):]
    acrescentadas = RESP.findall(resto)
    if resto.strip() and not resto.lstrip().startswith(r"\resp{"):
        erros.append(f"{caminho}: texto acrescentado fora de um \\resp no fim do arquivo")
    if acrescentadas != novos:
        erros.append(f"{caminho}: respostas novas {acrescentadas} não correspondem, "
                     f"na ordem, aos exercícios novos {novos}")
    todas = RESP.findall(novo)
    if todas != velhos + novos:
        erros.append(f"{caminho}: a ordem das respostas não segue a dos exercícios")


def main():
    erros = []
    total_velhos = total_novos = 0
    for cod, arq in CAPITULOS.items():
        velhos, novos = compara_capitulo(cod, arq, erros)
        compara_respostas(cod, velhos, novos, erros)
        total_velhos += len(velhos)
        total_novos += len(novos)
    if erros:
        print("Integridade dos exercícios: FALHOU")
        for e in erros:
            print(" -", e)
        sys.exit(1)
    print(f"Integridade dos exercícios: ok ({total_velhos} exercícios e respostas "
          f"idênticos a {REF}; {total_novos} novos no fim das listas)")


if __name__ == "__main__":
    main()
