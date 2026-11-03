"""Datas dos empréstimos (RFS13, RFS14 e RFS17): formato DD/MM/AAAA, sem horário."""

import re
from datetime import date, datetime
from zoneinfo import ZoneInfo

FUSO = ZoneInfo("America/Sao_Paulo")
FORMATO = re.compile(r"([0-9]{2})/([0-9]{2})/([0-9]{4})")


def hoje() -> date:
    """Dia atual no fuso America/Sao_Paulo."""
    return datetime.now(FUSO).date()


def formatar(valor) -> str:
    """date ou texto AAAA-MM-DD do banco -> DD/MM/AAAA; vazio continua vazio."""
    if not valor:
        return ""
    if isinstance(valor, str):
        valor = date.fromisoformat(valor)
    return valor.strftime("%d/%m/%Y")


def ler(valor: str, rotulo: str) -> tuple[date | None, str | None]:
    """Valida uma data obrigatória já limpa. Devolve (data, None) ou (None, mensagem de erro).

    O calendário do Python aplica as regras do DRE: meses de 30 e 31 dias,
    fevereiro com 28 dias e 29 nos anos bissextos, ano com quatro dígitos.
    """
    if valor == "":
        return None, f"{rotulo} é obrigatória."
    combinacao = FORMATO.fullmatch(valor)
    if not combinacao:
        return None, f"{rotulo} deve estar no formato DD/MM/AAAA."
    dia, mes, ano = (int(parte) for parte in combinacao.groups())
    try:
        return date(ano, mes, dia), None
    except ValueError:
        return None, f"{rotulo} não é uma data válida."
