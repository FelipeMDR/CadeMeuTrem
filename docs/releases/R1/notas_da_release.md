# Release 1 — Pessoas e categorias

**Entrega:** 29/10/2026 · **Branch em andamento:** `dev/release-1` · **Baseline:** tag `release-1` (criada após a revisão do PR)

## O que a Aula 20-21 pede e onde está

| # | Exigência | Situação | Onde |
|---|---|---|---|
| 1 | Implementação de 2 CRUDs | Feito | Pessoas (RFS01 a RFS04) em [`app/pessoas.py`](../../../app/pessoas.py); Categorias (RFS05 a RFS08) em [`app/categorias.py`](../../../app/categorias.py) |
| 2 | Teste automatizado dos CRUDs com Selenium | Feito: 37/37 aprovados (CT01: 20, CT02: 15, CT13: 2) | [`tests/selenium/`](../../../tests/selenium/) e [relatório](relatorio_testes.md) |
| 3 | Commits de código, DRE e cronograma na branch em andamento | Feito | Histórico da branch `dev/release-1` |
| 4 | Atualização periódica do cronograma e do DRE, sob controle de versão | CRO .pod/XML v2.2 revisados; horas reais pendentes | [DRE 3.1](../../01_DRE_Cade_Meu_Trem.pdf), [acompanhamento do CRO](acompanhamento_cronograma.md) |
| 5 | Baseline de gerência de configuração (tag) | PR #17 integrado; tag `release-1` pendente | [Gerência de configuração](../../gerencia_configuracao.md) |

## Entregue

- **Base da aplicação (A05):** Python + Flask + SQLite. O banco tem chaves estrangeiras, limites e o índice de um
  empréstimo aberto por objeto. Já existem as tabelas de objetos e empréstimos, para que as exclusões verifiquem vínculos.
  As telas são modelos Jinja2 em português, sem CDN; só `app/static` é servido, e banco e código ficam inacessíveis pela URL.
- **Pessoas (A06):**
  - inclusão com nome obrigatório (até 80) e contato opcional;
  - ativo Sim/Não;
  - alteração com identificador somente leitura;
  - consulta por trecho do nome e ativo, em ordem alfabética, com total e mensagem de vazio;
  - detalhe;
  - exclusão com confirmação, bloqueada quando há empréstimo.
- **Categorias (A07):**
  - nome obrigatório (até 40) e único, sem diferenciar maiúsculas nem espaços;
  - alteração que ignora o próprio registro na duplicidade;
  - consulta;
  - exclusão com confirmação, bloqueada quando há objeto.
- **Testes (A08):**
  - 20 cenários do CT01, 15 do CT02 e 2 do CT13 (proteção, antecipados da R2);
  - cada execução sobe a aplicação Flask com banco temporário;
  - salva captura de tela das falhas e grava as versões do ambiente.
- **Documentos (A09.1):**
  - DRE 3.1 no padrão SINFRA + Resumo de Regras (orientação do professor após a R0), com o ambiente Python + Flask;
  - MRB 2.1 com o resultado do CT01, do CT02 e do CT13;
  - EST 2.1 e plano resumido 2.1 com o ambiente da R1;
  - CRO v2.2 com revisão de 28/10 e progresso físico separado de esforço.

## Roteiro da demonstração (29/10)

1. `.venv\Scripts\python scripts\carregar_exemplo.py --substituir`, depois `scripts\iniciar.bat` e abrir http://127.0.0.1:8000.
2. **Pessoas:**
   - incluir uma pessoa;
   - tentar salvar sem nome (o erro preserva o contato digitado);
   - pesquisar por "an";
   - alterar e inativar;
   - excluir com confirmação.
3. **Categorias:**
   - incluir "Ferramentas" e tentar " ferramentas " (duplicidade);
   - renomear;
   - excluir com confirmação.
4. Rodar `scripts\testar.bat` (37 aprovados) e mostrar o [relatório](relatorio_testes.md).
5. Mostrar no GitHub:
   - a branch `dev/release-1`;
   - os commits com as atividades do cronograma;
   - o Pull Request;
   - as tags `release-0` e `release-1`.
6. Abrir o DRE 3.1 (seção 3.1, RFS01) e o cronograma no ProjectLibre (Gantt de acompanhamento com a linha de base).

## Pendências para a dupla

- [ ] Revisar o Pull Request da R1 (Antony e Felipe) e registrar a revisão.
- [ ] Transcrever apontamentos reais por atividade/integrante e atualizar atribuições no .pod v2.2.
- [x] Integrar o PR #17 na `main` (28/10, `1e1b6b8`).
- [ ] Integrar as correções desta revisão e criar a tag `release-1` (A09.2).
- [ ] Revisar a premissa de 2 h/PCU e o fator F08 da EST com as horas reais da R1.

## Fora desta release

Objetos, empréstimos e devolução (R2, 05/11); pendências (R3, 12/11); histórico (R4, 19/11). Nas exclusões com vínculo, o
teste de hoje prepara os objetos e empréstimos direto no banco. Ele será repetido pela tela quando esses cadastros existirem (R2).

## Revisão de 28/10

37/37 testes repetidos com sucesso. Consulte o [relatório de revisão](revisao_2026-10-28.md) e o [Status Report](status_report.md). Permanecem pendentes a proteção CSRF, os apontamentos reais, o registro de bugs em Mantis/Bugzilla e a confirmação do escopo final com o professor.
