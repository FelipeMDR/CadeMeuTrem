"""CT05 — Regras de empréstimo e devolução (RFS13 a RFS17 e RNF02), conforme a aba Testes da MRB."""

import sqlite3
from datetime import timedelta

import pytest

from conftest import br, hoje


def preparar(bd):
    categoria = bd.criar_categoria("Ferramentas")
    ana = bd.criar_pessoa("Ana Souza")
    furadeira = bd.criar_objeto(categoria, "FUR001", "Furadeira")
    return ana, furadeira


def tentar_incluir(tela, pessoa_id, objeto_id):
    """Envia a inclusão com valores forjados, como se a lista ainda oferecesse a opção."""
    tela.abrir("emprestimos", acao="incluir")
    tela.forjar_opcao("pessoa", str(pessoa_id))
    tela.forjar_opcao("objeto", str(objeto_id))
    tela.preencher("previsao-devolucao", br(hoje() + timedelta(days=3)))
    tela.clicar("salvar")


def devolver(tela, emprestimo_id, data=None):
    tela.abrir("emprestimos")
    tela.clicar_acao(emprestimo_id, "devolver")
    if data is not None:
        tela.preencher("data-devolucao", data)
    tela.clicar("confirmar-devolucao")


# ------------------------------------------------------------------ RFS13

def test_rfs13_segunda_retirada_aberta_do_mesmo_objeto_e_bloqueada(tela, bd):
    ana, furadeira = preparar(bd)
    bruno = bd.criar_pessoa("Bruno Lima")
    tela.abrir("emprestimos", acao="incluir")
    tela.escolher("pessoa", "Ana Souza (1)")
    tela.escolher("objeto", "FUR001 – Furadeira")
    tela.preencher("previsao-devolucao", br(hoje()))
    # Outro operador empresta o mesmo objeto antes da gravação.
    bd.registrar_emprestimo(bruno, furadeira, hoje(), hoje())
    tela.clicar("salvar")

    assert tela.erros() == ['O objeto "FUR001" já está emprestado.']
    assert bd.consultar("SELECT COUNT(*) FROM emprestimo") == [(1,)]


def test_rfs13_pessoa_inativa_e_bloqueada_na_gravacao(tela, bd):
    _, furadeira = preparar(bd)
    inativa = bd.criar_pessoa("Carla Dias", ativo=0)
    tentar_incluir(tela, inativa, furadeira)

    assert tela.erros() == ['A pessoa "Carla Dias" está inativa e não pode retirar objetos.']
    assert bd.consultar("SELECT COUNT(*) FROM emprestimo") == [(0,)]


def test_rfs13_objeto_inativo_e_bloqueado_na_gravacao(tela, bd):
    ana, furadeira = preparar(bd)
    bd.criar_objeto(1, "SER001", "Serrote")  # mantém o formulário disponível
    bd.executar("UPDATE objeto SET ativo = 0 WHERE id = ?", (furadeira,))
    tentar_incluir(tela, ana, furadeira)

    assert tela.erros() == ['O objeto "FUR001" está inativo e não pode ser emprestado.']
    assert bd.consultar("SELECT COUNT(*) FROM emprestimo") == [(0,)]


def test_rnf02_banco_impede_dois_emprestimos_abertos_do_mesmo_objeto(bd):
    ana, furadeira = preparar(bd)
    bd.registrar_emprestimo(ana, furadeira, hoje(), hoje())
    with pytest.raises(sqlite3.IntegrityError):
        bd.registrar_emprestimo(ana, furadeira, hoje(), hoje())


# ------------------------------------------------------------------ RFS17

def test_rfs17_devolver_objeto_ativo_permite_nova_retirada(tela, bd):
    ana, furadeira = preparar(bd)
    emprestimo = bd.registrar_emprestimo(ana, furadeira, hoje() - timedelta(days=2), hoje() + timedelta(days=2))
    tela.abrir("emprestimos")
    tela.clicar_acao(emprestimo, "devolver")

    assert tela.texto("devolver-objeto") == "FUR001 – Furadeira"
    assert tela.valor("data-devolucao") == br(hoje())
    tela.clicar("confirmar-devolucao")

    assert tela.mensagem() == "Devolução registrada com sucesso."
    assert tela.linhas()[0]["situacao"] == "Devolvido"
    assert tela.linhas()[0]["devolucao"] == br(hoje())
    tela.abrir("emprestimos", acao="incluir")
    assert tela.opcoes("objeto") == ["Selecione", "FUR001 – Furadeira"]


def test_rfs17_objeto_inativo_devolvido_continua_inelegivel(tela, bd):
    ana, furadeira = preparar(bd)
    emprestimo = bd.registrar_emprestimo(ana, furadeira, hoje() - timedelta(days=2), hoje())
    bd.executar("UPDATE objeto SET ativo = 0 WHERE id = ?", (furadeira,))
    devolver(tela, emprestimo)

    tela.abrir("objetos")
    assert tela.linhas()[0]["disponibilidade"] == "Inativo"
    tela.abrir("emprestimos", acao="incluir")
    assert "Não há objetos ativos e disponíveis" in tela.mensagem_erro()


def test_rfs17_cancelar_devolucao_preserva_emprestimo_aberto(tela, bd):
    ana, furadeira = preparar(bd)
    emprestimo = bd.registrar_emprestimo(ana, furadeira, hoje() - timedelta(days=2), hoje())
    tela.abrir("emprestimos")
    tela.clicar_acao(emprestimo, "devolver")
    tela.clicar("cancelar")

    assert tela.linhas()[0]["situacao"] == "Aberto"
    assert bd.consultar("SELECT data_devolucao FROM emprestimo") == [(None,)]


def test_rfs17_nao_devolve_novamente_nem_reabre(tela, bd):
    ana, furadeira = preparar(bd)
    retirada = hoje() - timedelta(days=5)
    emprestimo = bd.registrar_emprestimo(ana, furadeira, retirada, retirada, devolucao=retirada)

    tela.abrir("emprestimos")
    assert not tela.driver.find_elements("css selector", f'#lista tr[data-id="{emprestimo}"] a.acao-devolver')
    tela.abrir("emprestimos", acao="devolver", id_=emprestimo)
    assert tela.mensagem_erro() == (f"Este empréstimo já foi devolvido em {br(retirada)}. "
                                    "A devolução não pode ser registrada novamente nem desfeita.")
    assert not tela.existe("confirmar-devolucao")

    # A alteração não oferece a data da devolução para edição.
    tela.abrir("emprestimos", acao="alterar", id_=emprestimo)
    tela.destravar("data-devolucao")
    tela.preencher("data-devolucao", "")
    tela.clicar("salvar")
    assert bd.consultar("SELECT data_devolucao FROM emprestimo") == [(retirada.isoformat(),)]


def test_rfs17_devolucao_revalidada_na_confirmacao(tela, bd):
    ana, furadeira = preparar(bd)
    emprestimo = bd.registrar_emprestimo(ana, furadeira, hoje() - timedelta(days=2), hoje())
    tela.abrir("emprestimos")
    tela.clicar_acao(emprestimo, "devolver")
    # Outro operador registra a devolução antes da confirmação.
    bd.executar("UPDATE emprestimo SET data_devolucao = ? WHERE id = ?",
                ((hoje() - timedelta(days=1)).isoformat(), emprestimo))
    tela.clicar("confirmar-devolucao")

    assert "já foi devolvido" in tela.mensagem_erro()
    assert bd.consultar("SELECT data_devolucao FROM emprestimo") == [((hoje() - timedelta(days=1)).isoformat(),)]
