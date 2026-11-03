# Acompanhamento do cronograma — status em 03/11/2026

Atualização periódica do CRO (Aula 22-23, item 4). Os valores abaixo estão em
[`03_CRO_Cade_Meu_Trem.xml`](../../03_CRO_Cade_Meu_Trem.xml) (cronograma v2.4), que parte da v2.3 de 28/10. A linha de base 0
(76 h) foi preservada: datas, durações, trabalho e custo planejados não mudaram.

Segue a convenção da v2.3: o avanço comprovado fica no campo **% físico concluído**, e as horas reais continuam pendentes
de lançamento pela dupla. As notas de cada atividade citam o commit e o teste que comprovam a entrega.

## Situação por release

| Release | Trabalho planejado | Atividades concluídas | Observação |
|---|---|---|---|
| R1 | 17 h | Todas | A09.2 (PR #17 e tag `release1`, 28/10) e A09.3 (demonstração, 29/10) concluídas; marco M1 atingido. |
| R2 | 18 h (16 h base + 2 h reserva) | 16 h de 18 h | A10, A11, A12, A13.1 e a reserva B02 concluídas em 03/11. Faltam A13.2 (revisão e tag) e A13.3 (demonstração, antecipada para 03/11). |
| R3 e R4 | 31 h | — | Sem alteração; datas da linha de base mantidas. |

## Atividades concluídas em 03/11

| Atividade | Fim na linha de base | Evidência |
|---|---|---|
| A10.1 a A10.4 CRUD de objetos | 30 e 31/10 | RFS09 a RFS12; commit `92e40cb`; CT03 18/18 |
| A11.1 a A11.5 Empréstimos e devolução | 31/10 e 01/11 | RFS13 a RFS17; commit `1e1ab7b`; CT04 14/14, CT05 9/9, CT06 17/17 |
| A12.1 Integridade e exclusões com vínculo | 02/11 | CT05 e CT10 (persistência após reiniciar o servidor); commit `c5e9684` |
| A12.2 Datas e proteção de entrada | 03/11 | CT06 e CT13 (inclui token CSRF); commit `c5e9684` |
| A12.3 Registrar resultados | 03/11 | [relatório de testes](relatorio_testes.md): 101/101 aprovados |
| B02 Reserva de correção R2 | 04/11 | Modo de demonstração dos testes (`da3de8b`) e token CSRF (`503d723`) |
| A13.1 Atualizar documentos da R2 | 04/11 | DRE 3.2, MRB 2.2, cronograma v2.4, notas, roteiro e evidências |

A10, A11 e A12.1 terminaram de 1 a 4 dias depois da linha de base. A12.2 e A12.3 terminaram no prazo, e B02 e A13.1
um dia antes. A apresentação foi antecipada para 03/11 a pedido do professor, dois dias antes do marco M2 (05/11).

## Mudanças nesta versão do cronograma

- **Responsáveis:** as atividades da R1 em diante passam a ser da dupla, com 50% para cada integrante. O trabalho total de
  cada atividade não mudou. Na v2.3, A05 a A07 estavam só com Felipe, e as demais só com Antony. A R0 continua como foi
  entregue.
- **Reserva B02:** usada nas correções pedidas depois da R1, e não em retrabalho da R2.

## Riscos

- **R2 – Atraso por outras atividades:** A10 e A11 começaram depois do previsto. A recuperação foi concentrada em 03/11, e
  o marco foi preservado.
- **R4 – Crescimento do escopo:** não ocorreu. As correções (modo de demonstração e CSRF) atendem a pedidos do professor e
  da revisão técnica, sem novos requisitos funcionais; o RNF05 foi detalhado no DRE 3.2.
- **R5 – Perda de código ou documentos:** mitigado pelo repositório remoto e pelas tags de baseline.

## Horas reais

As horas reais **não foram medidas**. A dupla deve informar o tempo gasto em cada atividade concluída antes da
apresentação. Esse valor alimenta a revisão da produtividade de 2 h/PCU da EST.

## Como levar esta atualização para o arquivo .pod

1. No ProjectLibre, use **Arquivo › Abrir** e escolha `docs/03_CRO_Cade_Meu_Trem.xml`.
2. Confira se a linha de base 0 aparece e se a coluna **% físico concluído** mostra 100% nas atividades acima.
3. Confira na planilha de uso de recursos que cada atividade da R1 em diante tem Antony e Felipe com 50%.
4. Se tiverem as horas reais, preencha o **Trabalho real** das atividades concluídas.
5. Use **Arquivo › Salvar como** e substitua `docs/03_CRO_Cade_Meu_Trem.pod`.
6. Faça o commit na branch em andamento: `git commit -am "CRO: acompanhamento de 03/11 no .pod"`.
