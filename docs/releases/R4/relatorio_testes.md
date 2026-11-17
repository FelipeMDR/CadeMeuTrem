# Relatório de testes — Release 4

**Execução:** 17/11/2026 12:13 · **Resultado:** 129 de 129 cenários aprovados · **Duração:** 68.9 s

Testes funcionais automatizados com Selenium (Chrome headless). Cada execução usa um banco SQLite
temporário; o banco local em `data/` não é alterado. Para repetir: `scripts\testar.bat`.

## Ambiente

- Sistema: Windows 10 (10.0.26300)
- Python: 3.11.9
- Flask: 3.1.0
- Selenium: 4.27.1
- Navegador: chrome 157.0.8103.79
- ChromeDriver: 157.0.8103.78

## Tempos medidos no CT12 (RNF04)

- Massa: 100 pessoas, 500 objetos e 1.000 empréstimos. Limite: 2000 ms por consulta.
- Pendências, sem filtros: 39, 39, 38, 44, 39 ms (máximo 44 ms)
- Pendências, somente atrasados: 38, 26, 25, 26, 25 ms (máximo 38 ms)
- Histórico, últimos 30 dias: 45, 43, 46, 48, 47 ms (máximo 48 ms)
- Histórico, últimos 60 dias: 91, 84, 85, 84, 77 ms (máximo 91 ms)

## CT01 — Manter pessoas (RFS01 a RFS04): 20/20 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS01 | Incluir pessoa valida | Aprovado | 1.85 |
| RFS01 | Ativo inicia como sim | Aprovado | 0.06 |
| RFS01 | Espacos nas extremidades sao removidos | Aprovado | 0.64 |
| RFS01 | Nome obrigatorio preserva dados digitados | Aprovado | 0.68 |
| RFS01 | Limites de nome e contato | Aprovado | 0.56 |
| RFS01 | Homonimos sao permitidos | Aprovado | 0.42 |
| RFS01 | Texto com html e exibido como texto | Aprovado | 0.22 |
| RFS02 | Alterar pessoa mantem identificador | Aprovado | 0.46 |
| RFS02 | Alteracao aplica as mesmas validacoes | Aprovado | 0.29 |
| RFS02 | Reativar pessoa | Aprovado | 0.35 |
| RFS03 | Lista em ordem alfabetica | Aprovado | 0.27 |
| RFS03 | Desempate por identificador | Aprovado | 0.13 |
| RFS03 | Filtro por trecho do nome sem diferenciar maiusculas | Aprovado | 0.28 |
| RFS03 | Filtro ativo combinado por e | Aprovado | 0.20 |
| RFS03 | Sem resultados | Aprovado | 0.13 |
| RFS03 | Detalhe apresenta os mesmos campos | Aprovado | 0.14 |
| RFS04 | Cancelar exclusao preserva pessoa | Aprovado | 0.20 |
| RFS04 | Confirmar exclusao remove somente a pessoa | Aprovado | 0.23 |
| RFS04 | Exclusao bloqueada quando ha emprestimo | Aprovado | 0.19 |
| RFS04 | Vinculo revalidado na confirmacao | Aprovado | 0.28 |

## CT02 — Manter categorias (RFS05 a RFS08): 15/15 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS05 | Incluir categoria valida | Aprovado | 0.22 |
| RFS05 | Duplicidade desconsidera maiusculas e espacos | Aprovado | 0.47 |
| RFS05 | Duplicidade com acentos e maiusculas | Aprovado | 0.75 |
| RFS05 | Nome obrigatorio | Aprovado | 0.69 |
| RFS05 | Limite de 40 caracteres | Aprovado | 0.34 |
| RFS06 | Alterar categoria mantem identificador | Aprovado | 0.84 |
| RFS06 | Duplicidade desconsidera o proprio registro | Aprovado | 1.08 |
| RFS06 | Alteracao aplica as mesmas validacoes | Aprovado | 0.29 |
| RFS06 | Renomear mantem vinculo com objetos | Aprovado | 0.24 |
| RFS07 | Lista em ordem alfabetica | Aprovado | 0.23 |
| RFS07 | Filtro por trecho sem diferenciar maiusculas | Aprovado | 0.75 |
| RFS07 | Sem resultados | Aprovado | 0.13 |
| RFS08 | Cancelar exclusao preserva categoria | Aprovado | 0.20 |
| RFS08 | Confirmar exclusao remove somente a categoria | Aprovado | 0.21 |
| RFS08 | Exclusao bloqueada quando ha objeto | Aprovado | 0.15 |

## CT03 — Manter objetos (RFS09 a RFS12): 18/18 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS09 | Incluir objeto valido | Aprovado | 0.34 |
| RFS09 | Formulario sem codigo ativo sim e categoria com identificador | Aprovado | 0.12 |
| RFS09 | Obrigatorios preservam dados digitados | Aprovado | 0.71 |
| RFS09 | Limites de nome e observacao | Aprovado | 0.74 |
| RFS09 | Cada unidade fisica e um objeto com identificador proprio | Aprovado | 1.00 |
| RFS09 | Sem categoria cadastrada impede inclusao | Aprovado | 0.13 |
| RFS09 | Categoria inexistente na gravacao | Aprovado | 0.64 |
| RFS10 | Alterar objeto mantem identificador | Aprovado | 0.93 |
| RFS10 | Alteracao aplica as mesmas validacoes | Aprovado | 0.16 |
| RFS10 | Inativar objeto emprestado continua emprestado | Aprovado | 0.76 |
| RFS11 | Lista em ordem de nome e identificador | Aprovado | 0.42 |
| RFS11 | Filtro por trecho do nome sem diferenciar maiusculas | Aprovado | 0.40 |
| RFS11 | Filtros combinados por e | Aprovado | 0.55 |
| RFS11 | Detalhe inclui observacao | Aprovado | 0.21 |
| RFS12 | Cancelar exclusao preserva objeto | Aprovado | 0.23 |
| RFS12 | Confirmar exclusao remove somente o objeto | Aprovado | 0.26 |
| RFS12 | Exclusao bloqueada com emprestimo devolvido | Aprovado | 0.23 |
| RFS12 | Vinculo revalidado na confirmacao | Aprovado | 0.25 |

## CT04 — Controlar empréstimos (RFS13 a RFS16): 14/14 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS13 | Incluir emprestimo valido | Aprovado | 0.61 |
| RFS13 | Valores iniciais e listas somente com elegiveis | Aprovado | 0.27 |
| RFS13 | Homonimos distinguidos pelo identificador | Aprovado | 0.40 |
| RFS13 | Obrigatorios preservam dados digitados | Aprovado | 0.85 |
| RFS13 | Sem pessoa ou objeto elegivel informa o motivo | Aprovado | 0.12 |
| RFS14 | Alterar previsao e observacao | Aprovado | 0.39 |
| RFS14 | Pessoa objeto e retirada nao sao alterados | Aprovado | 0.38 |
| RFS14 | Devolvido permite alterar somente observacao | Aprovado | 0.40 |
| RFS15 | Ordem por retirada e identificador decrescentes | Aprovado | 0.41 |
| RFS15 | Filtros combinados por e | Aprovado | 0.52 |
| RFS15 | Detalhe inclui observacao | Aprovado | 0.30 |
| RFS16 | Cancelar exclusao preserva emprestimo | Aprovado | 0.33 |
| RFS16 | Confirmar exclusao preserva pessoa e objeto e libera objeto | Aprovado | 0.39 |
| RFS16 | Excluir historico antigo nao libera objeto com emprestimo aberto | Aprovado | 0.85 |

## CT05 — Regras de empréstimo e devolução (RFS13 a RFS17 e RNF02): 9/9 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS13 | Segunda retirada aberta do mesmo objeto e bloqueada | Aprovado | 0.31 |
| RFS13 | Pessoa inativa e bloqueada na gravacao | Aprovado | 0.26 |
| RFS13 | Objeto inativo e bloqueado na gravacao | Aprovado | 0.25 |
| RNF02 | Banco impede dois emprestimos abertos do mesmo objeto | Aprovado | 0.12 |
| RFS17 | Devolver objeto ativo permite nova retirada | Aprovado | 0.42 |
| RFS17 | Objeto inativo devolvido continua inelegivel | Aprovado | 0.37 |
| RFS17 | Cancelar devolucao preserva emprestimo aberto | Aprovado | 0.29 |
| RFS17 | Nao devolve novamente nem reabre | Aprovado | 0.28 |
| RFS17 | Devolucao revalidada na confirmacao | Aprovado | 0.29 |

## CT06 — Datas de retirada, previsão e devolução (RFS13, RFS14 e RFS17): 17/17 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS13 | Retirada invalida e recusada e dados permanecem[31/04/2024-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.38 |
| RFS13 | Retirada invalida e recusada e dados permanecem[29/02/2025-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.84 |
| RFS13 | Retirada invalida e recusada e dados permanecem[00/01/2024-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.35 |
| RFS13 | Retirada invalida e recusada e dados permanecem[15/13/2024-Data da retirada n\xe3o \xe9 uma data v\xe1lida.] | Aprovado | 0.34 |
| RFS13 | Retirada invalida e recusada e dados permanecem[1/2/2024-Data da retirada deve estar no formato DD/MM/AAAA.] | Aprovado | 0.33 |
| RFS13 | Retirada invalida e recusada e dados permanecem[2024-02-01-Data da retirada deve estar no formato DD/MM/AAAA.] | Aprovado | 0.34 |
| RFS13 | 29 de fevereiro em ano bissexto e aceito | Aprovado | 0.36 |
| RFS13 | Retirada futura e recusada | Aprovado | 0.33 |
| RFS13 | Previsao anterior a retirada e recusada | Aprovado | 0.30 |
| RFS13 | Limites iguais sao aceitos | Aprovado | 0.37 |
| RFS14 | Previsao valida com os mesmos limites | Aprovado | 1.37 |
| RFS17 | Devolucao entre retirada e hoje inclusive[-1-False] | Aprovado | 0.72 |
| RFS17 | Devolucao entre retirada e hoje inclusive[0-True] | Aprovado | 0.26 |
| RFS17 | Devolucao entre retirada e hoje inclusive[1-True] | Aprovado | 0.72 |
| RFS17 | Devolucao entre retirada e hoje inclusive[4-True] | Aprovado | 0.28 |
| RFS17 | Devolucao entre retirada e hoje inclusive[5-False] | Aprovado | 0.73 |
| RFS17 | Data de devolucao invalida | Aprovado | 0.72 |

## CT07 — Consultar pendências (RFS18): 9/9 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS18 | Sem filtros lista abertos com atrasados primeiro | Aprovado | 0.49 |
| RFS18 | Campos da listagem | Aprovado | 0.48 |
| RFS18 | Vencer hoje nao e atraso | Aprovado | 0.48 |
| RFS18 | Somente atrasados | Aprovado | 0.47 |
| RFS18 | Filtro de pessoa inclui inativas | Aprovado | 0.48 |
| RFS18 | Filtro de categoria usa a categoria atual | Aprovado | 0.64 |
| RFS18 | Objeto inativo com emprestimo aberto continua listado | Aprovado | 0.49 |
| RFS18 | Resultado vazio com totais zerados | Aprovado | 0.42 |
| RFS18 | Desempate por previsao e identificador | Aprovado | 0.43 |

## CT08 — Consultar histórico (RFS19): 11/11 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS19 | Periodo lista abertos e devolvidos com totais | Aprovado | 0.67 |
| RFS19 | Somente devolvidos | Aprovado | 0.45 |
| RFS19 | Limites do periodo sao inclusivos | Aprovado | 0.48 |
| RFS19 | Periodo invertido impede a consulta | Aprovado | 0.45 |
| RFS19 | Datas invalidas geram mensagem de correcao[31/04/2026-30/06/2026-erros0] | Aprovado | 0.34 |
| RFS19 | Datas invalidas geram mensagem de correcao[01/02/2026-29/02/2026-erros1] | Aprovado | 0.35 |
| RFS19 | Datas invalidas geram mensagem de correcao[2026-01-01--erros2] | Aprovado | 0.34 |
| RFS19 | Padrao e o mes atual ate hoje | Aprovado | 0.49 |
| RFS19 | Filtros combinados e resultado vazio | Aprovado | 0.52 |
| RFS19 | Desempate por identificador decrescente | Aprovado | 0.35 |
| RFS19 | Usa cadastros atuais e ignora excluidos | Aprovado | 0.75 |

## CT09 — Interface em português (RNF01): 3/3 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF01 | Telas em portugues com menu completo | Aprovado | 0.88 |
| RNF01 | Erros junto ao formulario preservam os dados | Aprovado | 0.93 |
| RNF01 | Exclusoes exigem confirmacao e cancelar preserva | Aprovado | 0.64 |

## CT10 — Persistência e integridade (RNF02): 5/5 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF02 | Dados persistem apos reiniciar o servidor | Aprovado | 2.83 |
| RNF02 | Exclusoes com vinculo sao bloqueadas pela tela | Aprovado | 1.32 |
| RNF02 | Referencias continuam validas apos renomear | Aprovado | 1.17 |
| RNF02 | Banco da r2 com codigo e migrado sem perder dados | Aprovado | 1.50 |
| RNF06 | Copia de seguranca com o sistema encerrado restaura os dados | Aprovado | 3.08 |

## CT11 — Execução local, sem internet (RNF03): 2/2 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF03 | Paginas usam somente arquivos da propria aplicacao | Aprovado | 0.36 |
| RNF03 | Servidor atende somente esta maquina | Aprovado | 0.04 |

## CT12 — Tempo de resposta dos relatórios (RNF04): 1/1 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF04 | Relatorios respondem em ate 2 segundos | Aprovado | 2.23 |

## CT13 — Validação e proteção (RNF05): 5/5 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF05 | Parametros repetidos ou invalidos sao ignorados | Aprovado | 0.30 |
| RNF05 | Banco e codigo nao sao servidos | Aprovado | 0.10 |
| RNF05 | Texto com html e aspas e exibido como texto | Aprovado | 0.61 |
| RNF05 | Observacao do emprestimo acima do limite e recusada | Aprovado | 0.42 |
| RNF05 | Formulario sem token valido e recusado | Aprovado | 2.87 |

## Verificação da entrega final em cópia limpa (CT14)

Em 17/11/2026, a branch `dev/release-4` (commit `5e38614`) foi clonada do GitHub numa pasta vazia, e o README foi
seguido do início: `python -m venv .venv`, instalação de `requirements.txt`, `scripts\carregar_exemplo.py` e a suíte
Selenium. Resultado: **129 de 129 aprovados em 68 s**, com o mesmo ambiente listado acima (ChromeDriver 157.0.8103.78).

## Execução sem internet (CT11)

A parte automatizada do CT11 confere, em todas as telas, que nenhum arquivo vem de fora da aplicação e que o servidor
atende somente em 127.0.0.1. A instalação das dependências precisa de internet uma única vez; depois disso, a aplicação
roda com a rede desligada. O roteiro para repetir essa verificação manualmente está no README, seção "Executar sem
internet".
