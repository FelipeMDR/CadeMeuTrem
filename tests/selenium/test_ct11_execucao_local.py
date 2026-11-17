"""CT11 — Execução local, sem internet (RNF03), conforme a aba Testes da MRB.

A parte automatizada confere que nenhuma página carrega arquivo de fora da aplicação (CDN, fontes,
scripts). O procedimento com a internet desligada está no README e no relatório de testes da R4.
"""

from pathlib import Path

from selenium.webdriver.common.by import By

from conftest import RAIZ

PAGINAS = ["/", "/pessoas/", "/pessoas/incluir", "/categorias/", "/objetos/", "/emprestimos/",
           "/relatorios/pendencias", "/relatorios/historico"]


def test_rnf03_paginas_usam_somente_arquivos_da_propria_aplicacao(tela, bd):
    bd.criar_categoria("Livros")
    for caminho in PAGINAS:
        tela.ir(caminho)
        recursos = tela.driver.execute_script(
            "return performance.getEntriesByType('resource').map(r => r.name);")
        externos = [r for r in recursos if not r.startswith(tela.base_url)]
        assert externos == [], (caminho, externos)
        for tag, atributo in (("script", "src"), ("link", "href"), ("img", "src"), ("iframe", "src")):
            for elemento in tela.driver.find_elements(By.TAG_NAME, tag):
                endereco = elemento.get_attribute(atributo) or ""
                assert endereco == "" or endereco.startswith(tela.base_url), (caminho, tag, endereco)


def test_rnf03_servidor_atende_somente_esta_maquina(tela):
    assert tela.base_url.startswith("http://127.0.0.1:")
    inicializacao = (Path(RAIZ) / "scripts" / "iniciar.bat").read_text(encoding="utf-8")
    assert "--host 127.0.0.1" in inicializacao
