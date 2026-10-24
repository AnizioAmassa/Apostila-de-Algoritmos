# Apostila de Algoritmos
#
# Este Makefile fica em AI-helper/, mas os comandos rodam na raiz do repositório.
# Da raiz, use "make -C AI-helper <alvo>" (ou "make -f AI-helper/Makefile <alvo>"):
#
#   pdf        compila apostila.pdf com o latexmk (sumário, referências e índice)
#   verificar  confere a integridade dos exercícios e os números dos exemplos
#   avisos     resume erros, avisos e linhas estouradas do último apostila.log
#   limpar     apaga os arquivos auxiliares (o apostila.pdf é mantido)

PRINCIPAL := apostila
PYTHON    ?= python3
AQUI      := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
RAIZ      := $(abspath $(AQUI)/..)
LATEXMK   := latexmk -r $(AQUI)/latexmkrc

# Datas do PDF fixadas pela data do último commit que mexeu nas fontes: assim,
# compilar duas vezes as mesmas fontes produz exatamente o mesmo arquivo, e a CI
# só faz commit do PDF quando o conteúdo de fato muda.
SOURCE_DATE_EPOCH ?= $(shell git -C $(RAIZ) log -1 --format=%ct -- $(PRINCIPAL).tex capitulos 2>/dev/null)
export SOURCE_DATE_EPOCH
export FORCE_SOURCE_DATE := 1

.PHONY: all pdf verificar avisos limpar

all: pdf

# O latexmk decide sozinho o que precisa ser refeito (inclusive o índice).
pdf:
	cd $(RAIZ) && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(PRINCIPAL).tex

verificar:
	cd $(RAIZ) && $(PYTHON) verificacao/rodar.py

avisos:
	cd $(RAIZ) && $(PYTHON) verificacao/log.py $(PRINCIPAL).log

limpar:
	cd $(RAIZ) && $(LATEXMK) -c $(PRINCIPAL).tex
	cd $(RAIZ) && rm -f $(PRINCIPAL).run.xml $(PRINCIPAL).bbl $(PRINCIPAL).synctex.gz
	rm -rf $(RAIZ)/verificacao/__pycache__
