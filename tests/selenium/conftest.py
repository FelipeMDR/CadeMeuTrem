"""Infraestrutura dos testes Selenium.

Cada execução sobe a aplicação Flask com um banco SQLite temporário
(variável CMT_DB), abre o Chrome em modo headless e limpa as tabelas antes de
cada teste. O banco real em data/ nunca é tocado.

Variável opcional:
  MOSTRAR_NAVEGADOR=1   abre o Chrome visível em vez de headless
"""

import os
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = Path(__file__).resolve().parent / "saida"


def porta_livre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def aguardar_porta(porta: int, limite_s: float = 10) -> None:
    fim = time.monotonic() + limite_s
    while time.monotonic() < fim:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", porta)) == 0:
                return
        time.sleep(0.1)
    raise RuntimeError(f"A aplicação Flask não respondeu na porta {porta}.")


@pytest.fixture(scope="session")
def banco(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("banco") / "teste.sqlite"


@pytest.fixture(scope="session")
def servidor(banco):
    SAIDA.mkdir(exist_ok=True)
    porta = porta_livre()
    ambiente = dict(os.environ, CMT_DB=str(banco))
    with open(SAIDA / "servidor.log", "w", encoding="utf-8") as log:
        processo = subprocess.Popen(
            [sys.executable, "-m", "flask", "--app", "app", "run", "--host", "127.0.0.1", "--port", str(porta)],
            cwd=RAIZ, env=ambiente, stdout=log, stderr=subprocess.STDOUT,
        )
        try:
            aguardar_porta(porta)
            url = f"http://127.0.0.1:{porta}"
            urllib.request.urlopen(url + "/pessoas/").read()
            yield url
        finally:
            processo.terminate()
            processo.wait(timeout=5)


@pytest.fixture(scope="session")
def navegador():
    opcoes = webdriver.ChromeOptions()
    if os.environ.get("MOSTRAR_NAVEGADOR") != "1":
        opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1280,900")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opcoes)
    registrar_ambiente(driver)
    yield driver
    driver.quit()


def registrar_ambiente(driver) -> None:
    """Grava as versões usadas na execução (RNF03 e RNF06) em tests/selenium/saida/ambiente.txt."""
    import platform
    from importlib.metadata import version

    import selenium

    capacidades = driver.capabilities
    linhas = [
        f"Sistema: {platform.system()} {platform.release()} ({platform.version()})",
        f"Python: {platform.python_version()}",
        f"Flask: {version('flask')}",
        f"Selenium: {selenium.__version__}",
        f"Navegador: {capacidades.get('browserName')} {capacidades.get('browserVersion')}",
        f"ChromeDriver: {capacidades.get('chrome', {}).get('chromedriverVersion', '').split(' ')[0]}",
    ]
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "ambiente.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")


class Banco:
    """Acesso direto ao banco de teste para preparar cenários e conferir o resultado."""

    def __init__(self, caminho: Path):
        self.caminho = caminho

    def _conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    def limpar(self) -> None:
        with self._conectar() as c:
            c.executescript(
                "DELETE FROM emprestimo; DELETE FROM objeto; DELETE FROM pessoa; DELETE FROM categoria;"
                "DELETE FROM sqlite_sequence;"
            )

    def consultar(self, sql: str, parametros=()) -> list[tuple]:
        with self._conectar() as c:
            return c.execute(sql, parametros).fetchall()

    def executar(self, sql: str, parametros=()) -> int:
        with self._conectar() as c:
            return c.execute(sql, parametros).lastrowid

    def criar_objeto(self, categoria_id: int, codigo: str = "OBJ001") -> int:
        return self.executar(
            "INSERT INTO objeto (codigo, nome, categoria_id) VALUES (?, ?, ?)",
            (codigo, f"Objeto {codigo}", categoria_id),
        )

    def criar_emprestimo(self, pessoa_id: int) -> int:
        categoria_id = self.executar(
            "INSERT INTO categoria (nome, nome_chave) VALUES ('Apoio', 'apoio')"
        )
        objeto_id = self.criar_objeto(categoria_id, "APO001")
        return self.executar(
            "INSERT INTO emprestimo (pessoa_id, objeto_id, data_retirada, previsao_devolucao)"
            " VALUES (?, ?, '2026-10-20', '2026-10-27')",
            (pessoa_id, objeto_id),
        )


class Tela:
    """Ações de alto nível sobre as páginas, usando os ids definidos nas telas."""

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url

    def abrir(self, pagina: str, acao: str | None = None, id_: int | None = None, **filtros) -> None:
        """Abre /pagina/[id/][acao] com os filtros na query string (ex.: /pessoas/?ativo=0)."""
        caminho = "/".join(str(parte) for parte in (pagina, id_, acao) if parte is not None)
        consulta = f"?{urllib.parse.urlencode(filtros)}" if filtros else ""
        barra = "/" if acao is None and id_ is None else ""  # listas terminam em /, como /pessoas/
        self.driver.get(f"{self.base_url}/{caminho}{barra}{consulta}")

    def elemento(self, id_: str):
        return self.driver.find_element(By.ID, id_)

    def existe(self, id_: str) -> bool:
        return len(self.driver.find_elements(By.ID, id_)) > 0

    def preencher(self, id_: str, valor: str, ignorar_limite: bool = False) -> None:
        campo = self.elemento(id_)
        if ignorar_limite:
            # Remove o maxlength do navegador para verificar a validação no servidor.
            self.driver.execute_script("arguments[0].removeAttribute('maxlength')", campo)
        campo.clear()
        if valor:
            campo.send_keys(valor)

    def valor(self, id_: str) -> str:
        return self.elemento(id_).get_attribute("value")

    def texto(self, id_: str) -> str:
        return self.elemento(id_).text

    def _navegar(self, acao) -> None:
        """Executa a ação e aguarda a página seguinte terminar de carregar.

        Marca a página atual com uma variável JavaScript e espera um documento novo
        (sem a marca) e completo. Erros do navegador durante a troca de página
        significam que a navegação ainda está em andamento.
        """
        self.driver.execute_script("window.__paginaAnterior = true;")
        acao()

        def nova_pagina_carregada(driver) -> bool:
            try:
                return driver.execute_script(
                    "return window.__paginaAnterior === undefined && document.readyState === 'complete';"
                )
            except WebDriverException:
                return False

        WebDriverWait(self.driver, 10).until(nova_pagina_carregada)

    def clicar(self, id_: str) -> None:
        """Clica e aguarda a próxima página carregar."""
        self._navegar(lambda: self.elemento(id_).click())

    def marcar(self, id_: str) -> None:
        self.elemento(id_).click()

    def clicar_acao(self, id_registro: int, acao: str) -> None:
        seletor = f'#lista tr[data-id="{id_registro}"] a.acao-{acao}'
        self._navegar(lambda: self.driver.find_element(By.CSS_SELECTOR, seletor).click())

    def erros(self) -> list[str]:
        return [li.text for li in self.driver.find_elements(By.CSS_SELECTOR, "#erros li")]

    def mensagem(self) -> str:
        return self.texto("mensagem") if self.existe("mensagem") else ""

    def mensagem_erro(self) -> str:
        return self.texto("mensagem-erro") if self.existe("mensagem-erro") else ""

    def linhas(self) -> list[dict]:
        resultado = []
        for tr in self.driver.find_elements(By.CSS_SELECTOR, "#lista tbody tr"):
            linha = {td.get_attribute("class").removeprefix("col-"): td.text
                     for td in tr.find_elements(By.CSS_SELECTOR, "td[class^='col-']")}
            # A coluna Identificador exibida deve corresponder ao registro da linha.
            assert linha["id"] == tr.get_attribute("data-id")
            linha["id"] = int(linha["id"])
            resultado.append(linha)
        return resultado

    def nomes(self) -> list[str]:
        return [linha["nome"] for linha in self.linhas()]


@pytest.fixture
def bd(servidor, banco) -> Banco:
    acesso = Banco(banco)
    acesso.limpar()
    return acesso


@pytest.fixture
def tela(navegador, servidor, bd) -> Tela:
    return Tela(navegador, servidor)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda uma captura de tela em tests/selenium/saida/ quando um teste falha."""
    resultado = yield
    relatorio = resultado.get_result()
    if relatorio.when == "call" and relatorio.failed and "tela" in item.funcargs:
        SAIDA.mkdir(exist_ok=True)
        item.funcargs["tela"].driver.save_screenshot(str(SAIDA / f"{item.name}.png"))
