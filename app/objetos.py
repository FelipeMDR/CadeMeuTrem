"""Manter objetos — RFS09 Incluir, RFS10 Alterar, RFS11 Consultar e RFS12 Excluir objeto."""

import sqlite3

from flask import Blueprint, redirect, render_template, request, url_for

from . import db
from .telas import ler_identificador, pagina_nao_encontrada
from .valida import escapar_like, minusculas, texto_limpo, validar_texto, valor_sim_nao

bp = Blueprint("objetos", __name__, url_prefix="/objetos")

CODIGO_MAX = 20
NOME_MAX = 80
OBSERVACAO_MAX = 250
CODIGO_DUPLICADO = "Já existe um objeto com este código."
SEM_CATEGORIAS = "Não há categorias cadastradas. Cadastre uma categoria antes de incluir objetos."

MENSAGENS = {
    "incluido": "Objeto cadastrado com sucesso.",
    "alterado": "Objeto alterado com sucesso.",
    "excluido": "Objeto excluído com sucesso.",
}

# Disponibilidade calculada (RFS09): Emprestado se houver empréstimo aberto; senão Disponível ou Inativo.
DISPONIBILIDADES = {"disponivel": "Disponível", "emprestado": "Emprestado", "inativo": "Inativo"}
SQL_OBJETOS = """
    SELECT * FROM (
        SELECT o.id, o.codigo, o.nome, o.observacao, o.ativo, o.categoria_id, c.nome AS categoria,
               CASE WHEN EXISTS (SELECT 1 FROM emprestimo e WHERE e.objeto_id = o.id AND e.data_devolucao IS NULL)
                        THEN 'Emprestado'
                    WHEN o.ativo = 1 THEN 'Disponível'
                    ELSE 'Inativo' END AS disponibilidade
        FROM objeto o JOIN categoria c ON c.id = o.categoria_id
    ) AS objetos
"""


def normalizar_codigo(valor: str) -> str:
    """" fur001 " e "FUR001" são o mesmo código."""
    return texto_limpo(valor).upper()


def buscar(id_: int):
    if id_ > db.MAIOR_IDENTIFICADOR:
        return None
    return db.consultar_um(SQL_OBJETOS + " WHERE id = ?", (id_,))


def categorias() -> list:
    return db.consultar("SELECT id, nome FROM categoria ORDER BY chave_ordenacao(nome), id")


def tem_emprestimos(conexao, id_: int) -> bool:
    return conexao.execute("SELECT 1 FROM emprestimo WHERE objeto_id = ? LIMIT 1", (id_,)).fetchone() is not None


def nao_encontrado():
    return pagina_nao_encontrada("Objeto não encontrado.", url_for("objetos.consultar"), "Voltar para Objetos")


def ler_formulario() -> dict:
    """Lê o formulário mantendo o que foi digitado, para reapresentar em caso de erro."""
    return {
        "codigo": normalizar_codigo(request.form.get("codigo")),
        "nome": texto_limpo(request.form.get("nome")),
        "categoria": texto_limpo(request.form.get("categoria")),
        "observacao": texto_limpo(request.form.get("observacao")),
        "ativo": request.form.get("ativo", ""),
    }


def validar(dados: dict, ignorar_id: int | None) -> list[str]:
    erro_codigo = validar_texto(dados["codigo"], "Código", CODIGO_MAX, True)
    if erro_codigo is None and codigo_em_uso(dados["codigo"], ignorar_id):
        erro_codigo = CODIGO_DUPLICADO
    erros = [erro_codigo, validar_texto(dados["nome"], "Nome", NOME_MAX, True)]
    if dados["categoria"] == "":
        erros.append("Categoria é obrigatória.")
    else:
        id_categoria = ler_identificador(dados["categoria"])
        if id_categoria is None or db.consultar_um("SELECT 1 FROM categoria WHERE id = ?", (id_categoria,)) is None:
            erros.append("A categoria selecionada não está cadastrada. Escolha uma categoria da lista.")
    erros.append(validar_texto(dados["observacao"], "Observação", OBSERVACAO_MAX, False))
    if valor_sim_nao(dados["ativo"]) is None:
        erros.append("Ativo deve ser Sim ou Não.")
    return [erro for erro in erros if erro]


def codigo_em_uso(codigo: str, ignorar_id: int | None) -> bool:
    """Na alteração, o próprio objeto não conta como duplicidade (RFS10)."""
    return db.consultar_um("SELECT 1 FROM objeto WHERE codigo = ? AND id IS NOT ? LIMIT 1",
                           (codigo, ignorar_id)) is not None


def gravar(sql: str, parametros: tuple) -> list[str]:
    """Grava e traduz a violação de unicidade do código na mensagem de duplicidade."""
    try:
        db.conexao().execute(sql, parametros)
    except sqlite3.IntegrityError as erro:
        if db.eh_violacao_unicidade(erro):
            return [CODIGO_DUPLICADO]
        if "FOREIGN KEY" in str(erro):
            return ["A categoria selecionada não está cadastrada. Escolha uma categoria da lista."]
        raise
    return []


def formulario(objeto, dados: dict, erros: list[str]):
    return render_template("objetos/formulario.html", titulo="Incluir objeto" if objeto is None else "Alterar objeto",
                           pagina_atual="objetos", objeto=objeto, dados=dados, erros=erros, categorias=categorias(),
                           codigo_max=CODIGO_MAX, nome_max=NOME_MAX, observacao_max=OBSERVACAO_MAX)


def parametros_gravacao(dados: dict) -> tuple:
    return (dados["codigo"], dados["nome"], int(dados["categoria"]), dados["observacao"] or None,
            valor_sim_nao(dados["ativo"]))


# ---------------------------------------------------------------- RFS11

@bp.get("/")
def consultar():
    filtro = {
        "codigo": normalizar_codigo(request.args.get("codigo")),
        "nome": texto_limpo(request.args.get("nome")),
        "categoria": request.args.get("categoria", ""),
        "ativo": request.args.get("ativo", ""),
        "disponibilidade": request.args.get("disponibilidade", ""),
    }
    # Escolhas fechadas com valor desconhecido são ignoradas (RNF05).
    if ler_identificador(filtro["categoria"]) is None:
        filtro["categoria"] = ""
    if filtro["ativo"] not in ("", "1", "0"):
        filtro["ativo"] = ""
    if filtro["disponibilidade"] not in ("", *DISPONIBILIDADES):
        filtro["disponibilidade"] = ""

    erro_filtro = (validar_texto(filtro["codigo"], "O filtro Código", CODIGO_MAX, False)
                   or validar_texto(filtro["nome"], "O filtro Nome", NOME_MAX, False))
    objetos = []
    if erro_filtro is None:
        sql = SQL_OBJETOS + " WHERE 1 = 1"
        parametros = []
        if filtro["codigo"]:
            sql += " AND codigo = ?"
            parametros.append(filtro["codigo"])
        if filtro["nome"]:
            sql += " AND minusculas(nome) LIKE ? ESCAPE '\\'"
            parametros.append(f"%{escapar_like(minusculas(filtro['nome']))}%")
        if filtro["categoria"]:
            sql += " AND categoria_id = ?"
            parametros.append(int(filtro["categoria"]))
        if filtro["ativo"]:
            sql += " AND ativo = ?"
            parametros.append(int(filtro["ativo"]))
        if filtro["disponibilidade"]:
            sql += " AND disponibilidade = ?"
            parametros.append(DISPONIBILIDADES[filtro["disponibilidade"]])
        sql += " ORDER BY chave_ordenacao(nome), codigo, id"
        objetos = db.consultar(sql, parametros)

    return render_template("objetos/consulta.html", titulo="Objetos", pagina_atual="objetos", objetos=objetos,
                           filtro=filtro, categorias=categorias(), disponibilidades=DISPONIBILIDADES,
                           codigo_max=CODIGO_MAX, nome_max=NOME_MAX,
                           mensagem=MENSAGENS.get(request.args.get("ok", "")), mensagem_erro=erro_filtro)


@bp.get("/<int:id_>")
def detalhar(id_: int):
    objeto = buscar(id_)
    if objeto is None:
        return nao_encontrado()
    return render_template("objetos/detalhe.html", titulo="Detalhe do objeto", pagina_atual="objetos", objeto=objeto)


# ---------------------------------------------------------------- RFS09 e RFS10

@bp.route("/incluir", methods=["GET", "POST"])
def incluir():
    if not categorias():
        # RFS09, regra 2: a categoria não é criada automaticamente.
        return render_template("objetos/sem_categorias.html", titulo="Incluir objeto", pagina_atual="objetos",
                               mensagem_erro=SEM_CATEGORIAS)
    if request.method == "GET":
        return formulario(None, {"codigo": "", "nome": "", "categoria": "", "observacao": "", "ativo": "1"}, [])
    dados = ler_formulario()
    erros = validar(dados, None) or gravar(
        "INSERT INTO objeto (codigo, nome, categoria_id, observacao, ativo) VALUES (?, ?, ?, ?, ?)",
        parametros_gravacao(dados))
    if erros:
        return formulario(None, dados, erros)
    return redirect(url_for("objetos.consultar", ok="incluido"), 303)


@bp.route("/<int:id_>/alterar", methods=["GET", "POST"])
def alterar(id_: int):
    objeto = buscar(id_)
    if objeto is None:
        return nao_encontrado()
    if request.method == "GET":
        return formulario(objeto, {"codigo": objeto["codigo"], "nome": objeto["nome"],
                                   "categoria": str(objeto["categoria_id"]), "observacao": objeto["observacao"] or "",
                                   "ativo": str(objeto["ativo"])}, [])
    dados = ler_formulario()
    # Identificador e Disponibilidade não são alterados. Inativar não encerra o empréstimo aberto.
    erros = validar(dados, id_) or gravar(
        "UPDATE objeto SET codigo = ?, nome = ?, categoria_id = ?, observacao = ?, ativo = ? WHERE id = ?",
        (*parametros_gravacao(dados), id_))
    if erros:
        return formulario(objeto, dados, erros)
    return redirect(url_for("objetos.consultar", ok="alterado"), 303)


# ---------------------------------------------------------------- RFS12

@bp.route("/<int:id_>/excluir", methods=["GET", "POST"])
def excluir(id_: int):
    objeto = buscar(id_)
    if objeto is None:
        return nao_encontrado()

    if request.method == "POST":
        # Revalida o vínculo ao gravar; não exclui empréstimos em cascata.
        with db.transacao() as conexao:
            bloqueado = tem_emprestimos(conexao, id_)
            if not bloqueado:
                conexao.execute("DELETE FROM objeto WHERE id = ?", (id_,))
        if not bloqueado:
            return redirect(url_for("objetos.consultar", ok="excluido"), 303)
    else:
        bloqueado = tem_emprestimos(db.conexao(), id_)

    erro = None
    if bloqueado:
        erro = (f'O objeto "{objeto["codigo"]} – {objeto["nome"]}" possui empréstimos registrados e não pode ser '
                "excluído. Ele pode ser inativado em Alterar objeto.")
    return render_template("objetos/excluir.html", titulo="Excluir objeto", pagina_atual="objetos",
                           objeto=objeto, bloqueado=bloqueado, mensagem_erro=erro)
