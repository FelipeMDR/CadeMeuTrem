"""Manter pessoas — RFS01 Incluir, RFS02 Alterar, RFS03 Consultar e RFS04 Excluir pessoa."""

from flask import Blueprint, redirect, render_template, request, url_for

from . import db
from .telas import pagina_nao_encontrada
from .valida import escapar_like, minusculas, texto_limpo, validar_texto, valor_sim_nao

bp = Blueprint("pessoas", __name__, url_prefix="/pessoas")

NOME_MAX = 80
CONTATO_MAX = 80

MENSAGENS = {
    "incluida": "Pessoa cadastrada com sucesso.",
    "alterada": "Pessoa alterada com sucesso.",
    "excluida": "Pessoa excluída com sucesso.",
}


def buscar(id_: int):
    if id_ > db.MAIOR_IDENTIFICADOR:
        return None
    return db.consultar_um("SELECT id, nome, contato, ativo FROM pessoa WHERE id = ?", (id_,))


def tem_emprestimos(conexao, id_: int) -> bool:
    return conexao.execute("SELECT 1 FROM emprestimo WHERE pessoa_id = ? LIMIT 1", (id_,)).fetchone() is not None


def nao_encontrada():
    return pagina_nao_encontrada("Pessoa não encontrada.", url_for("pessoas.consultar"), "Voltar para Pessoas")


def ler_formulario() -> dict:
    """Lê o formulário mantendo o que foi digitado, para reapresentar em caso de erro."""
    return {
        "nome": texto_limpo(request.form.get("nome")),
        "contato": texto_limpo(request.form.get("contato")),
        "ativo": request.form.get("ativo", ""),
    }


def validar(dados: dict) -> list[str]:
    erros = [
        validar_texto(dados["nome"], "Nome", NOME_MAX, True),
        validar_texto(dados["contato"], "Contato", CONTATO_MAX, False),
    ]
    if valor_sim_nao(dados["ativo"]) is None:
        erros.append("Ativo deve ser Sim ou Não.")
    return [erro for erro in erros if erro]


def formulario(id_: int | None, dados: dict, erros: list[str]):
    return render_template("pessoas/formulario.html", titulo="Incluir pessoa" if id_ is None else "Alterar pessoa",
                           pagina_atual="pessoas", id_=id_, dados=dados, erros=erros,
                           nome_max=NOME_MAX, contato_max=CONTATO_MAX)


# ---------------------------------------------------------------- RFS03

@bp.get("/")
def consultar():
    filtro_nome = texto_limpo(request.args.get("nome"))
    filtro_ativo = request.args.get("ativo", "")
    if filtro_ativo not in ("", "1", "0"):
        filtro_ativo = ""

    erro_filtro = validar_texto(filtro_nome, "O filtro Nome", NOME_MAX, False)
    pessoas = []
    if erro_filtro is None:
        sql = "SELECT id, nome, contato, ativo FROM pessoa WHERE 1 = 1"
        parametros = []
        if filtro_nome:
            sql += " AND minusculas(nome) LIKE ? ESCAPE '\\'"
            parametros.append(f"%{escapar_like(minusculas(filtro_nome))}%")
        if filtro_ativo:
            sql += " AND ativo = ?"
            parametros.append(int(filtro_ativo))
        sql += " ORDER BY chave_ordenacao(nome), id"
        pessoas = db.consultar(sql, parametros)

    return render_template("pessoas/consulta.html", titulo="Pessoas", pagina_atual="pessoas", pessoas=pessoas,
                           filtro_nome=filtro_nome, filtro_ativo=filtro_ativo, nome_max=NOME_MAX,
                           mensagem=MENSAGENS.get(request.args.get("ok", "")), mensagem_erro=erro_filtro)


@bp.get("/<int:id_>")
def detalhar(id_: int):
    pessoa = buscar(id_)
    if pessoa is None:
        return nao_encontrada()
    return render_template("pessoas/detalhe.html", titulo="Detalhe da pessoa", pagina_atual="pessoas", pessoa=pessoa)


# ---------------------------------------------------------------- RFS01 e RFS02

@bp.route("/incluir", methods=["GET", "POST"])
def incluir():
    if request.method == "GET":
        return formulario(None, {"nome": "", "contato": "", "ativo": "1"}, [])
    dados = ler_formulario()
    erros = validar(dados)
    if erros:
        return formulario(None, dados, erros)
    db.conexao().execute("INSERT INTO pessoa (nome, contato, ativo) VALUES (?, ?, ?)",
                         (dados["nome"], dados["contato"] or None, valor_sim_nao(dados["ativo"])))
    return redirect(url_for("pessoas.consultar", ok="incluida"), 303)


@bp.route("/<int:id_>/alterar", methods=["GET", "POST"])
def alterar(id_: int):
    pessoa = buscar(id_)
    if pessoa is None:
        return nao_encontrada()
    if request.method == "GET":
        return formulario(id_, {"nome": pessoa["nome"], "contato": pessoa["contato"] or "",
                                "ativo": str(pessoa["ativo"])}, [])
    dados = ler_formulario()
    erros = validar(dados)
    if erros:
        return formulario(id_, dados, erros)
    # O identificador não é alterado. Inativar não apaga nem encerra empréstimos.
    db.conexao().execute("UPDATE pessoa SET nome = ?, contato = ?, ativo = ? WHERE id = ?",
                         (dados["nome"], dados["contato"] or None, valor_sim_nao(dados["ativo"]), id_))
    return redirect(url_for("pessoas.consultar", ok="alterada"), 303)


# ---------------------------------------------------------------- RFS04

@bp.route("/<int:id_>/excluir", methods=["GET", "POST"])
def excluir(id_: int):
    pessoa = buscar(id_)
    if pessoa is None:
        return nao_encontrada()

    if request.method == "POST":
        # Revalida o vínculo no momento da gravação; não exclui empréstimos em cascata.
        with db.transacao() as conexao:
            bloqueada = tem_emprestimos(conexao, id_)
            if not bloqueada:
                conexao.execute("DELETE FROM pessoa WHERE id = ?", (id_,))
        if not bloqueada:
            return redirect(url_for("pessoas.consultar", ok="excluida"), 303)
    else:
        bloqueada = tem_emprestimos(db.conexao(), id_)

    erro = None
    if bloqueada:
        erro = (f'A pessoa "{pessoa["nome"]}" possui empréstimos registrados e não pode ser excluída. '
                "Ela pode ser inativada em Alterar pessoa.")
    return render_template("pessoas/excluir.html", titulo="Excluir pessoa", pagina_atual="pessoas",
                           pessoa=pessoa, bloqueada=bloqueada, mensagem_erro=erro)
