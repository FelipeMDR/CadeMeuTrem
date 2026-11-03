"""CT04 — Controlar empréstimos (RFS13 a RFS16), conforme a aba Testes da MRB."""

from datetime import timedelta

from conftest import br, hoje


def preparar(bd):
    """Duas pessoas ativas, uma inativa e três objetos: disponível, inativo e emprestado."""
    ferramentas = bd.criar_categoria("Ferramentas")
    ana = bd.criar_pessoa("Ana Souza")
    bd.criar_pessoa("Bruno Lima")
    bd.criar_pessoa("Carla Dias", ativo=0)
    furadeira = bd.criar_objeto(ferramentas, "FUR001", "Furadeira")
    bd.criar_objeto(ferramentas, "SER001", "Serrote", ativo=0)
    escada = bd.criar_objeto(ferramentas, "ESC001", "Escada")
    bd.registrar_emprestimo(ana, escada, hoje() - timedelta(days=3), hoje() + timedelta(days=4))
    return ana, furadeira


def incluir_emprestimo(tela, pessoa, objeto, retirada=None, previsao="", observacao=""):
    tela.abrir("emprestimos", acao="incluir")
    if pessoa:
        tela.escolher("pessoa", pessoa)
    if objeto:
        tela.escolher("objeto", objeto)
    if retirada is not None:
        tela.preencher("data-retirada", retirada)
    tela.preencher("previsao-devolucao", previsao)
    tela.preencher("observacao", observacao)
    tela.clicar("salvar")


def emprestimos_no_banco(bd):
    return bd.consultar("SELECT id, pessoa_id, objeto_id, data_retirada, previsao_devolucao, data_devolucao,"
                        " observacao FROM emprestimo ORDER BY id")


# ------------------------------------------------------------------ RFS13

def test_rfs13_incluir_emprestimo_valido(tela, bd):
    preparar(bd)
    retirada, previsao = hoje() - timedelta(days=1), hoje() + timedelta(days=6)
    incluir_emprestimo(tela, "Bruno Lima (2)", "FUR001 – Furadeira", br(retirada), br(previsao), "Com maleta")

    assert tela.mensagem() == "Empréstimo registrado com sucesso."
    linha = tela.linhas()[0]
    assert linha == {"id": 2, "pessoa": "Bruno Lima", "codigo": "FUR001", "objeto": "Furadeira",
                     "retirada": br(retirada), "previsao": br(previsao), "devolucao": "", "situacao": "Aberto"}
    assert emprestimos_no_banco(bd)[-1] == (2, 2, 1, retirada.isoformat(), previsao.isoformat(), None, "Com maleta")

    tela.abrir("objetos", codigo="FUR001")
    assert tela.linhas()[0]["disponibilidade"] == "Emprestado"


def test_rfs13_valores_iniciais_e_listas_somente_com_elegiveis(tela, bd):
    preparar(bd)
    tela.abrir("emprestimos", acao="incluir")

    assert tela.valor("data-retirada") == br(hoje())
    assert tela.valor("previsao-devolucao") == ""
    # Pessoa inativa, objeto inativo e objeto emprestado não aparecem.
    assert tela.opcoes("pessoa") == ["Selecione", "Ana Souza (1)", "Bruno Lima (2)"]
    assert tela.opcoes("objeto") == ["Selecione", "FUR001 – Furadeira"]


def test_rfs13_homonimos_distinguidos_pelo_identificador(tela, bd):
    preparar(bd)
    bd.criar_pessoa("Bruno Lima")
    incluir_emprestimo(tela, "Bruno Lima (4)", "FUR001 – Furadeira", previsao=br(hoje()))
    assert bd.consultar("SELECT pessoa_id FROM emprestimo WHERE objeto_id = 1") == [(4,)]


def test_rfs13_obrigatorios_preservam_dados_digitados(tela, bd):
    preparar(bd)
    incluir_emprestimo(tela, None, "FUR001 – Furadeira", "", "", "Levar à oficina")

    assert tela.erros() == ["Pessoa é obrigatória.", "Data da retirada é obrigatória.",
                            "Previsão de devolução é obrigatória."]
    assert tela.escolhido("objeto") == "FUR001 – Furadeira"
    assert tela.valor("observacao") == "Levar à oficina"
    assert len(emprestimos_no_banco(bd)) == 1


def test_rfs13_sem_pessoa_ou_objeto_elegivel_informa_o_motivo(tela, bd):
    bd.criar_pessoa("Carla Dias", ativo=0)
    tela.abrir("emprestimos", acao="incluir")

    motivo = tela.mensagem_erro()
    assert "Não há pessoas ativas" in motivo
    assert "Não há objetos ativos e disponíveis" in motivo
    assert not tela.existe("salvar")


# ------------------------------------------------------------------ RFS14

def test_rfs14_alterar_previsao_e_observacao(tela, bd):
    ana, _ = preparar(bd)
    tela.abrir("emprestimos")
    tela.clicar_acao(1, "alterar")

    for campo in ("identificador", "pessoa", "objeto", "data-retirada"):
        assert tela.elemento(campo).get_attribute("readonly") is not None, campo
    assert tela.valor("pessoa") == "Ana Souza (1)"
    assert tela.valor("objeto") == "ESC001 – Escada"
    nova_previsao = hoje() + timedelta(days=10)
    tela.preencher("previsao-devolucao", br(nova_previsao))
    tela.preencher("observacao", "Prazo estendido")
    tela.clicar("salvar")

    assert tela.mensagem() == "Empréstimo alterado com sucesso."
    assert bd.consultar("SELECT previsao_devolucao, observacao FROM emprestimo WHERE id = 1") == [
        (nova_previsao.isoformat(), "Prazo estendido")]


def test_rfs14_pessoa_objeto_e_retirada_nao_sao_alterados(tela, bd):
    preparar(bd)
    antes = emprestimos_no_banco(bd)
    tela.abrir("emprestimos", acao="alterar", id_=1)
    for campo, valor in (("pessoa", "Bruno Lima (2)"), ("objeto", "FUR001 – Furadeira"),
                         ("data-retirada", br(hoje()))):
        tela.destravar(campo)
        tela.preencher(campo, valor)
    tela.clicar("salvar")

    assert tela.mensagem() == "Empréstimo alterado com sucesso."
    assert emprestimos_no_banco(bd) == antes


def test_rfs14_devolvido_permite_alterar_somente_observacao(tela, bd):
    ana, furadeira = preparar(bd)
    retirada = hoje() - timedelta(days=8)
    bd.registrar_emprestimo(ana, furadeira, retirada, retirada + timedelta(days=2), devolucao=retirada)
    tela.abrir("emprestimos", acao="alterar", id_=2)

    assert tela.elemento("previsao-devolucao").get_attribute("readonly") is not None
    assert tela.valor("data-devolucao") == br(retirada)
    tela.destravar("previsao-devolucao")
    tela.preencher("previsao-devolucao", br(hoje()))
    tela.preencher("observacao", "Voltou sem a broca")
    tela.clicar("salvar")

    assert bd.consultar("SELECT previsao_devolucao, data_devolucao, observacao FROM emprestimo WHERE id = 2") == [
        ((retirada + timedelta(days=2)).isoformat(), retirada.isoformat(), "Voltou sem a broca")]


# ------------------------------------------------------------------ RFS15

def preparar_consulta(bd):
    categoria = bd.criar_categoria("Livros")
    ana = bd.criar_pessoa("Ana Souza")
    davi = bd.criar_pessoa("Davi Melo", ativo=0)
    livros = [bd.criar_objeto(categoria, f"LIV00{n}", f"Livro {n}") for n in range(1, 4)]
    base = hoje() - timedelta(days=20)
    bd.registrar_emprestimo(ana, livros[0], base, base + timedelta(days=5), devolucao=base + timedelta(days=4))
    bd.registrar_emprestimo(davi, livros[1], base + timedelta(days=10), base + timedelta(days=12))
    bd.registrar_emprestimo(ana, livros[2], base + timedelta(days=10), base + timedelta(days=15))
    bd.registrar_emprestimo(ana, livros[0], base + timedelta(days=6), base + timedelta(days=9))


def test_rfs15_ordem_por_retirada_e_identificador_decrescentes(tela, bd):
    preparar_consulta(bd)
    tela.abrir("emprestimos")
    assert [linha["id"] for linha in tela.linhas()] == [3, 2, 4, 1]
    assert tela.texto("total") == "Empréstimos exibidos: 4"


def test_rfs15_filtros_combinados_por_e(tela, bd):
    preparar_consulta(bd)
    tela.abrir("emprestimos")
    # O filtro de pessoa inclui inativas.
    assert "Davi Melo (2)" in tela.opcoes("filtro-pessoa")
    tela.escolher("filtro-pessoa", "Ana Souza (1)")
    tela.escolher("filtro-situacao", "Abertos")
    tela.clicar("pesquisar")
    assert [linha["id"] for linha in tela.linhas()] == [3, 4]

    tela.abrir("emprestimos", objeto="1", situacao="devolvidos")
    assert [(linha["id"], linha["situacao"]) for linha in tela.linhas()] == [(1, "Devolvido")]
    tela.abrir("emprestimos", pessoa="2", objeto="1")
    assert tela.texto("vazio") == "Nenhum empréstimo encontrado."


def test_rfs15_detalhe_inclui_observacao(tela, bd):
    ana, furadeira = preparar(bd)
    bd.executar("UPDATE emprestimo SET observacao = 'Escada de 7 degraus' WHERE id = 1")
    tela.abrir("emprestimos")
    tela.clicar_acao(1, "detalhar")
    assert tela.texto("detalhe-pessoa") == "Ana Souza"
    assert tela.texto("detalhe-codigo") == "ESC001"
    assert tela.texto("detalhe-situacao") == "Aberto"
    assert tela.texto("detalhe-observacao") == "Escada de 7 degraus"


# ------------------------------------------------------------------ RFS16

def test_rfs16_cancelar_exclusao_preserva_emprestimo(tela, bd):
    preparar(bd)
    tela.abrir("emprestimos")
    tela.clicar_acao(1, "excluir")

    assert tela.texto("confirmar-pessoa") == "Ana Souza"
    assert tela.texto("confirmar-codigo") == "ESC001"
    assert tela.texto("confirmar-retirada") == br(hoje() - timedelta(days=3))
    assert "sairá permanentemente do histórico" in tela.texto("confirmacao")
    tela.clicar("cancelar")
    assert len(emprestimos_no_banco(bd)) == 1


def test_rfs16_confirmar_exclusao_preserva_pessoa_e_objeto_e_libera_objeto(tela, bd):
    preparar(bd)
    tela.abrir("emprestimos")
    tela.clicar_acao(1, "excluir")
    tela.clicar("confirmar-exclusao")

    assert tela.mensagem() == "Empréstimo excluído com sucesso."
    assert tela.texto("vazio") == "Nenhum empréstimo encontrado."
    assert bd.consultar("SELECT COUNT(*) FROM pessoa") == [(3,)]
    assert bd.consultar("SELECT COUNT(*) FROM objeto") == [(3,)]
    tela.abrir("objetos", codigo="ESC001")
    assert tela.linhas()[0]["disponibilidade"] == "Disponível"


def test_rfs16_excluir_historico_antigo_nao_libera_objeto_com_emprestimo_aberto(tela, bd):
    ana, furadeira = preparar(bd)
    antigo = bd.registrar_emprestimo(ana, furadeira, hoje() - timedelta(days=9), hoje() - timedelta(days=7),
                                     devolucao=hoje() - timedelta(days=8))
    bd.registrar_emprestimo(ana, furadeira, hoje() - timedelta(days=1), hoje() + timedelta(days=2))
    tela.abrir("emprestimos")
    tela.clicar_acao(antigo, "excluir")
    tela.clicar("confirmar-exclusao")

    tela.abrir("objetos", codigo="FUR001")
    assert tela.linhas()[0]["disponibilidade"] == "Emprestado"
