# Acompanhamento do cronograma — R3, status em 17/11/2026

Atualização periódica do CRO. Os valores abaixo estão em [`03_CRO_Cade_Meu_Trem.xml`](../../03_CRO_Cade_Meu_Trem.xml)
(cronograma v2.6, consolidado com a R4), sincronizado com o `.pod` em 17/11. A linha de base 0 (76 h) e os responsáveis
por atividade foram preservados conforme o cronograma da R2, sem divisão igualitária de 50% por integrante. O avanço comprovado fica no campo **% físico concluído**, e as horas
reais continuam pendentes de lançamento.

## Situação por release

| Release | Trabalho planejado | Atividades concluídas | Observação |
|---|---|---|---|
| R2 | 18 h | Todas | A13.3 (demonstração) e marco M2 em 03/11, dois dias antes do previsto. |
| R3 | 15 h (13 h base + 2 h reserva) | 14 h de 15 h | A14, A15, B03, A16.1 e A16.2 concluídas em 17/11; PR #22 integrado e tag `release3` publicada. Falta A16.3 (demonstração, junto com a R4). |
| R4 | 16 h | 14 h de 16 h | Ver o acompanhamento da R4; demonstração pendente e reserva B04 não usada. |

As horas de atividades concluídas representam seu peso no planejamento, não horas reais trabalhadas.

## Atividades concluídas em 17/11

| Atividade | Fim na linha de base | Evidência |
|---|---|---|
| A14.1 a A14.3 Relatório de pendências | 07 e 08/11 | RFS18; commit `c64a55f` |
| A15.1 Cenários de atraso e filtros | 08/11 | CT07 9/9; commit `5e16407` |
| A15.2 Interface e confirmação de operações | 09/11 | CT09 3/3; commit `5e16407` |
| A15.3 Medir consultas | 10/11 | CT12: pendências em até 48 ms; [relatório de testes](relatorio_testes.md) |
| B03 Reserva de correção R3 | 11/11 | Mudança #21, objeto sem código; commit `80efd2d` |
| A16.1 Atualizar documentos da R3 | 11/11 | DRE 3.3, MRB 2.3, cronograma v2.5, notas e evidências |

## Desvios

As atividades da R3 terminaram de 6 a 10 dias depois da linha de base, e o marco M3 (12/11) não foi cumprido. Por
exigência do professor, a R3 é apresentada junto com a R4. O desvio está acima do limiar do risco **R2 – Atraso por outras
atividades** (mais de 20% da duração planejada). A resposta foi concentrar a R3 e a R4 em 17/11, sem acrescentar escopo,
para preservar o marco final M4 (19/11).

## Mudança de escopo

A **mudança #21** (objeto sem código) veio de orientação do professor e passou pelo controle de mudanças: issue com o
rótulo `mudança`, requisitos afetados no DRE 3.3, procedimentos revistos na MRB 2.3 e esforço absorvido pela reserva B03,
sem alterar os marcos.

## Horas reais

As horas reais **não foram medidas**. A dupla deve lançar no ProjectLibre o tempo gasto em cada atividade concluída.

## Arquivo do ProjectLibre

O arquivo [`03_CRO_Cade_Meu_Trem.pod`](../../03_CRO_Cade_Meu_Trem.pod) está sincronizado com o XML v2.6.
Foram conferidas as 99 linhas, a linha de base de 76 h, as datas planejadas, os custos, as atribuições e as colunas.
A coluna **Avanço físico** mantém o progresso das atividades; os resumos indicam **ver subtarefas**. As demonstrações
A16.3 e A20.2, os marcos M3 e M4 e o lançamento das horas reais continuam pendentes.
