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
| R2 | 03/11/2026 (prevista para 05/11) | Objetos, empréstimos e devolução | Implementada e testada (101/101) · apresentação em 03/11 |
| R3 | 12/11/2026 | Relatório de pendências e atrasos | Planejada |
| R4 | 19/11/2026 | Histórico, regressão e pacote final | Planejada |

O detalhe de cada release está em [docs/releases](docs/releases/) ([R1](docs/releases/R1/notas_da_release.md) e
[R2](docs/releases/R2/notas_da_release.md)), e o progresso diário está nos *Milestones* e nas *Issues* do GitHub.

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

Testes funcionais com Selenium: 101 cenários, de CT01 a CT06, CT10 e CT13. Cada execução sobe a aplicação com um banco
temporário e abre o Chrome em modo headless; leva cerca de um minuto.

```bat
scripts\testar.bat
.venv\Scripts\python tests\gerar_relatorio.py R2
```

Para apresentar os testes, use o modo de demonstração. Ele abre o Chrome visível e destaca cada campo ou botão antes de
usá-lo. O texto é digitado letra por letra, e cada página fica na tela por um instante. No canto da página aparece o
cenário em execução (por exemplo, `CT01 · RFS01 — incluir pessoa valida`). Nesse modo, a suíte completa leva cerca de
10 minutos; na aula, rode um caso de teste ou um requisito.

```bat
scripts\demonstrar_testes.bat
scripts\demonstrar_testes.bat tests\selenium\test_ct01_pessoas.py
scripts\demonstrar_testes.bat -k rfs01
```

O primeiro comando roda tudo. O segundo roda só um caso de teste, e o terceiro só os cenários de um requisito. Para
mudar o ritmo, defina antes a pausa em segundos (o padrão é 0.8): `set PAUSA_SELENIUM=1.5`. Sem o modo de demonstração,
como no `testar.bat` e no GitHub Actions, os testes rodam sem janela e sem pausas. As falhas geram capturas de tela em
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
  objetos.py           RFS09 a RFS12 (/objetos/...)
  emprestimos.py       RFS13 a RFS17 (/emprestimos/...)
  datas.py             datas DD/MM/AAAA e dia atual no fuso America/Sao_Paulo
  protecao.py          token contra envio de formulários por outros sites (CSRF)
  templates/           páginas Jinja2 (escape automático de HTML)
  static/estilo.css    única pasta de arquivos servida
data/                  esquema.sql, exemplo.sql e o banco local (não versionado)
scripts/               iniciar, testar, demonstrar os testes e carregar exemplo
tests/selenium/        CT01 a CT06, CT10 e CT13 (cadastros, empréstimos, datas, integridade e proteção)
docs/                  DRE, EST, CRO, MRB, escopo, plano e registros das releases
requirements.txt       Flask, tzdata, Selenium e pytest
```

## Como trabalhamos

Branches, tags de baseline e convenções de commit estão em [docs/gerencia_configuracao.md](docs/gerencia_configuracao.md).
Em resumo: cada release tem uma branch `dev/release-N`, entra na `main` por Pull Request revisado pelo colega e é congelada
com uma tag de release (`release-0` na R0, `release1` na R1 e `release2` na R2).

Revisão de 28/10: [achados e pendências](docs/releases/R1/revisao_2026-10-28.md); o CSRF e o caminho do Chrome foram
tratados na R2. Cronograma XML atualizado para v2.4 em 03/11; apontamentos reais aguardam lançamento.
