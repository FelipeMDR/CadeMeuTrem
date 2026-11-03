"""CT06 — Datas de retirada, previsão e devolução (RFS13, RFS14 e RFS17), conforme a aba Testes da MRB."""

from datetime import date, timedelta

import pytest

from conftest import br, hoje


@pytest.fixture
def cadastro(bd):
    categoria = bd.criar_categoria("Livros")
    return bd.criar_pessoa("Ana Souza"), bd.criar_objeto(categoria, "LIV001", "Dom Casmurro")


def incluir(tela, retirada, previsao):
    tela.abrir("emprestimos", acao="incluir")
    tela.escolher("pessoa", "Ana Souza (1)")
    tela.escolher("objeto", "LIV001 – Dom Casmurro")
    tela.preencher("data-retirada", retirada)
    tela.preencher("previsao-devolucao", previsao)
    tela.preencher("observacao", "Capa azul")
    tela.clicar("salvar")


# ------------------------------------------------------------------ RFS13

@pytest.mark.parametrize("retirada, erro", [
    ("31/04/2024", "Data da retirada não é uma data válida."),
    ("29/02/2025", "Data da retirada não é uma data válida."),
    ("00/01/2024", "Data da retirada não é uma data válida."),
    ("15/13/2024", "Data da retirada não é uma data válida."),
    ("1/2/2024", "Data da retirada deve estar no formato DD/MM/AAAA."),
    ("2024-02-01", "Data da retirada deve estar no formato DD/MM/AAAA."),
])
def test_rfs13_retirada_invalida_e_recusada_e_dados_permanecem(tela, bd, cadastro, retirada, erro):
    incluir(tela, retirada, "30/06/2026")

    assert tela.erros() == [erro]
    assert tela.valor("data-retirada") == retirada
    assert tela.valor("previsao-devolucao") == "30/06/2026"
    assert tela.escolhido("pessoa") == "Ana Souza (1)"
    assert tela.valor("observacao") == "Capa azul"
    assert bd.consultar("SELECT COUNT(*) FROM emprestimo") == [(0,)]


def test_rfs13_29_de_fevereiro_em_ano_bissexto_e_aceito(tela, bd, cadastro):
    incluir(tela, "29/02/2024", "01/03/2024")
    assert tela.mensagem() == "Empréstimo registrado com sucesso."
    assert bd.consultar("SELECT data_retirada FROM emprestimo") == [("2024-02-29",)]


def test_rfs13_retirada_futura_e_recusada(tela, bd, cadastro):
    amanha = hoje() + timedelta(days=1)
    incluir(tela, br(amanha), br(amanha + timedelta(days=5)))
    assert tela.erros() == ["Data da retirada não pode ser posterior ao dia atual."]


def test_rfs13_previsao_anterior_a_retirada_e_recusada(tela, bd, cadastro):
    incluir(tela, "10/10/2026", "09/10/2026")
    assert tela.erros() == ["Previsão de devolução deve ser igual ou posterior à data da retirada."]


def test_rfs13_limites_iguais_sao_aceitos(tela, bd, cadastro):
    incluir(tela, br(hoje()), br(hoje()))
    assert tela.mensagem() == "Empréstimo registrado com sucesso."
    assert bd.consultar("SELECT data_retirada, previsao_devolucao FROM emprestimo") == [
        (hoje().isoformat(), hoje().isoformat())]


# ------------------------------------------------------------------ RFS14

def test_rfs14_previsao_valida_com_os_mesmos_limites(tela, bd, cadastro):
    pessoa, objeto = cadastro
    retirada = date(2026, 10, 10)
    bd.registrar_emprestimo(pessoa, objeto, retirada, date(2026, 10, 20))
    tela.abrir("emprestimos", acao="alterar", id_=1)

    tela.preencher("previsao-devolucao", "09/10/2026")
    tela.clicar("salvar")
    assert tela.erros() == ["Previsão de devolução deve ser igual ou posterior à data da retirada."]
    assert tela.valor("previsao-devolucao") == "09/10/2026"

    tela.preencher("previsao-devolucao", "31/11/2026")
    tela.clicar("salvar")
    assert tela.erros() == ["Previsão de devolução não é uma data válida."]

    tela.preencher("previsao-devolucao", "10/10/2026")
    tela.clicar("salvar")
    assert tela.mensagem() == "Empréstimo alterado com sucesso."
    assert bd.consultar("SELECT previsao_devolucao FROM emprestimo") == [("2026-10-10",)]


# ------------------------------------------------------------------ RFS17

@pytest.mark.parametrize("deslocamento, aceita", [(-1, False), (0, True), (1, True), (4, True), (5, False)])
def test_rfs17_devolucao_entre_retirada_e_hoje_inclusive(tela, bd, cadastro, deslocamento, aceita):
    """Retirada há 4 dias: a devolução vai da retirada (0) até hoje (4)."""
    pessoa, objeto = cadastro
    retirada = hoje() - timedelta(days=4)
    bd.registrar_emprestimo(pessoa, objeto, retirada, hoje())
    devolucao = retirada + timedelta(days=deslocamento)
    tela.abrir("emprestimos", acao="devolver", id_=1)
    tela.preencher("data-devolucao", br(devolucao))
    tela.clicar("confirmar-devolucao")

    if aceita:
        assert tela.mensagem() == "Devolução registrada com sucesso."
        assert bd.consultar("SELECT data_devolucao FROM emprestimo") == [(devolucao.isoformat(),)]
    else:
        assert tela.erros() == [f"Data da devolução deve estar entre a data da retirada ({br(retirada)}) "
                                f"e o dia atual ({br(hoje())})."]
        assert tela.valor("data-devolucao") == br(devolucao)
        assert bd.consultar("SELECT data_devolucao FROM emprestimo") == [(None,)]


def test_rfs17_data_de_devolucao_invalida(tela, bd, cadastro):
    pessoa, objeto = cadastro
    bd.registrar_emprestimo(pessoa, objeto, date(2024, 2, 1), date(2024, 2, 5))
    tela.abrir("emprestimos", acao="devolver", id_=1)
    tela.preencher("data-devolucao", "30/02/2024")
    tela.clicar("confirmar-devolucao")
    assert tela.erros() == ["Data da devolução não é uma data válida."]
