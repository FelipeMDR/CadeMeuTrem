"""CT03 — Manter objetos (RFS09 a RFS12), conforme a aba Testes da MRB."""

from datetime import timedelta

from conftest import hoje


def incluir_objeto(tela, codigo, nome, categoria, observacao="", ativo=True, ignorar_limite=False):
    tela.abrir("objetos", acao="incluir")
    tela.preencher("codigo", codigo, ignorar_limite)
    tela.preencher("nome", nome, ignorar_limite)
    if categoria:
        tela.escolher("categoria", categoria)
    tela.preencher("observacao", observacao, ignorar_limite)
    tela.marcar("ativo-sim" if ativo else "ativo-nao")
    tela.clicar("salvar")


def objetos_no_banco(bd):
    return bd.consultar("SELECT id, codigo, nome, categoria_id, observacao, ativo FROM objeto ORDER BY id")


# ------------------------------------------------------------------ RFS09

def test_rfs09_incluir_objeto_valido(tela, bd):
    bd.criar_categoria("Ferramentas")
    incluir_objeto(tela, " fur001 ", "  Furadeira de impacto ", "Ferramentas (1)", "Armário da lavanderia")

    assert tela.mensagem() == "Objeto cadastrado com sucesso."
    assert tela.linhas() == [{"id": 1, "codigo": "FUR001", "nome": "Furadeira de impacto",
                              "categoria": "Ferramentas", "ativo": "Sim", "disponibilidade": "Disponível"}]
    assert objetos_no_banco(bd) == [(1, "FUR001", "Furadeira de impacto", 1, "Armário da lavanderia", 1)]


def test_rfs09_ativo_inicia_como_sim_e_categoria_mostra_nome_e_identificador(tela, bd):
    bd.criar_categoria("Livros")
    bd.criar_categoria("Cozinha")
    tela.abrir("objetos", acao="incluir")
    assert tela.elemento("ativo-sim").is_selected()
    assert tela.opcoes("categoria") == ["Selecione", "Cozinha (2)", "Livros (1)"]


def test_rfs09_obrigatorios_preservam_dados_digitados(tela, bd):
    bd.criar_categoria("Livros")
    incluir_objeto(tela, "   ", "", None, "Capa dura", ativo=False)

    assert tela.erros() == ["Código é obrigatório.", "Nome é obrigatório.", "Categoria é obrigatória."]
    assert tela.valor("observacao") == "Capa dura"
    assert tela.elemento("ativo-nao").is_selected()
    assert objetos_no_banco(bd) == []


def test_rfs09_limites_de_codigo_nome_e_observacao(tela, bd):
    bd.criar_categoria("Livros")
    incluir_objeto(tela, "C" * 20, "N" * 80, "Livros (1)", "O" * 250)
    assert tela.mensagem() == "Objeto cadastrado com sucesso."

    incluir_objeto(tela, "D" * 21, "N" * 81, "Livros (1)", "O" * 251, ignorar_limite=True)
    assert tela.erros() == [
        "Código deve ter no máximo 20 caracteres.",
        "Nome deve ter no máximo 80 caracteres.",
        "Observação deve ter no máximo 250 caracteres.",
    ]
    assert len(objetos_no_banco(bd)) == 1


def test_rfs09_codigo_unico_sem_diferenciar_maiusculas_e_espacos(tela, bd):
    bd.criar_categoria("Ferramentas")
    incluir_objeto(tela, "FUR001", "Furadeira", "Ferramentas (1)")
    incluir_objeto(tela, " fur001 ", "Outra furadeira", "Ferramentas (1)")

    assert tela.erros() == ["Já existe um objeto com este código."]
    assert tela.valor("nome") == "Outra furadeira"
    assert len(objetos_no_banco(bd)) == 1


def test_rfs09_sem_categoria_cadastrada_impede_inclusao(tela, bd):
    tela.abrir("objetos", acao="incluir")

    assert tela.mensagem_erro() == "Não há categorias cadastradas. Cadastre uma categoria antes de incluir objetos."
    assert not tela.existe("salvar")
    tela.clicar("ir-incluir-categoria")
    assert tela.existe("nome") and "categorias/incluir" in tela.driver.current_url
    assert bd.consultar("SELECT COUNT(*) FROM categoria") == [(0,)]


def test_rfs09_categoria_inexistente_na_gravacao(tela, bd):
    bd.criar_categoria("Livros")
    tela.abrir("objetos", acao="incluir")
    tela.preencher("codigo", "LIV001")
    tela.preencher("nome", "Dom Casmurro")
    tela.forjar_opcao("categoria", "99")
    tela.clicar("salvar")

    assert tela.erros() == ["A categoria selecionada não está cadastrada. Escolha uma categoria da lista."]
    assert objetos_no_banco(bd) == []


# ------------------------------------------------------------------ RFS10

def test_rfs10_alterar_objeto_mantem_identificador(tela, bd):
    bd.criar_categoria("Ferramentas")
    bd.criar_categoria("Jardim")
    incluir_objeto(tela, "FUR001", "Furadeira", "Ferramentas (1)")
    tela.clicar_acao(1, "alterar")

    assert tela.valor("identificador") == "1"
    assert tela.elemento("identificador").get_attribute("readonly") is not None
    assert tela.valor("disponibilidade") == "Disponível"
    assert tela.elemento("disponibilidade").get_attribute("readonly") is not None
    tela.preencher("codigo", "jar001")
    tela.preencher("nome", "Furadeira sem fio")
    tela.escolher("categoria", "Jardim (2)")
    tela.preencher("observacao", "Bateria nova")
    tela.clicar("salvar")

    assert tela.mensagem() == "Objeto alterado com sucesso."
    assert objetos_no_banco(bd) == [(1, "JAR001", "Furadeira sem fio", 2, "Bateria nova", 1)]


def test_rfs10_unicidade_desconsidera_o_proprio_objeto(tela, bd):
    categoria = bd.criar_categoria("Ferramentas")
    bd.criar_objeto(categoria, "FUR001", "Furadeira")
    bd.criar_objeto(categoria, "SER001", "Serrote")
    tela.abrir("objetos", acao="alterar", id_=1)
    tela.preencher("codigo", "fur001")
    tela.clicar("salvar")
    assert tela.mensagem() == "Objeto alterado com sucesso."

    tela.abrir("objetos", acao="alterar", id_=2)
    tela.preencher("codigo", "FUR001")
    tela.clicar("salvar")
    assert tela.erros() == ["Já existe um objeto com este código."]
    assert bd.consultar("SELECT codigo FROM objeto WHERE id = 2") == [("SER001",)]


def test_rfs10_inativar_objeto_emprestado_continua_emprestado(tela, bd):
    categoria = bd.criar_categoria("Ferramentas")
    objeto = bd.criar_objeto(categoria, "FUR001", "Furadeira")
    pessoa = bd.criar_pessoa("Ana Souza")
    bd.registrar_emprestimo(pessoa, objeto, hoje() - timedelta(days=2), hoje() + timedelta(days=5))

    tela.abrir("objetos", acao="alterar", id_=objeto)
    tela.marcar("ativo-nao")
    tela.clicar("salvar")

    assert tela.linhas() == [{"id": 1, "codigo": "FUR001", "nome": "Furadeira", "categoria": "Ferramentas",
                              "ativo": "Não", "disponibilidade": "Emprestado"}]
    assert bd.consultar("SELECT COUNT(*) FROM emprestimo WHERE data_devolucao IS NULL") == [(1,)]


# ------------------------------------------------------------------ RFS11

def preparar_consulta(bd):
    ferramentas = bd.criar_categoria("Ferramentas")
    livros = bd.criar_categoria("Livros")
    bd.criar_objeto(ferramentas, "SER001", "Serrote")
    bd.criar_objeto(ferramentas, "FUR002", "furadeira")
    bd.criar_objeto(ferramentas, "FUR001", "furadeira")
    bd.criar_objeto(livros, "LIV001", "Álgebra linear")
    bd.criar_objeto(livros, "LIV002", "Dom Casmurro", ativo=0)
    pessoa = bd.criar_pessoa("Bia Rocha")
    bd.registrar_emprestimo(pessoa, 3, hoje() - timedelta(days=1), hoje() + timedelta(days=3))


def test_rfs11_lista_em_ordem_de_nome_codigo_e_identificador(tela, bd):
    preparar_consulta(bd)
    tela.abrir("objetos")
    assert [(linha["codigo"], linha["nome"], linha["disponibilidade"]) for linha in tela.linhas()] == [
        ("LIV001", "Álgebra linear", "Disponível"),
        ("LIV002", "Dom Casmurro", "Inativo"),
        ("FUR001", "furadeira", "Emprestado"),
        ("FUR002", "furadeira", "Disponível"),
        ("SER001", "Serrote", "Disponível"),
    ]
    assert tela.texto("total") == "Objetos exibidos: 5"


def test_rfs11_filtro_codigo_compara_o_codigo_completo(tela, bd):
    preparar_consulta(bd)
    tela.abrir("objetos")
    tela.preencher("filtro-codigo", " fur001 ")
    tela.clicar("pesquisar")
    assert [linha["codigo"] for linha in tela.linhas()] == ["FUR001"]

    tela.abrir("objetos", codigo="FUR")
    assert tela.texto("vazio") == "Nenhum objeto encontrado."


def test_rfs11_filtros_combinados_por_e(tela, bd):
    preparar_consulta(bd)
    tela.abrir("objetos")
    tela.preencher("filtro-nome", "FURA")
    tela.escolher("filtro-categoria", "Ferramentas (1)")
    tela.escolher("filtro-disponibilidade", "Disponível")
    tela.clicar("pesquisar")
    assert [linha["codigo"] for linha in tela.linhas()] == ["FUR002"]

    tela.abrir("objetos", categoria="2", ativo="0")
    assert [linha["codigo"] for linha in tela.linhas()] == ["LIV002"]
    tela.abrir("objetos", disponibilidade="emprestado")
    assert [linha["codigo"] for linha in tela.linhas()] == ["FUR001"]
    tela.abrir("objetos", disponibilidade="inativo", nome="casmurro")
    assert [linha["codigo"] for linha in tela.linhas()] == ["LIV002"]


def test_rfs11_detalhe_inclui_observacao(tela, bd):
    categoria = bd.criar_categoria("Cozinha")
    bd.executar("INSERT INTO objeto (codigo, nome, categoria_id, observacao) VALUES ('PAN001', 'Panela', ?, 'Tampa solta')",
                (categoria,))
    tela.abrir("objetos")
    tela.clicar_acao(1, "detalhar")
    assert tela.texto("detalhe-codigo") == "PAN001"
    assert tela.texto("detalhe-categoria") == "Cozinha"
    assert tela.texto("detalhe-observacao") == "Tampa solta"
    assert tela.texto("detalhe-disponibilidade") == "Disponível"


# ------------------------------------------------------------------ RFS12

def test_rfs12_cancelar_exclusao_preserva_objeto(tela, bd):
    bd.criar_objeto(bd.criar_categoria("Livros"), "LIV001", "Dom Casmurro")
    tela.abrir("objetos")
    tela.clicar_acao(1, "excluir")

    assert tela.texto("confirmar-codigo") == "LIV001"
    assert tela.texto("confirmar-nome") == "Dom Casmurro"
    tela.clicar("cancelar")
    assert [linha["codigo"] for linha in tela.linhas()] == ["LIV001"]


def test_rfs12_confirmar_exclusao_remove_somente_o_objeto(tela, bd):
    categoria = bd.criar_categoria("Livros")
    bd.criar_objeto(categoria, "LIV001", "Dom Casmurro")
    bd.criar_objeto(categoria, "LIV002", "Iracema")
    tela.abrir("objetos")
    tela.clicar_acao(1, "excluir")
    tela.clicar("confirmar-exclusao")

    assert tela.mensagem() == "Objeto excluído com sucesso."
    assert [linha["codigo"] for linha in tela.linhas()] == ["LIV002"]
    assert bd.consultar("SELECT COUNT(*) FROM categoria") == [(1,)]


def test_rfs12_exclusao_bloqueada_com_emprestimo_devolvido(tela, bd):
    objeto = bd.criar_objeto(bd.criar_categoria("Livros"), "LIV001", "Dom Casmurro")
    pessoa = bd.criar_pessoa("Caio Reis")
    bd.registrar_emprestimo(pessoa, objeto, hoje() - timedelta(days=10), hoje() - timedelta(days=3),
                            devolucao=hoje() - timedelta(days=4))
    tela.abrir("objetos")
    tela.clicar_acao(objeto, "excluir")

    assert tela.mensagem_erro() == ('O objeto "LIV001 – Dom Casmurro" possui empréstimos registrados e não pode ser '
                                    "excluído. Ele pode ser inativado em Alterar objeto.")
    assert not tela.existe("confirmar-exclusao")
    tela.clicar("inativar")
    assert tela.valor("codigo") == "LIV001"
    assert bd.consultar("SELECT COUNT(*) FROM objeto") == [(1,)]


def test_rfs12_vinculo_revalidado_na_confirmacao(tela, bd):
    objeto = bd.criar_objeto(bd.criar_categoria("Livros"), "LIV001", "Dom Casmurro")
    tela.abrir("objetos")
    tela.clicar_acao(objeto, "excluir")
    # O empréstimo surge depois de a confirmação ser exibida.
    bd.registrar_emprestimo(bd.criar_pessoa("Davi Lima"), objeto, hoje(), hoje())
    tela.clicar("confirmar-exclusao")

    assert "não pode ser excluído" in tela.mensagem_erro()
    assert bd.consultar("SELECT COUNT(*) FROM objeto") == [(1,)]
