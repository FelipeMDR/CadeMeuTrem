"""CT08 — Consultar histórico (RFS19), conforme a aba Testes da MRB.

Usa o cenário do CT07, com datas relativas ao dia da execução (hoje = H):
1 Dom Casmurro/Ana, retirada H-9, aberto; 2 Furadeira/Bruno, retirada H-5, aberto;
3 Controle remoto/Carla, retirada H-7, devolvido; 4 Escada/Diego (inativo), retirada H-3, aberto.
"""

from datetime import timedelta

import pytest

from conftest import br, hoje


@pytest.fixture
def cenario(bd):
    h = hoje()
    livros, ferramentas, eletronicos = (bd.criar_categoria(n) for n in ("Livros", "Ferramentas", "Eletrônicos"))
    ana, bruno, carla = (bd.criar_pessoa(nome) for nome in ("Ana Souza", "Bruno Lima", "Carla Dias"))
    diego = bd.criar_pessoa("Diego Rocha", ativo=0)
    livro = bd.criar_objeto(livros, "Dom Casmurro")
    furadeira = bd.criar_objeto(ferramentas, "Furadeira")
    controle = bd.criar_objeto(eletronicos, "Controle remoto")
    escada = bd.criar_objeto(ferramentas, "Escada")
    bd.registrar_emprestimo(ana, livro, h - timedelta(days=9), h - timedelta(days=2))
    bd.registrar_emprestimo(bruno, furadeira, h - timedelta(days=5), h + timedelta(days=2))
    bd.registrar_emprestimo(carla, controle, h - timedelta(days=7), h - timedelta(days=2), devolucao=h - timedelta(days=1))
    bd.registrar_emprestimo(diego, escada, h - timedelta(days=3), h)
    return h


def consultar(tela, inicio, fim, **filtros):
    tela.abrir("relatorios/historico", inicio=inicio, fim=fim, **filtros)


def ids(tela):
    return [linha["id"] for linha in tela.linhas()]


def totais(tela):
    return tela.texto("total"), tela.texto("total-abertos"), tela.texto("total-devolvidos")


def test_rfs19_periodo_lista_abertos_e_devolvidos_com_totais(tela, cenario):
    consultar(tela, br(cenario - timedelta(days=9)), br(cenario))

    assert ids(tela) == [4, 2, 3, 1]
    assert totais(tela) == ("Empréstimos exibidos: 4", "Abertos: 3", "Devolvidos: 1")
    assert tela.linhas()[2] == {
        "id": 3, "pessoa": "Carla Dias", "objeto": "Controle remoto (3)", "retirada": br(cenario - timedelta(days=7)),
        "previsao": br(cenario - timedelta(days=2)), "devolucao": br(cenario - timedelta(days=1)), "situacao": "Devolvido",
    }


def test_rfs19_somente_devolvidos(tela, cenario):
    tela.abrir("relatorios/historico", inicio=br(cenario - timedelta(days=30)))
    tela.escolher("filtro-situacao", "Devolvidos")
    tela.clicar("pesquisar")

    assert [linha["objeto"] for linha in tela.linhas()] == ["Controle remoto (3)"]
    assert totais(tela) == ("Empréstimos exibidos: 1", "Abertos: 0", "Devolvidos: 1")


def test_rfs19_limites_do_periodo_sao_inclusivos(tela, cenario):
    consultar(tela, br(cenario - timedelta(days=5)), br(cenario - timedelta(days=5)))
    assert ids(tela) == [2]
    consultar(tela, br(cenario - timedelta(days=7)), br(cenario - timedelta(days=5)))
    assert ids(tela) == [2, 3]


def test_rfs19_periodo_invertido_impede_a_consulta(tela, cenario):
    tela.abrir("relatorios/historico")
    tela.preencher("filtro-inicio", br(cenario))
    tela.preencher("filtro-fim", br(cenario - timedelta(days=1)))
    tela.clicar("pesquisar")

    assert tela.erros() == ["Retirada final deve ser igual ou posterior à retirada inicial."]
    assert not tela.existe("lista") and not tela.existe("total")
    assert tela.valor("filtro-inicio") == br(cenario)


@pytest.mark.parametrize("inicio, fim, erros", [
    ("31/04/2026", "30/06/2026", ["Retirada inicial não é uma data válida."]),
    ("01/02/2026", "29/02/2026", ["Retirada final não é uma data válida."]),
    ("2026-01-01", "", ["Retirada inicial deve estar no formato DD/MM/AAAA.", "Retirada final é obrigatória."]),
])
def test_rfs19_datas_invalidas_geram_mensagem_de_correcao(tela, cenario, inicio, fim, erros):
    consultar(tela, inicio, fim)
    assert tela.erros() == erros
    assert not tela.existe("lista")
    assert tela.valor("filtro-inicio") == inicio and tela.valor("filtro-fim") == fim


def test_rfs19_padrao_e_o_mes_atual_ate_hoje(tela, cenario):
    tela.abrir("relatorios/historico")
    primeiro_dia = cenario.replace(day=1)

    assert tela.valor("filtro-inicio") == br(primeiro_dia)
    assert tela.valor("filtro-fim") == br(cenario)
    retiradas = {4: 3, 2: 5, 3: 7, 1: 9}  # identificador: dias antes de hoje
    esperados = [i for i, dias in retiradas.items() if cenario - timedelta(days=dias) >= primeiro_dia]
    assert ids(tela) == esperados


def test_rfs19_filtros_combinados_e_resultado_vazio(tela, cenario):
    inicio = br(cenario - timedelta(days=30))
    tela.abrir("relatorios/historico", inicio=inicio)
    assert "Diego Rocha (4)" in tela.opcoes("filtro-pessoa")
    tela.escolher("filtro-pessoa", "Ana Souza (1)")
    tela.escolher("filtro-objeto", "Dom Casmurro (1)")
    tela.clicar("pesquisar")
    assert ids(tela) == [1]

    consultar(tela, inicio, br(cenario), pessoa="2", objeto="1")
    assert tela.texto("vazio") == "Nenhum empréstimo encontrado no período."
    assert totais(tela) == ("Empréstimos exibidos: 0", "Abertos: 0", "Devolvidos: 0")


def test_rfs19_desempate_por_identificador_decrescente(tela, bd):
    categoria = bd.criar_categoria("Livros")
    pessoa = bd.criar_pessoa("Ana Souza")
    retirada = hoje() - timedelta(days=2)
    for n in range(3):
        bd.registrar_emprestimo(pessoa, bd.criar_objeto(categoria, f"Livro {n + 1}"), retirada, hoje())
    consultar(tela, br(retirada), br(hoje()))
    assert ids(tela) == [3, 2, 1]


def test_rfs19_usa_cadastros_atuais_e_ignora_excluidos(tela, bd, cenario):
    bd.executar("UPDATE pessoa SET nome = 'Ana Souza Lima' WHERE id = 1")
    bd.executar("UPDATE objeto SET nome = 'Dom Casmurro, edição de bolso' WHERE id = 1")
    bd.executar("DELETE FROM emprestimo WHERE id = 2")
    consultar(tela, br(cenario - timedelta(days=9)), br(cenario))

    assert ids(tela) == [4, 3, 1]
    assert (tela.linhas()[-1]["pessoa"], tela.linhas()[-1]["objeto"]) == (
        "Ana Souza Lima", "Dom Casmurro, edição de bolso (1)")
