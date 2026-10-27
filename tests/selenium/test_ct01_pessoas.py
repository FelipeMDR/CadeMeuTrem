"""CT01 — Manter pessoas (RFS01 a RFS04), conforme a aba Testes da MRB."""


def incluir_pessoa(tela, nome, contato="", ativo=True, ignorar_limite=False):
    tela.abrir("pessoas", acao="incluir")
    tela.preencher("nome", nome, ignorar_limite)
    tela.preencher("contato", contato, ignorar_limite)
    tela.marcar("ativo-sim" if ativo else "ativo-nao")
    tela.clicar("salvar")


# ------------------------------------------------------------------ RFS01

def test_rfs01_incluir_pessoa_valida(tela, bd):
    incluir_pessoa(tela, "Ana Souza", "ana@exemplo.com")

    assert tela.mensagem() == "Pessoa cadastrada com sucesso."
    assert tela.linhas() == [{"id": 1, "nome": "Ana Souza", "contato": "ana@exemplo.com", "ativo": "Sim"}]
    assert bd.consultar("SELECT nome, contato, ativo FROM pessoa") == [("Ana Souza", "ana@exemplo.com", 1)]


def test_rfs01_ativo_inicia_como_sim(tela):
    tela.abrir("pessoas", acao="incluir")
    assert tela.elemento("ativo-sim").is_selected()
    assert not tela.elemento("ativo-nao").is_selected()


def test_rfs01_espacos_nas_extremidades_sao_removidos(tela, bd):
    incluir_pessoa(tela, "   Bruno Lima   ", "  quarto 2  ")
    assert bd.consultar("SELECT nome, contato FROM pessoa") == [("Bruno Lima", "quarto 2")]


def test_rfs01_nome_obrigatorio_preserva_dados_digitados(tela, bd):
    incluir_pessoa(tela, "     ", "Quarto 2", ativo=False)

    assert tela.erros() == ["Nome é obrigatório."]
    assert tela.valor("contato") == "Quarto 2"
    assert tela.elemento("ativo-nao").is_selected()
    assert bd.consultar("SELECT COUNT(*) FROM pessoa") == [(0,)]


def test_rfs01_limites_de_nome_e_contato(tela, bd):
    # 80 caracteres são aceitos.
    incluir_pessoa(tela, "N" * 80, "C" * 80)
    assert tela.mensagem() == "Pessoa cadastrada com sucesso."

    # O navegador limita a digitação a 80 caracteres.
    tela.abrir("pessoas", acao="incluir")
    tela.preencher("nome", "X" * 85)
    assert len(tela.valor("nome")) == 80

    # Sem o limite do navegador, o servidor recusa 81 caracteres.
    incluir_pessoa(tela, "N" * 81, "C" * 81, ignorar_limite=True)
    assert tela.erros() == [
        "Nome deve ter no máximo 80 caracteres.",
        "Contato deve ter no máximo 80 caracteres.",
    ]
    assert bd.consultar("SELECT COUNT(*) FROM pessoa") == [(1,)]


def test_rfs01_homonimos_sao_permitidos(tela):
    incluir_pessoa(tela, "Carlos Lima")
    incluir_pessoa(tela, "Carlos Lima", "outro contato")

    linhas = tela.linhas()
    assert [linha["nome"] for linha in linhas] == ["Carlos Lima", "Carlos Lima"]
    assert [linha["id"] for linha in linhas] == [1, 2]


def test_rfs01_texto_com_html_e_exibido_como_texto(tela):
    incluir_pessoa(tela, '<b>Dani</b> "D\'Ávila"')
    assert tela.nomes() == ['<b>Dani</b> "D\'Ávila"']


# ------------------------------------------------------------------ RFS02

def test_rfs02_alterar_pessoa_mantem_identificador(tela, bd):
    incluir_pessoa(tela, "Eva Prado", "eva@exemplo.com")
    tela.clicar_acao(1, "alterar")

    assert tela.valor("identificador") == "1"
    assert tela.elemento("identificador").get_attribute("readonly") is not None
    tela.preencher("nome", "Eva Prado Reis")
    tela.preencher("contato", "")
    tela.marcar("ativo-nao")
    tela.clicar("salvar")

    assert tela.mensagem() == "Pessoa alterada com sucesso."
    assert tela.linhas() == [{"id": 1, "nome": "Eva Prado Reis", "contato": "", "ativo": "Não"}]
    assert bd.consultar("SELECT id, nome, contato, ativo FROM pessoa") == [(1, "Eva Prado Reis", None, 0)]


def test_rfs02_alteracao_aplica_as_mesmas_validacoes(tela, bd):
    incluir_pessoa(tela, "Fabio Neves")
    tela.clicar_acao(1, "alterar")
    tela.preencher("nome", "")
    tela.clicar("salvar")

    assert tela.erros() == ["Nome é obrigatório."]
    assert bd.consultar("SELECT nome FROM pessoa") == [("Fabio Neves",)]


def test_rfs02_reativar_pessoa(tela, bd):
    incluir_pessoa(tela, "Gabi Torres", ativo=False)
    tela.clicar_acao(1, "alterar")
    assert tela.elemento("ativo-nao").is_selected()
    tela.marcar("ativo-sim")
    tela.clicar("salvar")
    assert bd.consultar("SELECT ativo FROM pessoa") == [(1,)]


# ------------------------------------------------------------------ RFS03

def preparar_consulta(bd):
    for nome, ativo in [("carla Dias", 1), ("Bruno Alves", 1), ("Álvaro Reis", 1), ("Ana Clara", 0), ("ANA Paula", 1)]:
        bd.executar("INSERT INTO pessoa (nome, ativo) VALUES (?, ?)", (nome, ativo))


def test_rfs03_lista_em_ordem_alfabetica(tela, bd):
    preparar_consulta(bd)
    tela.abrir("pessoas")
    assert tela.nomes() == ["Álvaro Reis", "Ana Clara", "ANA Paula", "Bruno Alves", "carla Dias"]
    assert tela.texto("total") == "Pessoas exibidas: 5"


def test_rfs03_desempate_por_identificador(tela, bd):
    bd.executar("INSERT INTO pessoa (nome) VALUES ('Igual')")
    bd.executar("INSERT INTO pessoa (nome) VALUES ('Igual')")
    tela.abrir("pessoas")
    assert [linha["id"] for linha in tela.linhas()] == [1, 2]


def test_rfs03_filtro_por_trecho_do_nome_sem_diferenciar_maiusculas(tela, bd):
    preparar_consulta(bd)
    tela.abrir("pessoas")
    tela.preencher("filtro-nome", "an")
    tela.clicar("pesquisar")
    assert tela.nomes() == ["Ana Clara", "ANA Paula"]


def test_rfs03_filtro_ativo_combinado_por_e(tela, bd):
    preparar_consulta(bd)
    tela.abrir("pessoas", ativo="0")
    assert tela.nomes() == ["Ana Clara"]

    tela.abrir("pessoas", nome="ana", ativo="1")
    assert tela.nomes() == ["ANA Paula"]


def test_rfs03_sem_resultados(tela, bd):
    preparar_consulta(bd)
    tela.abrir("pessoas", nome="Zuleica")
    assert tela.texto("vazio") == "Nenhuma pessoa encontrada."
    assert tela.linhas() == []


def test_rfs03_detalhe_apresenta_os_mesmos_campos(tela, bd):
    bd.executar("INSERT INTO pessoa (nome, contato, ativo) VALUES ('Hugo Melo', 'Quarto 5', 0)")
    tela.abrir("pessoas")
    tela.clicar_acao(1, "detalhar")
    assert tela.texto("detalhe-id") == "1"
    assert tela.texto("detalhe-nome") == "Hugo Melo"
    assert tela.texto("detalhe-contato") == "Quarto 5"
    assert tela.texto("detalhe-ativo") == "Não"


# ------------------------------------------------------------------ RFS04

def test_rfs04_cancelar_exclusao_preserva_pessoa(tela, bd):
    bd.executar("INSERT INTO pessoa (nome) VALUES ('Iara Lopes')")
    tela.abrir("pessoas")
    tela.clicar_acao(1, "excluir")

    assert tela.texto("confirmar-id") == "1"
    assert tela.texto("confirmar-nome") == "Iara Lopes"
    tela.clicar("cancelar")
    assert tela.nomes() == ["Iara Lopes"]


def test_rfs04_confirmar_exclusao_remove_somente_a_pessoa(tela, bd):
    bd.executar("INSERT INTO pessoa (nome) VALUES ('Joao Paz')")
    bd.executar("INSERT INTO pessoa (nome) VALUES ('Karen Luz')")
    tela.abrir("pessoas")
    tela.clicar_acao(1, "excluir")
    tela.clicar("confirmar-exclusao")

    assert tela.mensagem() == "Pessoa excluída com sucesso."
    assert tela.nomes() == ["Karen Luz"]


def test_rfs04_exclusao_bloqueada_quando_ha_emprestimo(tela, bd):
    pessoa_id = bd.executar("INSERT INTO pessoa (nome) VALUES ('Lia Campos')")
    bd.criar_emprestimo(pessoa_id)
    tela.abrir("pessoas")
    tela.clicar_acao(pessoa_id, "excluir")

    assert "possui empréstimos registrados e não pode ser excluída" in tela.mensagem_erro()
    assert "inativada em Alterar pessoa" in tela.mensagem_erro()
    assert not tela.existe("confirmar-exclusao")
    assert bd.consultar("SELECT COUNT(*) FROM pessoa") == [(1,)]
    assert bd.consultar("SELECT COUNT(*) FROM emprestimo") == [(1,)]


def test_rfs04_vinculo_revalidado_na_confirmacao(tela, bd):
    pessoa_id = bd.executar("INSERT INTO pessoa (nome) VALUES ('Mara Dutra')")
    tela.abrir("pessoas")
    tela.clicar_acao(pessoa_id, "excluir")
    # O empréstimo surge depois de a confirmação ser exibida.
    bd.criar_emprestimo(pessoa_id)
    tela.clicar("confirmar-exclusao")

    assert "não pode ser excluída" in tela.mensagem_erro()
    assert bd.consultar("SELECT COUNT(*) FROM pessoa") == [(1,)]
