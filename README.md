# Cadê Meu Trem?

Sistema web local para controlar empréstimos de objetos em uma república estudantil: quem retirou cada objeto, até
quando deve devolvê-lo e o que está atrasado. Trabalho final de Gerência de Projetos de Software (SDES06 — UNIFEI).

**Equipe:** Antony Souza Siqueira e Felipe Santana Medeiros

**Tecnologia:** Python 3.11+ com Flask e SQLite. Testes funcionais com Selenium (pytest) no Google Chrome.

## Andamento

| Release | Entrega | Conteúdo | Situação |
|---|---|---|---|
| R0 | 22/10/2026 | Escopo, DRE, EST, CRO, MRB e plano | Entregue · tag `release-0` |
| R1 | 29/10/2026 | Pessoas, categorias e testes Selenium | Entregue · tag `release1` |
| R2 | 05/11/2026 | Objetos, empréstimos e devolução | Planejada |
| R3 | 12/11/2026 | Relatório de pendências e atrasos | Planejada |
| R4 | 19/11/2026 | Histórico, regressão e pacote final | Planejada |

O detalhe da R1 está em [docs/releases/R1](docs/releases/R1/notas_da_release.md), e o progresso diário está nos
*Milestones* e nas *Issues* do GitHub.

## Executar

Pré-requisitos: Windows, Google Chrome e Python 3.11 ou superior.

```bat
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts\carregar_exemplo.py
scripts\iniciar.bat
```

Abra http://127.0.0.1:8000. O servidor atende somente a esta máquina. O banco fica em `data\cade_meu_trem.sqlite`, que não
é servido pela aplicação, e é criado na primeira execução. `carregar_exemplo.py` recria o banco com dados fictícios; use
`--substituir` para apagar um banco existente. Para uma cópia de segurança, copie o arquivo `.sqlite` com o servidor parado.

## Testes

Testes funcionais com Selenium. Cada execução sobe a aplicação com um banco temporário e abre o Chrome em modo headless.

```bat
scripts\testar.bat
.venv\Scripts\python tests\gerar_relatorio.py R1
```

Para ver o navegador durante os testes, defina `set MOSTRAR_NAVEGADOR=1`. As falhas geram capturas de tela em
`tests\selenium\saida\`.

## Estrutura

```
app/                   aplicação Flask
  __init__.py          cria a aplicação e registra os módulos
  db.py                conexão SQLite, funções de busca e transações
  valida.py            validações comuns
  telas.py             auxiliares das telas
  pessoas.py           RFS01 a RFS04 (/pessoas/...)
  categorias.py        RFS05 a RFS08 (/categorias/...)
  templates/           páginas Jinja2 (escape automático de HTML)
  static/estilo.css    única pasta de arquivos servida
data/                  esquema.sql, exemplo.sql e o banco local (não versionado)
scripts/               iniciar, testar e carregar exemplo
tests/selenium/        CT01 (pessoas), CT02 (categorias) e CT13 (proteção)
docs/                  DRE, EST, CRO, MRB, escopo, plano e registros das releases
requirements.txt       Flask, Selenium e pytest
```

## Como trabalhamos

Branches, tags de baseline e convenções de commit estão em [docs/gerencia_configuracao.md](docs/gerencia_configuracao.md).
Em resumo: cada release tem uma branch `dev/release-N`, entra na `main` por Pull Request revisado pelo colega e é congelada
com uma tag de release (`release-0` na R0 e `release1` na R1).

Revisão de 28/10: [achados e pendências](docs/releases/R1/revisao_2026-10-28.md). Cronograma .pod/XML atualizado para v2.3; apontamentos reais aguardam lançamento.
