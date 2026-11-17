"""CT09 — Interface em português (RNF01), conforme a aba Testes da MRB.

Percorre as telas disponíveis, provoca erros de preenchimento e cancela exclusões.
"""

from datetime import timedelta

from selenium.webdriver.common.by import By

from conftest import hoje

MENU = ["Início", "Pessoas", "Categorias", "Objetos", "Empréstimos", "Pendências"]
TELAS = [
    ("/", "Controle de empréstimos de objetos"),
    ("/pessoas/", "Pessoas"),
    ("/pessoas/incluir", "Incluir pessoa"),
    ("/categorias/", "Categorias"),
    ("/categorias/incluir", "Incluir categoria"),
    ("/objetos/", "Objetos"),
    ("/emprestimos/", "Empréstimos"),
    ("/relatorios/pendencias", "Pendências e atrasos"),
]


def test_rnf01_telas_em_portugues_com_menu_completo(tela):
    for caminho, titulo in TELAS:
        tela.ir(caminho)
        assert tela.driver.find_element(By.TAG_NAME, "html").get_attribute("lang") == "pt-BR", caminho
        assert tela.driver.find_element(By.TAG_NAME, "h1").text == titulo, caminho
        assert [a.text for a in tela.driver.find_elements(By.CSS_SELECTOR, ".topo nav a")] == MENU, caminho


def test_rnf01_erros_junto_ao_formulario_preservam_os_dados(tela, bd):
    bd.criar_categoria("Livros")
    bd.criar_objeto(1, "Iracema")
    bd.criar_pessoa("Ana Souza")

    tela.abrir("pessoas", acao="incluir")
    tela.preencher("contato", "Quarto 2")
    tela.clicar("salvar")
    assert tela.erros() == ["Nome é obrigatório."] and tela.valor("contato") == "Quarto 2"

    tela.abrir("objetos", acao="incluir")
    tela.preencher("observacao", "Capa dura")
    tela.clicar("salvar")
    assert tela.erros() == ["Nome é obrigatório.", "Categoria é obrigatória."]
    assert tela.valor("observacao") == "Capa dura"

    tela.abrir("emprestimos", acao="incluir")
    tela.escolher("objeto", "Iracema (1)")
    tela.preencher("observacao", "Para a prova")
    tela.clicar("salvar")
    assert tela.erros() == ["Pessoa é obrigatória.", "Previsão de devolução é obrigatória."]
    assert tela.escolhido("objeto") == "Iracema (1)" and tela.valor("observacao") == "Para a prova"


def test_rnf01_exclusoes_exigem_confirmacao_e_cancelar_preserva(tela, bd):
    vazia = bd.criar_categoria("Jardim")
    livros = bd.criar_categoria("Livros")
    sem_vinculo = bd.criar_pessoa("Bruno Lima")
    leitora = bd.criar_pessoa("Ana Souza")
    livre = bd.criar_objeto(livros, "Iracema")
    emprestado = bd.criar_objeto(livros, "Dom Casmurro")
    emprestimo = bd.registrar_emprestimo(leitora, emprestado, hoje() - timedelta(days=1), hoje())

    for pagina, id_ in (("pessoas", sem_vinculo), ("categorias", vazia), ("objetos", livre), ("emprestimos", emprestimo)):
        tela.abrir(pagina)
        tela.clicar_acao(id_, "excluir")
        assert tela.existe("confirmar-exclusao"), pagina
        assert "Confirma a exclusão" in tela.texto("confirmacao"), pagina
        tela.clicar("cancelar")
        assert tela.existe("lista"), pagina

    assert bd.consultar("SELECT (SELECT COUNT(*) FROM pessoa), (SELECT COUNT(*) FROM categoria),"
                        " (SELECT COUNT(*) FROM objeto), (SELECT COUNT(*) FROM emprestimo)") == [(2, 2, 2, 1)]
