# Cadê Meu Trem?

Sistema web local para controlar empréstimos de objetos em uma república estudantil: quem retirou cada objeto, até
quando deve devolvê-lo e o que está atrasado. Trabalho final de Gerência de Projetos de Software (SDES06 — UNIFEI).

**Equipe:** Antony Souza Siqueira e Felipe Santana Medeiros

**Tecnologia:** Python 3.11+ com Flask e SQLite. Testes funcionais com Selenium (pytest) no Google Chrome.

**Como usar:** [manual do usuário](docs/manual_do_usuario.md).

## Andamento

| Release | Entrega | Conteúdo | Situação |
|---|---|---|---|
| R0 | 22/10/2026 | Escopo, DRE, EST, CRO, MRB e plano | Entregue · tag `release-0` |
| R1 | 29/10/2026 | Pessoas, categorias e testes Selenium | Entregue · tag `release1` |
| R2 | 03/11/2026 (prevista para 05/11) | Objetos, empréstimos e devolução | Entregue · tag `release2` |
| R3 | 17/11/2026 (prevista para 12/11) | Relatório de pendências e atrasos; objetos sem código | Implementada e testada · em revisão |
| R4 | 17/11/2026 (prevista para 19/11) | Histórico, regressão, instalação verificada e pacote final | Implementada e testada (129/129) · em revisão |

O detalhe de cada release está em [docs/releases](docs/releases/) ([R1](docs/releases/R1/notas_da_release.md),
[R2](docs/releases/R2/notas_da_release.md), [R3](docs/releases/R3/notas_da_release.md) e
[R4](docs/releases/R4/notas_da_release.md)), e o progresso diário está nos *Milestones* e nas *Issues* do GitHub.

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
`--substituir` para apagar um banco existente. Bancos criados antes da R3, com o código do objeto, são migrados
automaticamente ao abrir, sem perder dados.

### Cópia de segurança e restauração

Com o servidor parado (feche a janela do `iniciar.bat`), copie `data\cade_meu_trem.sqlite` para outro lugar. Para
restaurar, pare o servidor, copie o arquivo guardado de volta para `data\cade_meu_trem.sqlite` e inicie de novo. O teste
CT10 repete esse procedimento.

### Executar sem internet

A instalação das dependências precisa de internet uma única vez. Depois, a aplicação não usa nenhum arquivo de fora: todas
as páginas, estilos e dados ficam na máquina (verificado automaticamente pelo CT11). Para conferir: desligue a rede, rode
`scripts\iniciar.bat`, abra http://127.0.0.1:8000 e use os cadastros e os relatórios normalmente.

## Testes

Testes funcionais com Selenium: 129 cenários, de CT01 a CT13. Cada execução sobe a aplicação com um banco temporário e abre
o Chrome em modo headless; leva cerca de um minuto.

```bat
scripts\testar.bat
.venv\Scripts\python tests\gerar_relatorio.py R4
```

Para apresentar os testes, use o modo de demonstração. Ele abre o Chrome visível e destaca cada campo ou botão antes de
usá-lo. O texto é digitado letra por letra, e cada página fica na tela por um instante. No canto da página aparece o
cenário em execução (por exemplo, `CT01 · RFS01 — incluir pessoa valida`). Nesse modo, a suíte completa leva cerca de
15 minutos; na aula, rode um caso de teste ou um requisito.

```bat
scripts\demonstrar_testes.bat
scripts\demonstrar_testes.bat tests\selenium\test_ct07_pendencias.py
scripts\demonstrar_testes.bat -k rfs19
```

O primeiro comando roda tudo. O segundo roda só um caso de teste, e o terceiro só os cenários de um requisito. Para
mudar o ritmo, defina antes a pausa em segundos (o padrão é 0.8): `set PAUSA_SELENIUM=1.5`. Sem o modo de demonstração,
como no `testar.bat` e no GitHub Actions, os testes rodam sem janela e sem pausas. Se o Selenium não encontrar o Chrome,
informe o caminho em `set CHROME_BINARIO=...`. As falhas geram capturas de tela em `tests\selenium\saida\`.

## Estrutura

```
app/                   aplicação Flask
  __init__.py          cria a aplicação e registra os módulos
  db.py                conexão SQLite, transações e migração de bancos antigos
  valida.py            validações comuns
  telas.py             auxiliares das telas
  pessoas.py           RFS01 a RFS04 (/pessoas/...)
  categorias.py        RFS05 a RFS08 (/categorias/...)
  objetos.py           RFS09 a RFS12 (/objetos/...)
  emprestimos.py       RFS13 a RFS17 (/emprestimos/...)
  relatorios.py        RFS18 pendências e RFS19 histórico (/relatorios/...)
  datas.py             datas DD/MM/AAAA e dia atual no fuso America/Sao_Paulo
  protecao.py          token contra envio de formulários por outros sites (CSRF)
  templates/           páginas Jinja2 (escape automático de HTML)
  static/estilo.css    única pasta de arquivos servida
data/                  esquema.sql, exemplo.sql e o banco local (não versionado)
scripts/               iniciar, testar, demonstrar os testes e carregar exemplo
tests/selenium/        CT01 a CT13: cadastros, empréstimos, datas, relatórios, interface, integridade, execução local,
                       desempenho e proteção
docs/                  DRE, EST, CRO, MRB, escopo, plano, manual e registros das releases
requirements.txt       Flask, tzdata, Selenium e pytest
```

## Como trabalhamos

Branches, tags de baseline, convenções de commit e controle de mudanças estão em
[docs/gerencia_configuracao.md](docs/gerencia_configuracao.md). Em resumo: cada release tem uma branch `dev/release-N`,
entra na `main` por Pull Request revisado pelo colega e é congelada com uma tag de release (`release-0` na R0 e
`release1` a `release4` nas seguintes).
