"""Cadê Meu Trem? — controle de empréstimos de objetos (Flask + SQLite).

Execução local: flask --app app run --host 127.0.0.1 --port 8000
"""

from flask import Flask, render_template, url_for

from . import categorias, datas, db, emprestimos, objetos, pessoas, protecao
from .telas import pagina_nao_encontrada, sim_nao

NOME_SISTEMA = "Cadê Meu Trem?"
VERSAO_SISTEMA = "Release 2"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["BANCO"] = db.caminho_banco()
    db.iniciar(app)
    protecao.iniciar(app)
    for modulo in (pessoas, categorias, objetos, emprestimos):
        app.register_blueprint(modulo.bp)
    app.jinja_env.filters["data"] = datas.formatar

    @app.context_processor
    def dados_do_layout():
        return {"nome_sistema": NOME_SISTEMA, "versao_sistema": VERSAO_SISTEMA, "sim_nao": sim_nao}

    @app.get("/")
    def inicio():
        return render_template("inicio.html", titulo="Controle de empréstimos de objetos", pagina_atual="inicio")

    @app.errorhandler(404)
    def nao_encontrada(_erro):
        return pagina_nao_encontrada("Página não encontrada.", url_for("inicio"), "Ir para o início")

    return app
