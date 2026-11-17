"""CT07 — Consultar pendências (RFS18), conforme a aba Testes da MRB.

As datas são relativas ao dia da execução (hoje = H), o que equivale a fixar o dia atual:
- Dom Casmurro, Ana: retirada H-9, previsão H-2, aberto (atrasado 2 dias);
- Furadeira, Bruno: retirada H-5, previsão H+2, aberto (no prazo);
- Controle remoto, Carla: retirada H-7, previsão H-2, devolvido em H-1 (não aparece);
- Escada, Diego (pessoa inativa): retirada H-3, previsão H, aberto (vence hoje: no prazo).
"""

from datetime import timedelta

import pytest

from conftest import br, hoje


@pytest.fixture
def cenario(bd):
    h = hoje()
    livros = bd.criar_categoria("Livros")
    ferramentas = bd.criar_categoria("Ferramentas")
    eletronicos = bd.criar_categoria("Eletrônicos")
    bd.criar_categoria("Cozinha")
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


def resumo(tela):
    return [(linha["id"], linha["objeto"], linha["situacao"], linha["dias"]) for linha in tela.linhas()]


def test_rfs18_sem_filtros_lista_abertos_com_atrasados_primeiro(tela, cenario):
    tela.abrir("relatorios/pendencias")

    assert resumo(tela) == [
        (1, "Dom Casmurro (1)", "Atrasado", "2"),
        (4, "Escada (4)", "No prazo", "0"),
        (2, "Furadeira (2)", "No prazo", "0"),
    ]
    assert tela.texto("total") == "Empréstimos exibidos: 3"
    assert tela.texto("total-atrasados") == "Atrasados: 1"


def test_rfs18_campos_da_listagem(tela, cenario):
    tela.abrir("relatorios/pendencias")
    assert tela.linhas()[0] == {
        "id": 1, "objeto": "Dom Casmurro (1)", "categoria": "Livros", "pessoa": "Ana Souza",
        "retirada": br(cenario - timedelta(days=9)), "previsao": br(cenario - timedelta(days=2)),
        "situacao": "Atrasado", "dias": "2",
    }


def test_rfs18_vencer_hoje_nao_e_atraso(tela, cenario):
    tela.abrir("relatorios/pendencias")
    escada = next(linha for linha in tela.linhas() if linha["id"] == 4)
    assert (escada["previsao"], escada["situacao"], escada["dias"]) == (br(cenario), "No prazo", "0")


def test_rfs18_somente_atrasados(tela, cenario):
    tela.abrir("relatorios/pendencias")
    tela.escolher("filtro-atrasados", "Sim")
    tela.clicar("pesquisar")

    assert resumo(tela) == [(1, "Dom Casmurro (1)", "Atrasado", "2")]
    assert tela.texto("total") == "Empréstimos exibidos: 1"
    assert tela.texto("total-atrasados") == "Atrasados: 1"


def test_rfs18_filtro_de_pessoa_inclui_inativas(tela, cenario):
    tela.abrir("relatorios/pendencias")
    assert "Diego Rocha (4)" in tela.opcoes("filtro-pessoa")
    tela.escolher("filtro-pessoa", "Diego Rocha (4)")
    tela.clicar("pesquisar")
    assert [(linha["pessoa"], linha["objeto"]) for linha in tela.linhas()] == [("Diego Rocha", "Escada (4)")]


def test_rfs18_filtro_de_categoria_usa_a_categoria_atual(tela, bd, cenario):
    tela.abrir("relatorios/pendencias", categoria="2")
    assert [linha["objeto"] for linha in tela.linhas()] == ["Escada (4)", "Furadeira (2)"]

    bd.executar("UPDATE objeto SET categoria_id = 1 WHERE id = 2")
    tela.abrir("relatorios/pendencias", categoria="2")
    assert [linha["objeto"] for linha in tela.linhas()] == ["Escada (4)"]
    tela.abrir("relatorios/pendencias", categoria="1", atrasados="0")
    assert [(linha["objeto"], linha["categoria"]) for linha in tela.linhas()] == [
        ("Dom Casmurro (1)", "Livros"), ("Furadeira (2)", "Livros")]


def test_rfs18_objeto_inativo_com_emprestimo_aberto_continua_listado(tela, bd, cenario):
    bd.executar("UPDATE objeto SET ativo = 0 WHERE id = 2")
    tela.abrir("relatorios/pendencias")
    assert "Furadeira (2)" in [linha["objeto"] for linha in tela.linhas()]


def test_rfs18_resultado_vazio_com_totais_zerados(tela, cenario):
    tela.abrir("relatorios/pendencias")
    tela.escolher("filtro-categoria", "Cozinha (4)")
    tela.clicar("pesquisar")

    assert tela.texto("vazio") == "Nenhuma pendência encontrada."
    assert tela.linhas() == []
    assert tela.texto("total") == "Empréstimos exibidos: 0"
    assert tela.texto("total-atrasados") == "Atrasados: 0"


def test_rfs18_desempate_por_previsao_e_identificador(tela, bd):
    h = hoje()
    categoria = bd.criar_categoria("Livros")
    pessoa = bd.criar_pessoa("Ana Souza")
    for dias in (3, 5, 3):
        objeto = bd.criar_objeto(categoria, f"Livro atrasado {dias}")
        bd.registrar_emprestimo(pessoa, objeto, h - timedelta(days=10), h - timedelta(days=dias))
    objeto = bd.criar_objeto(categoria, "Livro no prazo")
    bd.registrar_emprestimo(pessoa, objeto, h - timedelta(days=1), h + timedelta(days=1))
    tela.abrir("relatorios/pendencias")

    # Atrasados primeiro; dentro de cada situação, previsão crescente e identificador crescente.
    assert [(linha["id"], linha["dias"]) for linha in tela.linhas()] == [(2, "5"), (1, "3"), (3, "3"), (4, "0")]
