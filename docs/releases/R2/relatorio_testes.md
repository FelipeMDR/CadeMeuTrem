# Relatório de testes — Release 2

**Execução:** 03/11/2026 17:47 · **Resultado:** 101 de 101 cenários aprovados · **Duração:** 52.9 s

Testes funcionais automatizados com Selenium (Chrome headless). Cada execução usa um banco SQLite
temporário; o banco local em `data/` não é alterado. Para repetir: `scripts\testar.bat`.

## Ambiente

- Sistema: Windows 10 (10.0.26300)
- Python: 3.11.9
- Flask: 3.1.0
- Selenium: 4.27.1
- Navegador: chrome 156.0.8078.80
- ChromeDriver: 156.0.8078.80

## CT01 — Manter pessoas (RFS01 a RFS04): 20/20 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS01 | Incluir pessoa valida | Aprovado | 2.69 |
| RFS01 | Ativo inicia como sim | Aprovado | 0.08 |
| RFS01 | Espacos nas extremidades sao removidos | Aprovado | 0.26 |
| RFS01 | Nome obrigatorio preserva dados digitados | Aprovado | 0.28 |
| RFS01 | Limites de nome e contato | Aprovado | 0.81 |
| RFS01 | Homonimos sao permitidos | Aprovado | 0.60 |
| RFS01 | Texto com html e exibido como texto | Aprovado | 0.30 |
| RFS02 | Alterar pessoa mantem identificador | Aprovado | 0.69 |
| RFS02 | Alteracao aplica as mesmas validacoes | Aprovado | 0.38 |
| RFS02 | Reativar pessoa | Aprovado | 0.43 |
| RFS03 | Lista em ordem alfabetica | Aprovado | 0.35 |
| RFS03 | Desempate por identificador | Aprovado | 0.17 |
| RFS03 | Filtro por trecho do nome sem diferenciar maiusculas | Aprovado | 0.37 |
| RFS03 | Filtro ativo combinado por e | Aprovado | 0.27 |
| RFS03 | Sem resultados | Aprovado | 0.15 |
| RFS03 | Detalhe apresenta os mesmos campos | Aprovado | 0.20 |
| RFS04 | Cancelar exclusao preserva pessoa | Aprovado | 0.29 |
| RFS04 | Confirmar exclusao remove somente a pessoa | Aprovado | 0.29 |
| RFS04 | Exclusao bloqueada quando ha emprestimo | Aprovado | 0.22 |
| RFS04 | Vinculo revalidado na confirmacao | Aprovado | 0.32 |

## CT02 — Manter categorias (RFS05 a RFS08): 15/15 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS05 | Incluir categoria valida | Aprovado | 0.30 |
| RFS05 | Duplicidade desconsidera maiusculas e espacos | Aprovado | 1.10 |
| RFS05 | Duplicidade com acentos e maiusculas | Aprovado | 0.34 |
| RFS05 | Nome obrigatorio | Aprovado | 0.27 |
| RFS05 | Limite de 40 caracteres | Aprovado | 0.50 |
| RFS06 | Alterar categoria mantem identificador | Aprovado | 0.48 |
| RFS06 | Duplicidade desconsidera o proprio registro | Aprovado | 1.25 |
| RFS06 | Alteracao aplica as mesmas validacoes | Aprovado | 0.44 |
| RFS06 | Renomear mantem vinculo com objetos | Aprovado | 0.38 |
| RFS07 | Lista em ordem alfabetica | Aprovado | 0.31 |
| RFS07 | Filtro por trecho sem diferenciar maiusculas | Aprovado | 0.30 |
| RFS07 | Sem resultados | Aprovado | 0.16 |
| RFS08 | Cancelar exclusao preserva categoria | Aprovado | 0.24 |
| RFS08 | Confirmar exclusao remove somente a categoria | Aprovado | 0.30 |
| RFS08 | Exclusao bloqueada quando ha objeto | Aprovado | 0.20 |

## CT03 — Manter objetos (RFS09 a RFS12): 18/18 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS09 | Incluir objeto valido | Aprovado | 0.55 |
| RFS09 | Ativo inicia como sim e categoria mostra nome e identificador | Aprovado | 0.15 |
| RFS09 | Obrigatorios preservam dados digitados | Aprovado | 0.31 |
| RFS09 | Limites de codigo nome e observacao | Aprovado | 1.19 |
| RFS09 | Codigo unico sem diferenciar maiusculas e espacos | Aprovado | 0.61 |
| RFS09 | Sem categoria cadastrada impede inclusao | Aprovado | 0.17 |
| RFS09 | Categoria inexistente na gravacao | Aprovado | 0.27 |
| RFS10 | Alterar objeto mantem identificador | Aprovado | 0.73 |
| RFS10 | Unicidade desconsidera o proprio objeto | Aprovado | 0.46 |
| RFS10 | Inativar objeto emprestado continua emprestado | Aprovado | 0.37 |
| RFS11 | Lista em ordem de nome codigo e identificador | Aprovado | 0.49 |
| RFS11 | Filtro codigo compara o codigo completo | Aprovado | 0.46 |
| RFS11 | Filtros combinados por e | Aprovado | 0.70 |
| RFS11 | Detalhe inclui observacao | Aprovado | 0.28 |
| RFS12 | Cancelar exclusao preserva objeto | Aprovado | 0.29 |
| RFS12 | Confirmar exclusao remove somente o objeto | Aprovado | 0.37 |
| RFS12 | Exclusao bloqueada com emprestimo devolvido | Aprovado | 0.27 |
| RFS12 | Vinculo revalidado na confirmacao | Aprovado | 0.27 |

## CT04 — Controlar empréstimos (RFS13 a RFS16): 14/14 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS13 | Incluir emprestimo valido | Aprovado | 0.73 |
| RFS13 | Valores iniciais e listas somente com elegiveis | Aprovado | 0.28 |
| RFS13 | Homonimos distinguidos pelo identificador | Aprovado | 0.45 |
| RFS13 | Obrigatorios preservam dados digitados | Aprovado | 0.43 |
| RFS13 | Sem pessoa ou objeto elegivel informa o motivo | Aprovado | 0.13 |
| RFS14 | Alterar previsao e observacao | Aprovado | 0.91 |
| RFS14 | Pessoa objeto e retirada nao sao alterados | Aprovado | 0.46 |
| RFS14 | Devolvido permite alterar somente observacao | Aprovado | 0.47 |
| RFS15 | Ordem por retirada e identificador decrescentes | Aprovado | 0.56 |
| RFS15 | Filtros combinados por e | Aprovado | 0.73 |
| RFS15 | Detalhe inclui observacao | Aprovado | 0.36 |
| RFS16 | Cancelar exclusao preserva emprestimo | Aprovado | 0.49 |
| RFS16 | Confirmar exclusao preserva pessoa e objeto e libera objeto | Aprovado | 0.55 |
| RFS16 | Excluir historico antigo nao libera objeto com emprestimo aberto | Aprovado | 0.52 |

## CT05 — Regras de empréstimo e devolução (RFS13 a RFS17 e RNF02): 9/9 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS13 | Segunda retirada aberta do mesmo objeto e bloqueada | Aprovado | 0.41 |
| RFS13 | Pessoa inativa e bloqueada na gravacao | Aprovado | 0.33 |
| RFS13 | Objeto inativo e bloqueado na gravacao | Aprovado | 0.33 |
| RNF02 | Banco impede dois emprestimos abertos do mesmo objeto | Aprovado | 0.14 |
| RFS17 | Devolver objeto ativo permite nova retirada | Aprovado | 0.62 |
| RFS17 | Objeto inativo devolvido continua inelegivel | Aprovado | 0.50 |
| RFS17 | Cancelar devolucao preserva emprestimo aberto | Aprovado | 0.38 |
| RFS17 | Nao devolve novamente nem reabre | Aprovado | 0.83 |
| RFS17 | Devolucao revalidada na confirmacao | Aprovado | 0.35 |

## CT06 — Datas de retirada, previsão e devolução (RFS13, RFS14 e RFS17): 17/17 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS13 | Retirada invalida e recusada e dados permanecem[31/04/2024-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.51 |
| RFS13 | Retirada invalida e recusada e dados permanecem[29/02/2025-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.48 |
| RFS13 | Retirada invalida e recusada e dados permanecem[00/01/2024-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.49 |
| RFS13 | Retirada invalida e recusada e dados permanecem[15/13/2024-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.52 |
| RFS13 | Retirada invalida e recusada e dados permanecem[1/2/2024-Data da retirada deve estar no formato DD/MM/AAAA.] | Aprovado | 0.48 |
| RFS13 | Retirada invalida e recusada e dados permanecem[2024-02-01-Data da retirada deve estar no formato DD/MM/AAAA.] | Aprovado | 0.48 |
| RFS13 | 29 de fevereiro em ano bissexto e aceito | Aprovado | 0.45 |
| RFS13 | Retirada futura e recusada | Aprovado | 0.42 |
| RFS13 | Previsao anterior a retirada e recusada | Aprovado | 0.89 |
| RFS13 | Limites iguais sao aceitos | Aprovado | 0.52 |
| RFS14 | Previsao valida com os mesmos limites | Aprovado | 0.57 |
| RFS17 | Devolucao entre retirada e hoje inclusive[-1-False] | Aprovado | 0.32 |
| RFS17 | Devolucao entre retirada e hoje inclusive[0-True] | Aprovado | 0.33 |
| RFS17 | Devolucao entre retirada e hoje inclusive[1-True] | Aprovado | 0.32 |
| RFS17 | Devolucao entre retirada e hoje inclusive[4-True] | Aprovado | 0.34 |
| RFS17 | Devolucao entre retirada e hoje inclusive[5-False] | Aprovado | 0.31 |
| RFS17 | Data de devolucao invalida | Aprovado | 0.29 |

## CT10 — Persistência e integridade (RNF02): 3/3 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF02 | Dados persistem apos reiniciar o servidor | Aprovado | 2.90 |
| RNF02 | Exclusoes com vinculo sao bloqueadas pela tela | Aprovado | 1.27 |
| RNF02 | Referencias continuam validas apos renomear | Aprovado | 1.70 |

## CT13 — Validação e proteção (RNF05): 5/5 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF05 | Parametros repetidos ou invalidos sao ignorados | Aprovado | 0.40 |
| RNF05 | Banco e codigo nao sao servidos | Aprovado | 0.15 |
| RNF05 | Texto com html e aspas e exibido como texto | Aprovado | 0.87 |
| RNF05 | Observacao do emprestimo acima do limite e recusada | Aprovado | 0.57 |
| RNF05 | Formulario sem token valido e recusado | Aprovado | 2.47 |
