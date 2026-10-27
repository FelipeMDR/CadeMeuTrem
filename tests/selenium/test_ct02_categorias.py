"""CT02 — Manter categorias (RFS05 a RFS08), conforme a aba Testes da MRB."""


def incluir_categoria(tela, nome, ignorar_limite=False):
    tela.abrir("categorias", acao="incluir")
    tela.preencher("nome", nome, ignorar_limite)
    tela.clicar("salvar")


def alterar_categoria(tela, id_categoria, nome):
    tela.abrir("categorias")
    tela.clicar_acao(id_categoria, "alterar")
    tela.preencher("nome", nome)
    tela.clicar("salvar")


# ------------------------------------------------------------------ RFS05

def test_rfs05_incluir_categoria_valida(tela, bd):
    incluir_categoria(tela, "Ferramentas")

    assert tela.mensagem() == "Categoria cadastrada com sucesso."
    assert tela.linhas() == [{"id": 1, "nome": "Ferramentas"}]
    assert bd.consultar("SELECT nome FROM categoria") == [("Ferramentas",)]


def test_rfs05_duplicidade_desconsidera_maiusculas_e_espacos(tela, bd):
    incluir_categoria(tela, "Ferramentas")
    for variacao in [" ferramentas ", "FERRAMENTAS", "fErRaMeNtAs"]:
        incluir_categoria(tela, variacao)
        assert tela.erros() == ["Já existe uma categoria com este nome."]
        assert tela.valor("nome") == variacao.strip()
    assert bd.consultar("SELECT COUNT(*) FROM categoria") == [(1,)]


def test_rfs05_duplicidade_com_acentos_e_maiusculas(tela, bd):
    incluir_categoria(tela, "Eletrônicos")
    incluir_categoria(tela, "ELETRÔNICOS")
    assert tela.erros() == ["Já existe uma categoria com este nome."]


def test_rfs05_nome_obrigatorio(tela, bd):
    for vazio in ["", "     "]:
        incluir_categoria(tela, vazio)
        assert tela.erros() == ["Nome é obrigatório."]
    assert bd.consultar("SELECT COUNT(*) FROM categoria") == [(0,)]


def test_rfs05_limite_de_40_caracteres(tela, bd):
    incluir_categoria(tela, "C" * 40)
    assert tela.mensagem() == "Categoria cadastrada com sucesso."

    tela.abrir("categorias", acao="incluir")
    tela.preencher("nome", "D" * 45)
    assert len(tela.valor("nome")) == 40

    incluir_categoria(tela, "D" * 41, ignorar_limite=True)
    assert tela.erros() == ["Nome deve ter no máximo 40 caracteres."]
    assert bd.consultar("SELECT COUNT(*) FROM categoria") == [(1,)]


# ------------------------------------------------------------------ RFS06

def test_rfs06_alterar_categoria_mantem_identificador(tela, bd):
    incluir_categoria(tela, "Livro")
    tela.clicar_acao(1, "alterar")
    assert tela.valor("identificador") == "1"
    assert tela.elemento("identificador").get_attribute("readonly") is not None
    tela.preencher("nome", "Livros")
    tela.clicar("salvar")

    assert tela.mensagem() == "Categoria alterada com sucesso."
    assert tela.linhas() == [{"id": 1, "nome": "Livros"}]


def test_rfs06_duplicidade_desconsidera_o_proprio_registro(tela, bd):
    incluir_categoria(tela, "Livros")
    incluir_categoria(tela, "Cozinha")

    alterar_categoria(tela, 1, "LIVROS")
    assert tela.mensagem() == "Categoria alterada com sucesso."

    alterar_categoria(tela, 1, " cozinha ")
    assert tela.erros() == ["Já existe uma categoria com este nome."]
    assert bd.consultar("SELECT nome FROM categoria ORDER BY id") == [("LIVROS",), ("Cozinha",)]


def test_rfs06_alteracao_aplica_as_mesmas_validacoes(tela, bd):
    incluir_categoria(tela, "Jardim")
    alterar_categoria(tela, 1, "   ")
    assert tela.erros() == ["Nome é obrigatório."]
    assert bd.consultar("SELECT nome FROM categoria") == [("Jardim",)]


def test_rfs06_renomear_mantem_vinculo_com_objetos(tela, bd):
    categoria_id = bd.executar("INSERT INTO categoria (nome, nome_chave) VALUES ('Ferramenta', 'ferramenta')")
    bd.criar_objeto(categoria_id, "FUR001")
    alterar_categoria(tela, categoria_id, "Ferramentas")

    assert tela.mensagem() == "Categoria alterada com sucesso."
    assert bd.consultar(
        "SELECT c.id, c.nome FROM objeto o JOIN categoria c ON c.id = o.categoria_id WHERE o.codigo = 'FUR001'"
    ) == [(categoria_id, "Ferramentas")]


# ------------------------------------------------------------------ RFS07

def preparar_consulta(bd):
    for nome in ["Ferramentas", "cozinha", "Eletrônicos", "Áudio", "Livros"]:
        bd.executar("INSERT INTO categoria (nome, nome_chave) VALUES (?, lower(?))", (nome, nome))


def test_rfs07_lista_em_ordem_alfabetica(tela, bd):
    preparar_consulta(bd)
    tela.abrir("categorias")
    assert tela.nomes() == ["Áudio", "cozinha", "Eletrônicos", "Ferramentas", "Livros"]
    assert tela.texto("total") == "Categorias exibidas: 5"


def test_rfs07_filtro_por_trecho_sem_diferenciar_maiusculas(tela, bd):
    preparar_consulta(bd)
    tela.abrir("categorias")
    tela.preencher("filtro-nome", "OS")
    tela.clicar("pesquisar")
    assert tela.nomes() == ["Eletrônicos", "Livros"]


def test_rfs07_sem_resultados(tela, bd):
    preparar_consulta(bd)
    tela.abrir("categorias", nome="Brinquedos")
    assert tela.texto("vazio") == "Nenhuma categoria encontrada."


# ------------------------------------------------------------------ RFS08

def test_rfs08_cancelar_exclusao_preserva_categoria(tela, bd):
    bd.executar("INSERT INTO categoria (nome, nome_chave) VALUES ('Jogos', 'jogos')")
    tela.abrir("categorias")
    tela.clicar_acao(1, "excluir")

    assert tela.texto("confirmar-id") == "1"
    assert tela.texto("confirmar-nome") == "Jogos"
    tela.clicar("cancelar")
    assert tela.nomes() == ["Jogos"]


def test_rfs08_confirmar_exclusao_remove_somente_a_categoria(tela, bd):
    bd.executar("INSERT INTO categoria (nome, nome_chave) VALUES ('Jogos', 'jogos')")
    bd.executar("INSERT INTO categoria (nome, nome_chave) VALUES ('Música', 'música')")
    tela.abrir("categorias")
    tela.clicar_acao(1, "excluir")
    tela.clicar("confirmar-exclusao")

    assert tela.mensagem() == "Categoria excluída com sucesso."
    assert tela.nomes() == ["Música"]


def test_rfs08_exclusao_bloqueada_quando_ha_objeto(tela, bd):
    categoria_id = bd.executar("INSERT INTO categoria (nome, nome_chave) VALUES ('Esporte', 'esporte')")
    bd.criar_objeto(categoria_id, "BOL001")
    tela.abrir("categorias")
    tela.clicar_acao(categoria_id, "excluir")

    assert "possui objetos vinculados e não pode ser excluída" in tela.mensagem_erro()
    assert not tela.existe("confirmar-exclusao")
    assert bd.consultar("SELECT COUNT(*) FROM categoria") == [(1,)]
    assert bd.consultar("SELECT COUNT(*) FROM objeto") == [(1,)]
