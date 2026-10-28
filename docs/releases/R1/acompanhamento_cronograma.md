# Acompanhamento do cronograma — revisão de 28/10/2026

CRO **v2.3**: [ProjectLibre](../../03_CRO_Cade_Meu_Trem.pod) e [XML](../../03_CRO_Cade_Meu_Trem.xml).

## O que foi corrigido

O XML 2.1 concentrava 13 h de atividades da R1 entre 19h e 21h de 27/10, todas atribuídas a Antony, com sobreposição e dependências incompatíveis. Também preenchia trabalho real a partir da estimativa, embora não houvesse medição. Esses dados não comprovam esforço ou horário efetivo.

A revisão preserva a linha de base 0, calendário, recursos, dependências, datas planejadas e 76 h (67 h base + 9 h de reserva). O avanço comprovado está no campo **% físico concluído** e nas notas das subtarefas. Os campos de execução por duração/trabalho foram deixados sem lançamento validado: **ActualWork = 0 significa não informado, e não zero horas gastas**. Não usar esses valores para EVM, produtividade ou custo real.

O .pod foi atualizado pela biblioteca nativa do ProjectLibre 1.9.8, salvo e reaberto. Foram comparadas as 99 tarefas: datas, trabalho, custo e linha de base preservados; notas e avanço físico conferidos. A importação direta do XML não foi usada para gerar o .pod, pois o teste de importação perdeu parte do trabalho da baseline. O XML é uma representação paralela; para editar, prefira o .pod.

## Avanço comprovado

| Atividades | Situação | Evidência |
|---|---|---|
| A01 a A04 | Entregas da R0 concluídas; A04.3 versionada em 26/10 | tag release-0 |
| A05.1 a A05.3 | Base Python + Flask + SQLite concluída | e998de3 |
| A06.1 a A06.4 | Pessoas concluído | ec97672; CT01 aprovado |
| A07.1 a A07.4 | Categorias concluído | 2c9f3a9; CT02 aprovado |
| A08.1 a A08.3 | Suíte existente aprovada | 37/37 na revisão de 28/10; ver relatório |
| A09.1 | Documentos atualizados, incluindo correções desta revisão | diff desta revisão |
| A09.2 | Parcial: merge confirmado; baseline da R1 pendente | PR #17, merge 1e1b6b8 de 28/10; tag release-1 ausente na consulta |
| A09.3 / M1 | Demonstração e aceite pendentes | previstos para 29/10 |
| R2 a R4 | Planejadas | marcos 05/11, 12/11 e 19/11 |

A R1 possui 13 h de **peso planejado de entregas concluídas**, de 15 h base (86,7%), ou 76,5% ao incluir 2 h de reserva no denominador. Isso não é esforço real. As reservas não são entregas obrigatórias e seu consumo ainda precisa ser confirmado. Não se pode afirmar que a recuperação ocorreu sem consumi-las.

## Apontamentos pendentes

A dupla informou possuir apontamentos, mas os valores não foram recebidos nesta revisão. Registrar por atividade: integrante, início, término e horas efetivas. Depois atualizar as atribuições no ProjectLibre, conferir sobrealocação e exportar novamente o XML, preservando a baseline 0. Não inferir horas de trabalho pela data dos commits.

Até receber esses valores, não afirmar que o risco R3 ficou abaixo de 2 h, que houve atraso real de 1 a 4 dias em cada atividade, ou que a reserva não foi utilizada. Os commits comprovam a disponibilidade dos artefatos em uma data, não quando cada atividade começou ou terminou.

## Distribuição de responsabilidades — CRO v2.3

Felipe é responsável pelo desenvolvimento da R1. São 11 subtarefas, com responsabilidade exclusiva por atividade:

| Responsável | Atividades R1 | Trabalho planejado |
|---|---|---|
| Felipe Santana Medeiros | A05.1–A05.3: ambiente, banco e navegação | 4 h |
| Felipe Santana Medeiros | A06.1–A06.4: CRUD de pessoas | 3 h |
| Felipe Santana Medeiros | A07.1–A07.4: CRUD de categorias | 2 h |
| Antony Souza Siqueira | A08.1–A08.3: testes | 3 h |
| Antony Souza Siqueira | A09.1–A09.3: documentação, versionamento e demonstração | 3 h |
| Antony Souza Siqueira | B01: reserva R1, uso ainda não confirmado | 2 h |

R1: Felipe 9 h e Antony 8 h, incluindo a reserva. Projeto completo: Felipe 9 h e Antony 67 h. A distribuição não aumenta as 76 h totais e preserva datas, custos e baseline 0. Os apontamentos reais continuam pendentes. A tag release-0 permanece como referência histórica da alocação original.
