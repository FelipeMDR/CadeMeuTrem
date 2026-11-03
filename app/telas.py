"""Auxiliares comuns das telas (RNF01)."""

from flask import render_template

from .db import MAIOR_IDENTIFICADOR


def sim_nao(valor) -> str:
    return "Sim" if int(valor) == 1 else "Não"


def pagina_nao_encontrada(texto: str, voltar_para: str, rotulo_voltar: str):
    return render_template("nao_encontrado.html", titulo="Registro não encontrado", mensagem_erro=texto,
                           voltar_para=voltar_para, rotulo_voltar=rotulo_voltar), 404


def ler_identificador(valor) -> int | None:
    """Identificador escolhido em lista ou filtro: inteiro positivo dentro do limite do SQLite."""
    if isinstance(valor, str) and valor.isascii() and valor.isdigit():
        numero = int(valor)
        if 0 < numero <= MAIOR_IDENTIFICADOR:
            return numero
    return None
