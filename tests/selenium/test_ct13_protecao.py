"""CT13 — Validação e proteção (RNF05). Cenários antecipados na R1; os demais entram na R2."""


def test_rnf05_parametros_repetidos_ou_invalidos_sao_ignorados(tela, bd):
    bd.executar("INSERT INTO pessoa (nome) VALUES ('Olga Reis')")
    for pagina in ("pessoas", "categorias"):
        tela.driver.get(f"{tela.base_url}/{pagina}/?ok=x&ok=y&ativo=talvez&ativo=1&nome=&nome=zz")
        assert tela.existe("filtros"), f"a consulta de {pagina} não foi exibida"
        assert tela.mensagem() == ""
    tela.abrir("pessoas", ativo="talvez")
    assert tela.nomes() == ["Olga Reis"]


def test_rnf05_banco_e_codigo_nao_sao_servidos(tela):
    for caminho in ("/data/esquema.sql", "/static/../db.py", "/app/db.py", "/static/../../data/esquema.sql"):
        tela.driver.get(tela.base_url + caminho)
        assert "CREATE TABLE" not in tela.driver.page_source
        assert "def conexao" not in tela.driver.page_source
