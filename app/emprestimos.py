"""Controlar empréstimos e devoluções — RFS13 Incluir, RFS14 Alterar, RFS15 Consultar,
RFS16 Excluir empréstimo e RFS17 Registrar devolução."""

import sqlite3
from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from . import datas, db
from .telas import ler_identificador, pagina_nao_encontrada
from .valida import texto_limpo, validar_texto

bp = Blueprint("emprestimos", __name__, url_prefix="/emprestimos")

OBSERVACAO_MAX = 250
SITUACOES = {"abertos": "Abertos", "devolvidos": "Devolvidos"}

MENSAGENS = {
    "incluido": "Empréstimo registrado com sucesso.",
    "alterado": "Empréstimo alterado com sucesso.",
    "excluido": "Empréstimo excluído com sucesso.",
    "devolvido": "Devolução registrada com sucesso.",
}

SQL_EMPRESTIMOS = """
    SELECT e.id, e.pessoa_id, p.nome AS pessoa, e.objeto_id, o.codigo, o.nome AS objeto,
           e.data_retirada, e.previsao_devolucao, e.data_devolucao, e.observacao,
           CASE WHEN e.data_devolucao IS NULL THEN 'Aberto' ELSE 'Devolvido' END AS situacao
    FROM emprestimo e
    JOIN pessoa p ON p.id = e.pessoa_id
    JOIN objeto o ON o.id = e.objeto_id
"""
SQL_OBJETOS_DISPONIVEIS = """
    SELECT o.id, o.codigo, o.nome FROM objeto o
    WHERE o.ativo = 1
      AND NOT EXISTS (SELECT 1 FROM emprestimo e WHERE e.objeto_id = o.id AND e.data_devolucao IS NULL)
    ORDER BY chave_ordenacao(o.nome), o.codigo, o.id
"""


def buscar(conexao, id_: int):
    if id_ > db.MAIOR_IDENTIFICADOR:
        return None
    return conexao.execute(SQL_EMPRESTIMOS + " WHERE e.id = ?", (id_,)).fetchone()


def nao_encontrado():
    return pagina_nao_encontrada("Empréstimo não encontrado.", url_for("emprestimos.consultar"),
                                 "Voltar para Empréstimos")


def pessoas_ativas() -> list:
    return db.consultar("SELECT id, nome FROM pessoa WHERE ativo = 1 ORDER BY chave_ordenacao(nome), id")


def objetos_disponiveis() -> list:
    return db.consultar(SQL_OBJETOS_DISPONIVEIS)


def validar_observacao(observacao: str) -> str | None:
    return validar_texto(observacao, "Observação", OBSERVACAO_MAX, False)


def validar_previsao(texto: str, retirada: date | None) -> tuple[date | None, str | None]:
    previsao, erro = datas.ler(texto, "Previsão de devolução")
    if erro is None and retirada is not None and previsao < retirada:
        return None, "Previsão de devolução deve ser igual ou posterior à data da retirada."
    return previsao, erro


# ---------------------------------------------------------------- RFS15

@bp.get("/")
def consultar():
    filtro = {
        "pessoa": request.args.get("pessoa", ""),
        "objeto": request.args.get("objeto", ""),
        "situacao": request.args.get("situacao", ""),
    }
    # Escolhas fechadas com valor desconhecido são ignoradas (RNF05).
    for campo in ("pessoa", "objeto"):
        if ler_identificador(filtro[campo]) is None:
            filtro[campo] = ""
    if filtro["situacao"] not in ("", *SITUACOES):
        filtro["situacao"] = ""

    sql = SQL_EMPRESTIMOS + " WHERE 1 = 1"
    parametros = []
    if filtro["pessoa"]:
        sql += " AND e.pessoa_id = ?"
        parametros.append(int(filtro["pessoa"]))
    if filtro["objeto"]:
        sql += " AND e.objeto_id = ?"
        parametros.append(int(filtro["objeto"]))
    if filtro["situacao"] == "abertos":
        sql += " AND e.data_devolucao IS NULL"
    elif filtro["situacao"] == "devolvidos":
        sql += " AND e.data_devolucao IS NOT NULL"
    sql += " ORDER BY e.data_retirada DESC, e.id DESC"

    # Os filtros incluem pessoas e objetos inativos.
    return render_template(
        "emprestimos/consulta.html", titulo="Empréstimos", pagina_atual="emprestimos",
        emprestimos=db.consultar(sql, parametros), filtro=filtro, situacoes=SITUACOES,
        pessoas=db.consultar("SELECT id, nome FROM pessoa ORDER BY chave_ordenacao(nome), id"),
        objetos=db.consultar("SELECT id, codigo, nome FROM objeto ORDER BY chave_ordenacao(nome), codigo, id"),
        mensagem=MENSAGENS.get(request.args.get("ok", "")))


@bp.get("/<int:id_>")
def detalhar(id_: int):
    emprestimo = buscar(db.conexao(), id_)
    if emprestimo is None:
        return nao_encontrado()
    return render_template("emprestimos/detalhe.html", titulo="Detalhe do empréstimo", pagina_atual="emprestimos",
                           emprestimo=emprestimo)


# ---------------------------------------------------------------- RFS13

def motivos_sem_elegiveis() -> list[str]:
    motivos = []
    if not pessoas_ativas():
        motivos.append("Não há pessoas ativas. Cadastre ou reative uma pessoa em Pessoas.")
    if not objetos_disponiveis():
        motivos.append("Não há objetos ativos e disponíveis. Cadastre um objeto ou registre a devolução de um "
                       "empréstimo aberto.")
    return motivos


def formulario_inclusao(dados: dict, erros: list[str]):
    return render_template("emprestimos/formulario.html", titulo="Incluir empréstimo", pagina_atual="emprestimos",
                           dados=dados, erros=erros, pessoas=pessoas_ativas(), objetos=objetos_disponiveis(),
                           observacao_max=OBSERVACAO_MAX)


def validar_inclusao(conexao, dados: dict) -> list[str]:
    """Valida o formulário e a elegibilidade de pessoa e objeto no momento da gravação."""
    erros = []
    if dados["pessoa"] == "":
        erros.append("Pessoa é obrigatória.")
    else:
        pessoa = conexao.execute("SELECT nome, ativo FROM pessoa WHERE id = ?",
                                 (ler_identificador(dados["pessoa"]) or 0,)).fetchone()
        if pessoa is None:
            erros.append("A pessoa selecionada não está cadastrada.")
        elif not pessoa["ativo"]:
            erros.append(f'A pessoa "{pessoa["nome"]}" está inativa e não pode retirar objetos.')

    if dados["objeto"] == "":
        erros.append("Objeto é obrigatório.")
    else:
        objeto = conexao.execute(
            "SELECT codigo, ativo, EXISTS (SELECT 1 FROM emprestimo e WHERE e.objeto_id = o.id"
            " AND e.data_devolucao IS NULL) AS emprestado FROM objeto o WHERE id = ?",
            (ler_identificador(dados["objeto"]) or 0,)).fetchone()
        if objeto is None:
            erros.append("O objeto selecionado não está cadastrado.")
        elif objeto["emprestado"]:
            erros.append(f'O objeto "{objeto["codigo"]}" já está emprestado.')
        elif not objeto["ativo"]:
            erros.append(f'O objeto "{objeto["codigo"]}" está inativo e não pode ser emprestado.')

    retirada, erro = datas.ler(dados["data_retirada"], "Data da retirada")
    if erro is None and retirada > datas.hoje():
        erro = "Data da retirada não pode ser posterior ao dia atual."
    erros.append(erro)
    erros.append(validar_previsao(dados["previsao"], retirada)[1])
    erros.append(validar_observacao(dados["observacao"]))
    return [e for e in erros if e]


@bp.route("/incluir", methods=["GET", "POST"])
def incluir():
    if request.method == "GET":
        motivos = motivos_sem_elegiveis()
        if motivos:
            return render_template("emprestimos/sem_elegiveis.html", titulo="Incluir empréstimo",
                                   pagina_atual="emprestimos", motivos=motivos)
        return formulario_inclusao({"pessoa": "", "objeto": "", "data_retirada": datas.formatar(datas.hoje()),
                                    "previsao": "", "observacao": ""}, [])

    dados = {campo: texto_limpo(request.form.get(campo))
             for campo in ("pessoa", "objeto", "data_retirada", "previsao", "observacao")}
    try:
        # Validação e gravação na mesma transação: a elegibilidade é revalidada ao gravar (RFS13).
        with db.transacao() as conexao:
            erros = validar_inclusao(conexao, dados)
            if not erros:
                conexao.execute(
                    "INSERT INTO emprestimo (pessoa_id, objeto_id, data_retirada, previsao_devolucao, observacao)"
                    " VALUES (?, ?, ?, ?, ?)",
                    (int(dados["pessoa"]), int(dados["objeto"]), datas.ler(dados["data_retirada"], "")[0].isoformat(),
                     datas.ler(dados["previsao"], "")[0].isoformat(), dados["observacao"] or None))
    except sqlite3.IntegrityError as erro:
        # O índice único do banco também impede dois empréstimos abertos do mesmo objeto (RNF02).
        if not db.eh_violacao_unicidade(erro):
            raise
        erros = ["O objeto selecionado já está emprestado."]
    if erros:
        return formulario_inclusao(dados, erros)
    return redirect(url_for("emprestimos.consultar", ok="incluido"), 303)


# ---------------------------------------------------------------- RFS14

@bp.route("/<int:id_>/alterar", methods=["GET", "POST"])
def alterar(id_: int):
    emprestimo = buscar(db.conexao(), id_)
    if emprestimo is None:
        return nao_encontrado()
    dados = {"previsao": datas.formatar(emprestimo["previsao_devolucao"]),
             "observacao": emprestimo["observacao"] or ""}
    erros = []
    if request.method == "POST":
        dados = {campo: texto_limpo(request.form.get(campo)) for campo in ("previsao", "observacao")}
        # Pessoa, objeto, retirada e devolução não são lidos do formulário: não podem ser alterados.
        with db.transacao() as conexao:
            atual = buscar(conexao, id_)
            aberto = atual["data_devolucao"] is None
            previsao = None
            if aberto:
                previsao, erro = validar_previsao(dados["previsao"], date.fromisoformat(atual["data_retirada"]))
                erros.append(erro)
            else:
                dados["previsao"] = datas.formatar(atual["previsao_devolucao"])
            erros.append(validar_observacao(dados["observacao"]))
            erros = [e for e in erros if e]
            if not erros:
                conexao.execute(
                    "UPDATE emprestimo SET previsao_devolucao = ?, observacao = ? WHERE id = ?",
                    (previsao.isoformat() if aberto else atual["previsao_devolucao"], dados["observacao"] or None,
                     id_))
        if not erros:
            return redirect(url_for("emprestimos.consultar", ok="alterado"), 303)
        emprestimo = atual
    return render_template("emprestimos/alterar.html", titulo="Alterar empréstimo", pagina_atual="emprestimos",
                           emprestimo=emprestimo, dados=dados, erros=erros, observacao_max=OBSERVACAO_MAX)


# ---------------------------------------------------------------- RFS16

@bp.route("/<int:id_>/excluir", methods=["GET", "POST"])
def excluir(id_: int):
    emprestimo = buscar(db.conexao(), id_)
    if emprestimo is None:
        return nao_encontrado()
    if request.method == "POST":
        # Remove somente o lançamento; pessoa e objeto continuam cadastrados.
        # A disponibilidade do objeto é calculada pelos empréstimos que restarem.
        db.conexao().execute("DELETE FROM emprestimo WHERE id = ?", (id_,))
        return redirect(url_for("emprestimos.consultar", ok="excluido"), 303)
    return render_template("emprestimos/excluir.html", titulo="Excluir empréstimo", pagina_atual="emprestimos",
                           emprestimo=emprestimo)


# ---------------------------------------------------------------- RFS17

def ja_devolvido(emprestimo):
    texto = (f"Este empréstimo já foi devolvido em {datas.formatar(emprestimo['data_devolucao'])}. "
             "A devolução não pode ser registrada novamente nem desfeita.")
    return render_template("emprestimos/devolver.html", titulo="Registrar devolução", pagina_atual="emprestimos",
                           emprestimo=emprestimo, devolvido=True, mensagem_erro=texto)


@bp.route("/<int:id_>/devolver", methods=["GET", "POST"])
def devolver(id_: int):
    emprestimo = buscar(db.conexao(), id_)
    if emprestimo is None:
        return nao_encontrado()
    if emprestimo["data_devolucao"] is not None:
        return ja_devolvido(emprestimo)

    data_texto = datas.formatar(datas.hoje())
    erros = []
    if request.method == "POST":
        data_texto = texto_limpo(request.form.get("data_devolucao"))
        devolucao, erro = datas.ler(data_texto, "Data da devolução")
        retirada = date.fromisoformat(emprestimo["data_retirada"])
        if erro is None and not retirada <= devolucao <= datas.hoje():
            erro = (f"Data da devolução deve estar entre a data da retirada ({datas.formatar(retirada)}) "
                    f"e o dia atual ({datas.formatar(datas.hoje())}).")
        if erro:
            erros = [erro]
        else:
            with db.transacao() as conexao:
                # Só encerra se ainda estiver aberto: não há devolução repetida.
                gravou = conexao.execute(
                    "UPDATE emprestimo SET data_devolucao = ? WHERE id = ? AND data_devolucao IS NULL",
                    (devolucao.isoformat(), id_)).rowcount
            if not gravou:
                return ja_devolvido(buscar(db.conexao(), id_))
            return redirect(url_for("emprestimos.consultar", ok="devolvido"), 303)
    return render_template("emprestimos/devolver.html", titulo="Registrar devolução", pagina_atual="emprestimos",
                           emprestimo=emprestimo, devolvido=False, data_devolucao=data_texto, erros=erros)
