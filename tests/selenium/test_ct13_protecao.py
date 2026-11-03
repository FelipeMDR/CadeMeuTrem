"""CT13 — Validação e proteção (RNF05), conforme a aba Testes da MRB.

Limites e datas inválidas de cada cadastro também são verificados no CT01, CT02, CT03 e CT06.
"""

from datetime import timedelta

from conftest import br, hoje

PARAMETROS_INVALIDOS = ("?ok=x&ok=y&ativo=talvez&ativo=1&nome=&nome=zz&categoria=abc&disponibilidade=quebrado"
                        "&pessoa=-1&objeto=99999999999999999999&situacao=talvez")


def test_rnf05_parametros_repetidos_ou_invalidos_sao_ignorados(tela, bd):
    bd.executar("INSERT INTO pessoa (nome) VALUES ('Olga Reis')")
    for pagina in ("pessoas", "categorias", "objetos", "emprestimos"):
        tela.ir(f"/{pagina}/{PARAMETROS_INVALIDOS}")
        assert tela.existe("filtros"), f"a consulta de {pagina} não foi exibida"
        assert tela.mensagem() == ""
    tela.abrir("pessoas", ativo="talvez")
    assert tela.nomes() == ["Olga Reis"]


def test_rnf05_banco_e_codigo_nao_sao_servidos(tela):
    for caminho in ("/data/esquema.sql", "/static/../db.py", "/app/db.py", "/static/../../data/esquema.sql"):
        tela.ir(caminho)
        assert "CREATE TABLE" not in tela.driver.page_source
        assert "def conexao" not in tela.driver.page_source


def test_rnf05_texto_com_html_e_aspas_e_exibido_como_texto(tela, bd):
    categoria = bd.criar_categoria("Ferramentas")
    bd.criar_pessoa("Ana Souza")
    nome = '<script>document.title="x"</script> Fura\'deira "grande"'
    tela.abrir("objetos", acao="incluir")
    tela.preencher("codigo", "FUR001")
    tela.preencher("nome", nome)
    tela.escolher("categoria", f"Ferramentas ({categoria})")
    tela.preencher("observacao", "<b>frágil</b>")
    tela.clicar("salvar")
    assert tela.nomes() == [nome]

    tela.abrir("emprestimos", acao="incluir")
    tela.escolher("pessoa", "Ana Souza (1)")
    tela.escolher("objeto", f"FUR001 – {nome}")
    tela.preencher("previsao-devolucao", br(hoje() + timedelta(days=1)))
    tela.preencher("observacao", '<img src=x onerror="document.title=1">')
    tela.clicar("salvar")
    tela.clicar_acao(1, "detalhar")
    assert tela.texto("detalhe-objeto") == nome
    assert tela.texto("detalhe-observacao") == '<img src=x onerror="document.title=1">'
    assert tela.driver.title == "Detalhe do empréstimo — Cadê Meu Trem?"


def test_rnf05_observacao_do_emprestimo_acima_do_limite_e_recusada(tela, bd):
    bd.criar_objeto(bd.criar_categoria("Livros"), "LIV001", "Iracema")
    bd.criar_pessoa("Ana Souza")
    tela.abrir("emprestimos", acao="incluir")
    tela.escolher("pessoa", "Ana Souza (1)")
    tela.escolher("objeto", "LIV001 – Iracema")
    tela.preencher("previsao-devolucao", br(hoje()))
    tela.preencher("observacao", "O" * 251, ignorar_limite=True)
    tela.clicar("salvar")

    assert tela.erros() == ["Observação deve ter no máximo 250 caracteres."]
    assert bd.consultar("SELECT COUNT(*) FROM emprestimo") == [(0,)]


def test_rnf05_formulario_sem_token_valido_e_recusado(tela, bd):
    """Proteção contra envio por outro site (CSRF): sem o token da sessão, nada é gravado."""
    tela.abrir("pessoas", acao="incluir")
    tela.preencher("nome", "Pessoa forjada")
    tela.driver.execute_script("document.querySelector('input[name=token_csrf]').value = 'forjado';")
    tela.clicar("salvar")
    assert tela.texto("mensagem-erro").startswith("O formulário expirou ou não veio desta aplicação.")

    tela.abrir("pessoas", acao="incluir")
    tela.preencher("nome", "Pessoa sem token")
    tela.driver.execute_script("document.querySelector('input[name=token_csrf]').remove();")
    tela.clicar("salvar")
    assert "Nada foi gravado" in tela.texto("mensagem-erro")
    assert bd.consultar("SELECT COUNT(*) FROM pessoa") == [(0,)]
