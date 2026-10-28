"""Validações e normalizações comuns aos cadastros (RNF05)."""

import unicodedata


def texto_limpo(valor) -> str:
    """Remove espaços nas extremidades; ausente vira texto vazio."""
    return valor.strip() if isinstance(valor, str) else ""


def minusculas(valor: str) -> str:
    return valor.lower()


def chave_ordenacao(valor) -> str:
    """Chave para ordem alfabética: minúsculas e sem acentos (Álvaro antes de Bruno)."""
    texto = unicodedata.normalize("NFD", (valor or "").strip().lower())
    return "".join(c for c in texto if not unicodedata.combining(c))


def validar_texto(valor: str, rotulo: str, maximo: int, obrigatorio: bool) -> str | None:
    """Valida um texto já limpo. Devolve a mensagem de erro ou None.

    Texto somente com espaços chega aqui vazio e é tratado como não preenchido.
    """
    if valor == "":
        return f"{rotulo} é obrigatório." if obrigatorio else None
    if len(valor) > maximo:
        return f"{rotulo} deve ter no máximo {maximo} caracteres."
    return None


def valor_sim_nao(valor) -> int | None:
    """Escolha fechada Sim ou Não; devolve 1, 0 ou None se o valor for inválido."""
    return {"1": 1, "0": 0}.get(valor) if isinstance(valor, str) else None


def escapar_like(valor: str) -> str:
    """Escapa curingas para uso seguro em LIKE ... ESCAPE '\\'."""
    return valor.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
