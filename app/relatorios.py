"""Relatórios em tela — RFS18 Consultar pendências."""

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
