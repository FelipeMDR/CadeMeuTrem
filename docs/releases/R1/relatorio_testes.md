# Relatório de testes — Release 1

**Execução:** 27/10/2026 20:13 · **Resultado:** 37 de 37 cenários aprovados · **Duração:** 17.6 s

Testes funcionais automatizados com Selenium (Chrome headless). Cada execução usa um banco SQLite
temporário; o banco local em `data/` não é alterado. Para repetir: `scripts\testar.bat`.

## Ambiente

- Sistema: Windows 10 (10.0.26300)
- Python: 3.11.9
- Flask: 3.1.0
- Selenium: 4.27.1
- Navegador: chrome 156.0.8078.48
- ChromeDriver: 156.0.8078.73

## CT01 — Manter pessoas (RFS01 a RFS04): 20/20 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS01 | Incluir pessoa valida | Aprovado | 1.89 |
| RFS01 | Ativo inicia como sim | Aprovado | 0.06 |
| RFS01 | Espacos nas extremidades sao removidos | Aprovado | 0.19 |
| RFS01 | Nome obrigatorio preserva dados digitados | Aprovado | 0.20 |
| RFS01 | Limites de nome e contato | Aprovado | 0.60 |
| RFS01 | Homonimos sao permitidos | Aprovado | 0.42 |
| RFS01 | Texto com html e exibido como texto | Aprovado | 0.23 |
| RFS02 | Alterar pessoa mantem identificador | Aprovado | 1.43 |
| RFS02 | Alteracao aplica as mesmas validacoes | Aprovado | 0.78 |
| RFS02 | Reativar pessoa | Aprovado | 0.79 |
| RFS03 | Lista em ordem alfabetica | Aprovado | 0.27 |
| RFS03 | Desempate por identificador | Aprovado | 0.13 |
| RFS03 | Filtro por trecho do nome sem diferenciar maiusculas | Aprovado | 0.26 |
| RFS03 | Filtro ativo combinado por e | Aprovado | 0.21 |
| RFS03 | Sem resultados | Aprovado | 0.14 |
| RFS03 | Detalhe apresenta os mesmos campos | Aprovado | 0.14 |
| RFS04 | Cancelar exclusao preserva pessoa | Aprovado | 0.21 |
| RFS04 | Confirmar exclusao remove somente a pessoa | Aprovado | 0.23 |
| RFS04 | Exclusao bloqueada quando ha emprestimo | Aprovado | 0.18 |
| RFS04 | Vinculo revalidado na confirmacao | Aprovado | 0.28 |

## CT02 — Manter categorias (RFS05 a RFS08): 15/15 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RFS05 | Incluir categoria valida | Aprovado | 0.73 |
| RFS05 | Duplicidade desconsidera maiusculas e espacos | Aprovado | 0.99 |
| RFS05 | Duplicidade com acentos e maiusculas | Aprovado | 0.27 |
| RFS05 | Nome obrigatorio | Aprovado | 0.21 |
| RFS05 | Limite de 40 caracteres | Aprovado | 0.36 |
| RFS06 | Alterar categoria mantem identificador | Aprovado | 0.34 |
| RFS06 | Duplicidade desconsidera o proprio registro | Aprovado | 1.62 |
| RFS06 | Alteracao aplica as mesmas validacoes | Aprovado | 0.30 |
| RFS06 | Renomear mantem vinculo com objetos | Aprovado | 0.25 |
| RFS07 | Lista em ordem alfabetica | Aprovado | 0.23 |
| RFS07 | Filtro por trecho sem diferenciar maiusculas | Aprovado | 0.24 |
| RFS07 | Sem resultados | Aprovado | 0.14 |
| RFS08 | Cancelar exclusao preserva categoria | Aprovado | 0.19 |
| RFS08 | Confirmar exclusao remove somente a categoria | Aprovado | 0.21 |
| RFS08 | Exclusao bloqueada quando ha objeto | Aprovado | 0.14 |

## CT13 — Validação e proteção (RNF05), cenários antecipados: 2/2 aprovados

| Requisito | Cenário | Resultado | Tempo (s) |
|---|---|---|---|
| RNF05 | Parametros repetidos ou invalidos sao ignorados | Aprovado | 0.16 |
| RNF05 | Banco e codigo nao sao servidos | Aprovado | 2.21 |
