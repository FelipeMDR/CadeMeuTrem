# Acompanhamento do cronograma — R4, status em 17/11/2026

Os valores abaixo estão em [`03_CRO_Cade_Meu_Trem.xml`](../../03_CRO_Cade_Meu_Trem.xml) (cronograma v2.6). A linha de
base 0 (76 h), as datas planejadas, o trabalho e os responsáveis por atividade foram preservados conforme o cronograma
da R2, sem divisão igualitária de 50% por integrante. O `.pod` foi sincronizado e reaberto para validação em 17/11. O avanço comprovado fica no campo **% físico concluído**; as horas reais
continuam pendentes de lançamento.

## Situação por release

| Release | Trabalho planejado | Atividades concluídas | Falta |
|---|---|---|---|
| R0 a R2 | 45 h | 41 h | Atividades obrigatórias concluídas; 4 h das reservas B00 e B01 sem consumo registrado. |
| R3 | 15 h | 14 h | A16.3 (demonstração); A16.2 concluída com o PR #22 e a tag `release3` |
| R4 | 16 h (15 h base + 1 h reserva) | 14 h | A20.2 (demonstração); A20.1 concluída com o PR #23 e a tag `release4`; reserva B04 não usada |

As horas de atividades concluídas representam seu peso no planejamento, não horas reais trabalhadas.

## Atividades da R4 concluídas em 17/11

| Atividade | Fim na linha de base | Evidência |
|---|---|---|
| A17.1 a A17.3 Histórico de empréstimos | 14/11 | RFS19; commit `55a5636` |
| A18.1 Histórico e período inclusivo | 15/11 | CT08 11/11; commit `5e38614` |
| A18.2 Regressão dos cadastros e relatórios | 15/11 | 129/129 aprovados; [relatório de testes](relatorio_testes.md) |
| A18.3 Instalação e execução offline | 15/11 | CT11 2/2 e CT14 (clone limpo do GitHub, 129/129) |
| A18.4 Desempenho e restauração | 16/11 | CT12 abaixo de 100 ms e restauração no CT10; commit `5e38614` |
| A19.1 README e dados de exemplo | 17/11 | README consolidado, manual do usuário e dados com histórico |
| A19.2 Documentos e rastreabilidade | 18/11 | DRE 3.4, MRB 2.4 e cronograma v2.6 |

A17 e A18 terminaram de 1 a 3 dias depois da linha de base; A19 terminou no prazo. A R4 é apresentada antes do marco M4
(19/11), junto com a R3, por exigência do professor.

## Riscos

- **R2 – Atraso por outras atividades:** ocorreu na R3 (6 a 10 dias). A resposta foi concentrar a R3 e a R4 e preservar
  o marco final.
- **R4 – Crescimento do escopo:** controlado. A única mudança, a #21 (objeto sem código), passou pelo controle de
  mudanças e reduziu o cadastro, sem novos requisitos.
- **R5 – Perda de código ou documentos:** mitigado pelo repositório remoto e pelas tags de baseline.

## Horas reais

As horas reais **não foram medidas**. A dupla deve lançar no ProjectLibre o tempo gasto em cada atividade; esse valor
fecha o EVM da entrega final e a revisão da produtividade de 2 h/PCU da EST.

## Arquivo do ProjectLibre

O arquivo [`03_CRO_Cade_Meu_Trem.pod`](../../03_CRO_Cade_Meu_Trem.pod) está sincronizado com o XML v2.6.
Foram conferidas as 99 linhas, a linha de base de 76 h, as datas planejadas, os custos, as atribuições e as colunas.
A coluna **Avanço físico** mantém o progresso das atividades; os resumos indicam **ver subtarefas**. As demonstrações
A16.3 e A20.2, os marcos M3 e M4 e o lançamento das horas reais continuam pendentes.
