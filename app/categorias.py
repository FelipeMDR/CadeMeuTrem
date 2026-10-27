"""Manter categorias — RFS05 Incluir, RFS06 Alterar, RFS07 Consultar e RFS08 Excluir categoria."""

import sqlite3

from flask import Blueprint, redirect, render_template, request, url_for

from . import db
from .telas import pagina_nao_encontrada
from .valida import escapar_like, minusculas, texto_limpo, validar_texto

bp = Blueprint("categorias", __name__, url_prefix="/categorias")

NOME_MAX = 40
DUPLICADA = "Já existe uma categoria com este nome."

MENSAGENS = {
    "incluida": "Categoria cadastrada com sucesso.",
    "alterada": "Categoria alterada com sucesso.",
    "excluida": "Categoria excluída com sucesso.",
}


def buscar(id_: int):
    if id_ > db.MAIOR_IDENTIFICADOR:
        return None
    return db.consultar_um("SELECT id, nome FROM categoria WHERE id = ?", (id_,))


def tem_objetos(conexao, id_: int) -> bool:
    return conexao.execute("SELECT 1 FROM objeto WHERE categoria_id = ? LIMIT 1", (id_,)).fetchone() is not None


def nao_encontrada():
    return pagina_nao_encontrada("Categoria não encontrada.", url_for("categorias.consultar"), "Voltar para Categorias")


def chave(nome: str) -> str:
    """"Ferramentas" e " ferramentas " têm a mesma chave."""
    return minusculas(nome.strip())


def nome_em_uso(nome: str, ignorar_id: int | None) -> bool:
    """Verifica duplicidade desconsiderando maiúsculas e, na alteração, o próprio registro."""
    linha = db.consultar_um("SELECT 1 FROM categoria WHERE nome_chave = ? AND id IS NOT ? LIMIT 1",
                            (chave(nome), ignorar_id))
    return linha is not None


def validar(nome: str, ignorar_id: int | None) -> list[str]:
    erro = validar_texto(nome, "Nome", NOME_MAX, True)
    if erro:
        return [erro]
    return [DUPLICADA] if nome_em_uso(nome, ignorar_id) else []


def formulario(id_: int | None, nome: str, erros: list[str]):
    return render_template("categorias/formulario.html",
                           titulo="Incluir categoria" if id_ is None else "Alterar categoria",
                           pagina_atual="categorias", id_=id_, nome=nome, erros=erros, nome_max=NOME_MAX)


def gravar(sql: str, parametros: tuple) -> list[str]:
    """Grava e traduz a violação de unicidade do banco na mensagem de duplicidade."""
    try:
        db.conexao().execute(sql, parametros)
    except sqlite3.IntegrityError as erro:
        if not db.eh_violacao_unicidade(erro):
            raise
        return [DUPLICADA]
    return []


# ---------------------------------------------------------------- RFS07

@bp.get("/")
def consultar():
    filtro_nome = texto_limpo(request.args.get("nome"))
    erro_filtro = validar_texto(filtro_nome, "O filtro Nome", NOME_MAX, False)
    categorias = []
    if erro_filtro is None:
        sql = "SELECT id, nome FROM categoria"
        parametros = []
        if filtro_nome:
            sql += " WHERE minusculas(nome) LIKE ? ESCAPE '\\'"
            parametros.append(f"%{escapar_like(minusculas(filtro_nome))}%")
        sql += " ORDER BY chave_ordenacao(nome), id"
        categorias = db.consultar(sql, parametros)

    return render_template("categorias/consulta.html", titulo="Categorias", pagina_atual="categorias",
                           categorias=categorias, filtro_nome=filtro_nome, nome_max=NOME_MAX,
                           mensagem=MENSAGENS.get(request.args.get("ok", "")), mensagem_erro=erro_filtro)


# ---------------------------------------------------------------- RFS05 e RFS06

@bp.route("/incluir", methods=["GET", "POST"])
def incluir():
    if request.method == "GET":
        return formulario(None, "", [])
    nome = texto_limpo(request.form.get("nome"))
    erros = validar(nome, None) or gravar("INSERT INTO categoria (nome, nome_chave) VALUES (?, ?)",
                                          (nome, chave(nome)))
    if erros:
        return formulario(None, nome, erros)
    return redirect(url_for("categorias.consultar", ok="incluida"), 303)


@bp.route("/<int:id_>/alterar", methods=["GET", "POST"])
def alterar(id_: int):
    categoria = buscar(id_)
    if categoria is None:
        return nao_encontrada()
    if request.method == "GET":
        return formulario(id_, categoria["nome"], [])
    nome = texto_limpo(request.form.get("nome"))
    # Renomear mantém os vínculos: os objetos referenciam o identificador.
    erros = validar(nome, id_) or gravar("UPDATE categoria SET nome = ?, nome_chave = ? WHERE id = ?",
                                         (nome, chave(nome), id_))
    if erros:
        return formulario(id_, nome, erros)
    return redirect(url_for("categorias.consultar", ok="alterada"), 303)


# ---------------------------------------------------------------- RFS08

@bp.route("/<int:id_>/excluir", methods=["GET", "POST"])
def excluir(id_: int):
    categoria = buscar(id_)
    if categoria is None:
        return nao_encontrada()

    if request.method == "POST":
        # Revalida o vínculo ao gravar; não exclui objetos em cascata.
        with db.transacao() as conexao:
            bloqueada = tem_objetos(conexao, id_)
            if not bloqueada:
                conexao.execute("DELETE FROM categoria WHERE id = ?", (id_,))
        if not bloqueada:
            return redirect(url_for("categorias.consultar", ok="excluida"), 303)
    else:
        bloqueada = tem_objetos(db.conexao(), id_)

    erro = None
    if bloqueada:
        erro = (f'A categoria "{categoria["nome"]}" possui objetos vinculados e não pode ser excluída. '
                "Altere a categoria desses objetos antes de excluí-la.")
    return render_template("categorias/excluir.html", titulo="Excluir categoria", pagina_atual="categorias",
                           categoria=categoria, bloqueada=bloqueada, mensagem_erro=erro)
