"""Relatórios em tela — RFS18 Consultar pendências e RFS19 Consultar histórico."""

from flask import Blueprint, render_template, request

from . import datas, db
from .telas import ler_identificador

bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")

# Atrasado: aberto com previsão anterior ao dia atual; vencer hoje não é atraso (RFS18).
SQL_PENDENCIAS = """
    SELECT e.id, e.objeto_id, o.nome AS objeto, c.nome AS categoria, p.nome AS pessoa,
           e.data_retirada, e.previsao_devolucao,
           MAX(0, CAST(julianday(:hoje) - julianday(e.previsao_devolucao) AS INTEGER)) AS dias_atraso
    FROM emprestimo e
    JOIN objeto o ON o.id = e.objeto_id
    JOIN categoria c ON c.id = o.categoria_id
    JOIN pessoa p ON p.id = e.pessoa_id
    WHERE e.data_devolucao IS NULL
"""


def pessoas_e_categorias() -> dict:
    """Opções dos filtros: pessoas inclusive inativas e todas as categorias."""
    return {
        "pessoas": db.consultar("SELECT id, nome FROM pessoa ORDER BY chave_ordenacao(nome), id"),
        "categorias": db.consultar("SELECT id, nome FROM categoria ORDER BY chave_ordenacao(nome), id"),
    }


# ---------------------------------------------------------------- RFS18

@bp.get("/pendencias")
def pendencias():
    filtro = {
        "pessoa": request.args.get("pessoa", ""),
        "categoria": request.args.get("categoria", ""),
        "atrasados": request.args.get("atrasados", "0"),
    }
    # Escolhas fechadas com valor desconhecido são ignoradas (RNF05).
    for campo in ("pessoa", "categoria"):
        if ler_identificador(filtro[campo]) is None:
            filtro[campo] = ""
    if filtro["atrasados"] not in ("0", "1"):
        filtro["atrasados"] = "0"

    # Pessoas e objetos inativos continuam no resultado enquanto o empréstimo estiver aberto.
    sql = SQL_PENDENCIAS
    parametros = {"hoje": datas.hoje().isoformat()}
    if filtro["pessoa"]:
        sql += " AND e.pessoa_id = :pessoa"
        parametros["pessoa"] = int(filtro["pessoa"])
    if filtro["categoria"]:
        sql += " AND o.categoria_id = :categoria"
        parametros["categoria"] = int(filtro["categoria"])
    if filtro["atrasados"] == "1":
        sql += " AND e.previsao_devolucao < :hoje"
    sql += " ORDER BY (e.previsao_devolucao < :hoje) DESC, e.previsao_devolucao, e.id"
    linhas = db.consultar(sql, parametros)

    return render_template("relatorios/pendencias.html", titulo="Pendências e atrasos", pagina_atual="pendencias",
                           linhas=linhas, filtro=filtro, atrasados=sum(1 for linha in linhas if linha["dias_atraso"]),
                           hoje=datas.hoje(), **pessoas_e_categorias())


# ---------------------------------------------------------------- RFS19

SITUACOES = {"abertos": "Abertos", "devolvidos": "Devolvidos"}
SQL_HISTORICO = """
    SELECT e.id, p.nome AS pessoa, e.objeto_id, o.nome AS objeto, e.data_retirada, e.previsao_devolucao,
           e.data_devolucao, CASE WHEN e.data_devolucao IS NULL THEN 'Aberto' ELSE 'Devolvido' END AS situacao
    FROM emprestimo e
    JOIN pessoa p ON p.id = e.pessoa_id
    JOIN objeto o ON o.id = e.objeto_id
    WHERE e.data_retirada BETWEEN :inicio AND :fim
"""


def validar_periodo(inicio_texto: str, fim_texto: str) -> tuple[list[str], dict]:
    """Período obrigatório da retirada; datas inválidas ou intervalo invertido impedem a consulta."""
    inicio, erro_inicio = datas.ler(inicio_texto, "Retirada inicial")
    fim, erro_fim = datas.ler(fim_texto, "Retirada final")
    erros = [erro for erro in (erro_inicio, erro_fim) if erro]
    if not erros and fim < inicio:
        erros.append("Retirada final deve ser igual ou posterior à retirada inicial.")
    return erros, {"inicio": inicio.isoformat() if inicio else None, "fim": fim.isoformat() if fim else None}


@bp.get("/historico")
def historico():
    hoje = datas.hoje()
    # Sem período informado, vale o mês atual até hoje; campo enviado vazio é erro de preenchimento.
    filtro = {
        "inicio": request.args.get("inicio", datas.formatar(hoje.replace(day=1))).strip(),
        "fim": request.args.get("fim", datas.formatar(hoje)).strip(),
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

    erros, parametros = validar_periodo(filtro["inicio"], filtro["fim"])
    linhas = []
    if not erros:
        sql = SQL_HISTORICO
        if filtro["pessoa"]:
            sql += " AND e.pessoa_id = :pessoa"
            parametros["pessoa"] = int(filtro["pessoa"])
        if filtro["objeto"]:
            sql += " AND e.objeto_id = :objeto"
            parametros["objeto"] = int(filtro["objeto"])
        if filtro["situacao"] == "abertos":
            sql += " AND e.data_devolucao IS NULL"
        elif filtro["situacao"] == "devolvidos":
            sql += " AND e.data_devolucao IS NOT NULL"
        sql += " ORDER BY e.data_retirada DESC, e.id DESC"
        linhas = db.consultar(sql, parametros)

    abertos = sum(1 for linha in linhas if linha["situacao"] == "Aberto")
    return render_template(
        "relatorios/historico.html", titulo="Histórico de empréstimos", pagina_atual="historico", linhas=linhas,
        filtro=filtro, erros=erros, situacoes=SITUACOES, abertos=abertos, devolvidos=len(linhas) - abertos,
        pessoas=db.consultar("SELECT id, nome FROM pessoa ORDER BY chave_ordenacao(nome), id"),
        objetos=db.consultar("SELECT id, nome FROM objeto ORDER BY chave_ordenacao(nome), id"))
