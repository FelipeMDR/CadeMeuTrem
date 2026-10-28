# Gerência de configuração

Como o código e os documentos do Cadê Meu Trem? são versionados, revisados e congelados em cada release.

## Itens de configuração

| Item | Onde | Observação |
|---|---|---|
| Documento de Requisitos (DRE) | `docs/01_DRE_Cade_Meu_Trem.docx` + `.pdf` | Versão na tabela de revisões; o PDF acompanha cada alteração para leitura no GitHub. |
| Cronograma (CRO) | `docs/03_CRO_Cade_Meu_Trem.pod` + `.xml` | `.pod` é o arquivo do ProjectLibre; o `.xml` é a exportação legível. |
| Estimativa (EST), Matriz (MRB), Escopo/EAP, Plano | `docs/` | Atualizados quando a mudança os afeta. |
| Código-fonte | `app/` (Flask, templates e static), `data/esquema.sql`, `requirements.txt` | O banco `data/*.sqlite` **não** é versionado. |
| Testes | `tests/` | Suíte Selenium e gerador do relatório. |
| Registros de cada release | `docs/releases/RN/` | Relatório de testes, acompanhamento do cronograma e notas da release. |

## Branches

| Branch | Uso |
|---|---|
| `main` | Somente baselines aprovadas. Não recebe commits diretos. |
| `analise/release-0` | Branch de análise da R0 com os documentos entregues (DRE, EST, CRO, MRB). |
| `dev/release-N` | Branch em andamento da release N. Todos os commits de código, DRE e cronograma da release entram aqui. |

## Fluxo de uma release

1. Criar a branch em andamento a partir da `main`: `git switch main && git pull && git switch -c dev/release-2`.
2. Fazer commits pequenos, citando a atividade do cronograma ou o documento:
   - `A10: CRUD de objetos (RFS09 a RFS12)`
   - `DRE 3.3: ajusta regra de código do objeto`
   - `CRO: acompanhamento de 02/11`
3. Atualizar o cronograma e, quando necessário, o DRE na mesma branch (Aula 20-21, itens 3 e 4).
4. Rodar os testes (`scripts\testar.bat`) e gerar o relatório (`.venv\Scripts\python tests\gerar_relatorio.py R2`).
5. Abrir um Pull Request de `dev/release-N` para `main`. O outro integrante revisa e aprova.
6. Depois do merge, salvar a **baseline** com uma tag anotada e publicá-la:

   ```bash
   git switch main
   git pull
   git tag -a release-2 -m "Baseline R2 — objetos, empréstimos e devolução"
   git push origin release-2
   ```

7. Opcional: criar uma *Release* no GitHub a partir da tag, anexando o PDF do DRE e o relatório de testes.

## Baselines

| Tag | Conteúdo | Data |
|---|---|---|
| `release-0` | Documentos de análise da R0 (DRE 2.0, EST, CRO, MRB, escopo, plano). | Entregue em 22/10/2026; versionada em 26/10/2026 |
| `release-1` | Pessoas e categorias em Python + Flask, testes CT01/CT02/CT13, DRE 3.1, EST, CRO e MRB atualizados. | Após a revisão do PR da R1 (até 29/10/2026) |

Para consultar uma baseline: `git switch --detach release-0`. Para voltar: `git switch main`.

## Controle de mudanças

Toda mudança de escopo ou de tecnologia vira uma *issue* com o rótulo `mudança`. A issue registra os requisitos afetados e o impacto em
esforço e prazo. Mudanças que afetam a entrega combinada são discutidas com o professor antes de entrar na branch em
andamento (DRE, seção 5.1).

## Acompanhamento no GitHub

- **Milestones R1 a R4**, com as datas de entrega, mostram o progresso de cada release.
- **Issues**, uma por atividade do cronograma (A05, A06...), fecham pelo commit ou PR que as conclui (`Closes #N`).

## Situação verificada em 28/10/2026

O PR #17 foi integrado à main no commit `1e1b6b8`. A tag `release-1` ainda não estava publicada. As correções da revisão devem passar pelo mesmo fluxo de integração antes de congelar a baseline. Merge não comprova, por si só, aprovação individual dos dois integrantes.
