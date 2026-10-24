# Apostila de Algoritmos
#
#   make pdf        compila apostila.pdf com o latexmk (sumário, referências e índice)
#   make verificar  confere a integridade dos exercícios e os números dos exemplos
#   make avisos     resume erros, avisos e linhas estouradas do último apostila.log
#   make limpar     apaga os arquivos auxiliares (o apostila.pdf é mantido)

PRINCIPAL := apostila
PYTHON    ?= python3

# Datas do PDF fixadas pela data do último commit que mexeu nas fontes: assim,
# compilar duas vezes as mesmas fontes produz exatamente o mesmo arquivo, e a CI
# só faz commit do PDF quando o conteúdo de fato muda.
SOURCE_DATE_EPOCH ?= $(shell git log -1 --format=%ct -- $(PRINCIPAL).tex capitulos 2>/dev/null)
export SOURCE_DATE_EPOCH
export FORCE_SOURCE_DATE := 1

.PHONY: all pdf verificar avisos limpar

all: pdf

# O latexmk decide sozinho o que precisa ser refeito (inclusive o índice).
pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(PRINCIPAL).tex

verificar:
	$(PYTHON) verificacao/rodar.py

avisos:
	$(PYTHON) verificacao/log.py $(PRINCIPAL).log

limpar:
	latexmk -c $(PRINCIPAL).tex
	rm -f $(PRINCIPAL).run.xml $(PRINCIPAL).bbl $(PRINCIPAL).synctex.gz
	rm -rf verificacao/__pycache__
