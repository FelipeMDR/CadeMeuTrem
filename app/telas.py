"""Auxiliares comuns das telas (RNF01)."""

from flask import render_template


def sim_nao(valor) -> str:
    return "Sim" if int(valor) == 1 else "Não"


def pagina_nao_encontrada(texto: str, voltar_para: str, rotulo_voltar: str):
    return render_template("nao_encontrado.html", titulo="Registro não encontrado", mensagem_erro=texto,
                           voltar_para=voltar_para, rotulo_voltar=rotulo_voltar), 404
