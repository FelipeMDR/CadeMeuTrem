"""Conexão com o SQLite (RNF02). O banco fica em data/, fora dos arquivos servidos (RNF05)."""

import os
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path

from flask import current_app, g

from .valida import chave_ordenacao, minusculas

RAIZ = Path(__file__).resolve().parent.parent
ESQUEMA = RAIZ / "data" / "esquema.sql"
MAIOR_IDENTIFICADOR = 2**63 - 1  # maior inteiro do SQLite


def caminho_banco() -> str:
    return os.environ.get("CMT_DB") or str(RAIZ / "data" / "cade_meu_trem.sqlite")


def abrir(caminho: str) -> sqlite3.Connection:
    # isolation_level=None: cada comando grava sozinho; transações são abertas explicitamente.
    conexao = sqlite3.connect(caminho, isolation_level=None)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.execute("PRAGMA busy_timeout = 3000")
    # Busca sem diferenciar maiúsculas (inclusive acentuadas) e ordem alfabética que ignora acentos.
    conexao.create_function("minusculas", 1, lambda v: None if v is None else minusculas(v), deterministic=True)
    conexao.create_function("chave_ordenacao", 1, chave_ordenacao, deterministic=True)
    return conexao


def criar_esquema(caminho: str) -> None:
    """Executa data/esquema.sql; IF NOT EXISTS mantém os dados existentes."""
    with closing(abrir(caminho)) as conexao:
        conexao.executescript(ESQUEMA.read_text(encoding="utf-8"))


def iniciar(app) -> None:
    criar_esquema(app.config["BANCO"])
    app.teardown_appcontext(fechar)


def conexao() -> sqlite3.Connection:
    if "conexao" not in g:
        g.conexao = abrir(current_app.config["BANCO"])
    return g.conexao


def fechar(_erro=None) -> None:
    aberta = g.pop("conexao", None)
    if aberta is not None:
        aberta.close()


def consultar(sql: str, parametros=()) -> list[sqlite3.Row]:
    return conexao().execute(sql, parametros).fetchall()


def consultar_um(sql: str, parametros=()) -> sqlite3.Row | None:
    return conexao().execute(sql, parametros).fetchone()


@contextmanager
def transacao():
    """Transação que bloqueia escritas concorrentes até o fim (revalidação de vínculos)."""
    atual = conexao()
    atual.execute("BEGIN IMMEDIATE")
    try:
        yield atual
        atual.execute("COMMIT")
    except BaseException:
        atual.execute("ROLLBACK")
        raise


def eh_violacao_unicidade(erro: Exception) -> bool:
    return isinstance(erro, sqlite3.IntegrityError) and "UNIQUE constraint failed" in str(erro)
