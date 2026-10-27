# Acompanhamento do cronograma — status em 27/10/2026

Atualização periódica do CRO (Aula 20-21, item 4). A linha de base 0 foi preservada; os valores abaixo
estão registrados em [`03_CRO_Cade_Meu_Trem.xml`](../../03_CRO_Cade_Meu_Trem.xml) (cronograma v2.1).

## Situação por release

| Release | Trabalho planejado | Concluído | % | Observação |
|---|---|---|---|---|
| R0 | 10 h (8 h base + 2 h reserva) | 8 h | 80% | Entregue em 22/10. A04.3 (versionar a análise) só foi concluída em 26/10. Reserva B00 não utilizada. |
| R1 | 17 h (15 h base + 2 h reserva) | 13 h | 76% | Base, pessoas, categorias, testes e documentos concluídos em 27/10. Faltam A09.2 (revisão e versão) e A09.3 (demonstração). Reserva B01 não utilizada. |
| R2 a R4 | 49 h | 0 h | 0% | Sem alteração; datas da linha de base mantidas. |

## Atividades concluídas

| Atividade | Fim na linha de base | Fim real | Desvio | Evidência |
|---|---|---|---|---|
| A04.3 Versionar documentação da R0 | 22/10 | 26/10 | +4 dias | branch `analise/release-0`, tag `release-0` |
| A05.1 Preparar ambiente local (Python, Flask e SQLite) | 23/10 | 27/10 | +4 dias | `requirements.txt`; commit `e998de3` |
| A05.2 Criar banco e regras de integridade | 24/10 | 27/10 | +3 dias | `data/esquema.sql`; commit `e998de3` |
| A05.3 Criar navegação e validações comuns | 24/10 | 27/10 | +3 dias | commit `e998de3` |
| A06.1 a A06.4 CRUD de pessoas | 24 a 25/10 | 27/10 | +2 a +3 dias | RFS01 a RFS04; commit `ec97672` |
| A07.1 a A07.4 CRUD de categorias | 25/10 | 27/10 | +2 dias | RFS05 a RFS08; commit `2c9f3a9` |
| A08.1 e A08.2 Testes de pessoas e categorias | 26/10 | 27/10 | +1 dia | CT01 (20 cenários) e CT02 (15); commit `314fd70` |
| A08.3 Registrar resultados e ajustar suíte | 27/10 | 27/10 | 0 | [relatório de testes](relatorio_testes.md): 37/37 aprovados |
| A09.1 Atualizar documentos da R1 | 28/10 | 27/10 | −1 dia | DRE 3.1, EST 2.1, MRB 2.1, plano resumido 2.1 e este acompanhamento |

**Pendente na R1:** A09.2 Revisar e versionar a R1 (revisão do Pull Request, merge e tag `release-1`) e A09.3 Demonstrar
pessoas e categorias (29/10). A reserva B01 (2 h, 27 e 28/10) continua disponível para correções antes da entrega. O marco
M1 continua em 29/10.

## Análise dos desvios e riscos

- As atividades da R1 terminaram de 1 a 4 dias depois da linha de base. Isso supera o limiar do risco **R2 – Atraso por
  outras atividades**: atraso maior que 20% da duração planejada de uma atividade necessária à release. A resposta foi
  concentrar a recuperação em 26 e 27/10, sem consumir a reserva B01. O marco M1 (29/10) foi preservado.
- **R3 – Dificuldade com ferramentas:** Flask e Selenium foram configurados e validados (37 cenários), dentro do limite de
  2 h do limiar.
- **R4 – Crescimento do escopo:** não ocorreu. Os 2 cenários antecipados do CT13 verificam proteções já exigidas pelo RNF05
  e não acrescentam funcionalidades.
- **R5 – Perda de código ou documentos:** mitigado pelo repositório remoto no GitHub com baselines por tag.

## Horas reais

As horas reais **não foram medidas**. O XML registra o trabalho real igual ao planejado, o padrão do ProjectLibre ao marcar
100%. Antes da apresentação, a dupla deve informar o tempo real gasto em cada atividade. Esse valor alimenta a revisão da
produtividade de 2 h/PCU prevista na EST após a R1.

## Como levar esta atualização para o arquivo .pod

O ProjectLibre não está instalado na máquina em que o XML foi atualizado. Para manter o `.pod` (arquivo principal) igual ao XML:

1. No ProjectLibre, use **Arquivo › Abrir** e escolha `docs/03_CRO_Cade_Meu_Trem.xml`.
2. Confira no Gantt de acompanhamento se a linha de base 0 aparece. As barras da R1 devem estar deslocadas para 27/10.
3. Se tiverem as horas reais, preencha o **Trabalho real** das atividades concluídas.
4. Use **Arquivo › Salvar como** e substitua `docs/03_CRO_Cade_Meu_Trem.pod`.
5. Faça o commit na branch em andamento: `git commit -am "CRO: acompanhamento de 27/10 no .pod"`.

Se a linha de base não vier na importação do XML, abra o `.pod` atual e marque manualmente o **% concluído**, o **Início real**
e o **Término real** das atividades da tabela acima. Depois, exporte o XML de novo.
