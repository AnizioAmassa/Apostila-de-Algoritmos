# Apostila de Algoritmos

Apostila em LaTeX, em português, da disciplina de Algoritmos do IMPA Tech:
complexidade, estruturas de dados (heaps, Union-Find, AVL, tabelas hash),
ordenação e seleção, divisão e conquista, programação dinâmica, algoritmos
gulosos e matroides e algoritmos em grafos. Cada capítulo traz exemplos
resolvidos, um resumo e uma lista de exercícios com respostas no Apêndice B.

**O PDF pronto é o [`apostila.pdf`](apostila.pdf) da raiz do repositório.** Ele é
recompilado automaticamente pela CI a cada push (veja abaixo), então basta
baixá-lo daqui.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `apostila.tex` | arquivo principal: preâmbulo com todos os estilos (caixas, figuras, pseudocódigo, exercícios), folha de rosto, prefácio e a lista de `\input` dos capítulos |
| `capitulos/01_*.tex` … `capitulos/18_*.tex` | os 18 capítulos; cada um termina com `\section{Exercícios}` |
| `capitulos/A_hash.tex` | Apêndice A: tabelas hash |
| `capitulos/B_respostas.tex` | Apêndice B: inclui as respostas de `capitulos/respostas/NN.tex` |
| `capitulos/respostas/NN.tex` | respostas dos exercícios do capítulo `NN` (e `A.tex`, do Apêndice A) |
| `capitulos/referencias.tex` | referências bibliográficas |
| `verificacao/` | scripts Python que conferem os exercícios e os números do texto (veja abaixo) |
| `AI-helper/AImanual.md` | este manual |
| `AI-helper/Makefile` | atalhos para compilar, verificar e limpar (rodam na raiz do repositório) |
| `AI-helper/latexmkrc` | configuração do `latexmk`: o índice remissivo usa o estilo `indice.ist` |
| `indice.ist` | estilo do `makeindex` para o índice remissivo |
| `.github/workflows/apostila.yml` | a CI que verifica, compila e atualiza o `apostila.pdf` |
| `apostila.pdf` | o PDF compilado, mantido no repositório |

### Exercícios e respostas

Cada exercício é escrito como

```latex
\begin{exercicio}{rotulo}[Origem]<sec:secao,ex:exemplo>
Enunciado...
\end{exercicio}
```

e a resposta, no arquivo `capitulos/respostas/NN.tex` do capítulo, como
`\resp{rotulo} Texto da resposta.` O rótulo liga os dois: o enunciado mostra o
link “resposta: p. X”, e o número da resposta leva de volta ao enunciado.

O argumento opcional entre `< >` lista, separados por vírgula, os rótulos da
seção, do exemplo ou da figura que o exercício pratica (prefixos `sec:`, `ex:`,
`fig:`, `teo:` e `lema:`). O cabeçalho mostra “(ver §5.3 e Exemplo 5.11)”, com
links. Ele é a única mudança aceita pelo script de integridade nos exercícios
antigos.

## Como compilar

Da raiz do repositório:

```sh
make -C AI-helper pdf    # equivale a: latexmk -r AI-helper/latexmkrc -pdf apostila.tex
```

O `latexmk` roda o `pdflatex` quantas vezes for preciso (sumário e referências
cruzadas) e também o `makeindex`, que gera o índice remissivo no fim do livro,
com o estilo `indice.ist` indicado no `AI-helper/latexmkrc`. Como esse arquivo
não fica na raiz, o `latexmk` só o lê com `-r AI-helper/latexmkrc`; sem ele a
apostila compila do mesmo jeito, mas o índice sai sem as letras de cada grupo.
A compilação completa leva cerca de 2 minutos.

Outros alvos do `AI-helper/Makefile`:

```sh
make -C AI-helper verificar   # integridade dos exercícios + conferência dos números (Python 3)
make -C AI-helper avisos      # resume erros, avisos e linhas estouradas do apostila.log
make -C AI-helper limpar      # apaga os arquivos auxiliares; o apostila.pdf é mantido
```

Para compilar um capítulo isolado, monte um `.tex` com as linhas do preâmbulo
de `apostila.tex` (até antes de `\begin{document}`) seguidas de
`\begin{document}\mainmatter\setcounter{chapter}{N-1}\input{capitulos/X}\end{document}`.
O Capítulo 16 usa a macro `\digrafoFW`, definida no Capítulo 12; inclua o 12
antes dele.

### Índice remissivo

Os termos aparecem no índice por meio de `\index{}`, colocado logo depois da
ocorrência em negrito que os define, por exemplo
`\textbf{fator de carga}\index{fator de carga}`. Termos com acento levam uma
chave de ordenação sem acento antes de `@` (`\index{arvore avl@árvore AVL}`), e
subentradas usam `!` (`\index{heap!binomial}`). Não coloque `\index` nos
exercícios nem nas respostas: o script de integridade recusaria a mudança.

### Pacotes TeX necessários

Em Debian/Ubuntu:

```sh
sudo apt-get install -y --no-install-recommends \
  latexmk texlive-latex-recommended texlive-latex-extra texlive-pictures \
  texlive-fonts-extra texlive-fonts-recommended texlive-lang-portuguese \
  texlive-science texlive-plain-generic cm-super
```

Sem `texlive-plain-generic` falta o `binhex.tex`; sem `cm-super` a compilação
para com um erro de “font expansion”. Em outras distribuições, uma instalação
completa do TeX Live (`scheme-full`) também serve.

## Verificação

`make -C AI-helper verificar` roda `verificacao/rodar.py` (que também pode ser
chamado diretamente, da raiz), que executa:

* `verificacao/integridade.py` — compara a seção de exercícios de cada capítulo
  e os arquivos de `capitulos/respostas/` com o commit de referência `9a09ba5`.
  Enunciados e respostas existentes não podem mudar; só são aceitos o argumento
  `<...>` no cabeçalho de um exercício, exercícios novos no fim da lista e
  respostas novas no fim do arquivo de respostas, na mesma ordem. O script
  precisa do histórico do Git (num clone raso, use `git fetch --unshallow`).
* `verificacao/cap*.py` — recalculam os números dos exemplos e das respostas de
  simulação (heaps, Union-Find, AVL, ordenações, seleção, inversões, programação
  dinâmica, Floyd-Warshall, Kruskal e Prim, buscas, Dijkstra, hash etc.) e
  conferem que cada valor escrito no `.tex` é o calculado. Se alguém mudar um
  número no texto sem recalcular, o script correspondente falha e diz onde.

## O `apostila.pdf` é atualizado automaticamente

A cada push, em qualquer branch, o GitHub Actions (`.github/workflows/apostila.yml`):

1. instala o TeX;
2. roda `python3 verificacao/rodar.py`;
3. compila com `latexmk -r AI-helper/latexmkrc -pdf apostila.tex`;
4. se o `apostila.pdf` mudou, faz um commit dele de volta no mesmo branch, como
   `github-actions[bot]`, com a mensagem “Atualiza apostila.pdf [skip ci]”.

Pushes que alteram só o `apostila.pdf` não disparam a CI, e o commit da CI usa
`[skip ci]`; assim não há laço. Depois de fazer push, rode `git pull` antes de
continuar trabalhando: a CI pode ter acrescentado esse commit ao branch.

As datas gravadas no PDF vêm do último commit que mexeu nas fontes
(`SOURCE_DATE_EPOCH`), de modo que compilar de novo as mesmas fontes produz o
mesmo arquivo e a CI só faz commit quando o conteúdo realmente muda.

Para a CI conseguir fazer o commit, o repositório precisa permitir escrita pelo
`GITHUB_TOKEN`: em *Settings → Actions → General → Workflow permissions*,
marque *Read and write permissions*.
