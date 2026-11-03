"""Proteção contra envio de formulários por outros sites (CSRF) — RNF05.

Cada sessão recebe um token aleatório. Todo formulário POST o envia em um campo
oculto, e a aplicação recusa gravações sem o token correto.
"""

import os
import secrets

from flask import abort, render_template, request, session, url_for

CAMPO = "token_csrf"


def token() -> str:
    if CAMPO not in session:
        session[CAMPO] = secrets.token_urlsafe(32)
    return session[CAMPO]


def iniciar(app) -> None:
    # Sem CMT_CHAVE, a chave muda a cada execução: as sessões valem enquanto o servidor estiver aberto.
    app.secret_key = os.environ.get("CMT_CHAVE") or secrets.token_hex(32)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
    app.jinja_env.globals["token_csrf"] = token

    @app.before_request
    def conferir_token():
        if request.method != "POST":
            return None
        enviado = request.form.get(CAMPO, "")
        esperado = session.get(CAMPO, "")
        if not esperado or not secrets.compare_digest(enviado, esperado):
            abort(400)
        return None

    @app.errorhandler(400)
    def requisicao_recusada(_erro):
        return render_template("nao_encontrado.html", titulo="Requisição recusada",
                               mensagem_erro="O formulário expirou ou não veio desta aplicação. "
                                             "Nada foi gravado. Abra a página novamente e repita a operação.",
                               voltar_para=url_for("inicio"), rotulo_voltar="Ir para o início"), 400
