"""Infraestrutura dos testes Selenium.

Cada execução sobe a aplicação Flask com um banco SQLite temporário
(variável CMT_DB), abre o Chrome em modo headless e limpa as tabelas antes de
cada teste. O banco real em data/ nunca é tocado.

Variáveis opcionais (scripts\\demonstrar_testes.bat já define a primeira):
  MOSTRAR_NAVEGADOR=1   abre o Chrome visível em ritmo de demonstração: destaca cada
                        campo ou botão antes de usá-lo, digita letra por letra, deixa
                        cada página na tela por um instante e mostra o cenário em execução
  PAUSA_SELENIUM=0.8    pausa básica do ritmo de demonstração, em segundos (0 desliga)
  CHROME_BINARIO=...    caminho do chrome.exe, quando o Selenium não o encontra sozinho
"""

import math
import os
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = Path(__file__).resolve().parent / "saida"
MOSTRAR_NAVEGADOR = os.environ.get("MOSTRAR_NAVEGADOR") == "1"
# Sem janela (padrão e GitHub Actions), os testes rodam sem pausas.
PAUSA = float(os.environ.get("PAUSA_SELENIUM", "0.8")) if MOSTRAR_NAVEGADOR else 0.0

# Caixa no canto da página com o cenário em execução. Não recebe cliques
# (pointer-events: none), então não atrapalha as ações do teste.
MOSTRAR_CENARIO_JS = """
if (!document.body) return;
var caixa = document.getElementById('cenario-selenium') || document.createElement('div');
caixa.id = 'cenario-selenium';
caixa.textContent = arguments[0];
caixa.style.cssText = 'position:fixed;right:12px;bottom:12px;z-index:9999;max-width:60%;padding:8px 12px;'
    + 'background:#212529;color:#fff;font:15px/1.35 sans-serif;border-radius:6px;opacity:.92;pointer-events:none';
document.body.appendChild(caixa);
"""


def hoje() -> date:
    """Dia atual no mesmo fuso da aplicação (America/Sao_Paulo)."""
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date()


def br(dia: date) -> str:
    return dia.strftime("%d/%m/%Y")


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


@contextmanager
def aplicacao_rodando(banco: Path, nome_log: str = "servidor.log"):
    """Sobe a aplicação Flask com o banco informado e devolve a URL; encerra o processo ao sair."""
    SAIDA.mkdir(exist_ok=True)
    porta = porta_livre()
    ambiente = dict(os.environ, CMT_DB=str(banco))
    with open(SAIDA / nome_log, "w", encoding="utf-8") as log:
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
def servidor(banco):
    with aplicacao_rodando(banco) as url:
        yield url


@pytest.fixture(scope="session")
def navegador():
    opcoes = webdriver.ChromeOptions()
    if not MOSTRAR_NAVEGADOR:
        opcoes.add_argument("--headless=new")
    if os.environ.get("CHROME_BINARIO"):
        opcoes.binary_location = os.environ["CHROME_BINARIO"]
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

    def criar_pessoa(self, nome: str, ativo: int = 1) -> int:
        return self.executar("INSERT INTO pessoa (nome, ativo) VALUES (?, ?)", (nome, ativo))

    def criar_categoria(self, nome: str) -> int:
        return self.executar("INSERT INTO categoria (nome, nome_chave) VALUES (?, ?)", (nome, nome.strip().lower()))

    def criar_objeto(self, categoria_id: int, codigo: str = "OBJ001", nome: str | None = None, ativo: int = 1) -> int:
        return self.executar(
            "INSERT INTO objeto (codigo, nome, categoria_id, ativo) VALUES (?, ?, ?, ?)",
            (codigo, nome or f"Objeto {codigo}", categoria_id, ativo),
        )

    def registrar_emprestimo(self, pessoa_id: int, objeto_id: int, retirada: date, previsao: date,
                             devolucao: date | None = None) -> int:
        return self.executar(
            "INSERT INTO emprestimo (pessoa_id, objeto_id, data_retirada, previsao_devolucao, data_devolucao)"
            " VALUES (?, ?, ?, ?, ?)",
            (pessoa_id, objeto_id, retirada.isoformat(), previsao.isoformat(),
             devolucao.isoformat() if devolucao else None),
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


def descrever_cenario(item) -> str:
    """test_ct01_pessoas.py::test_rfs01_incluir_pessoa_valida -> 'CT01 · RFS01 — incluir pessoa valida'."""
    caso = item.path.stem.split("_")[1].upper()
    requisito, _, resto = item.name.removeprefix("test_").partition("_")
    return f"{caso} · {requisito.upper()} — {resto.replace('_', ' ')}"


class Tela:
    """Ações de alto nível sobre as páginas, usando os ids definidos nas telas.

    Com PAUSA > 0 (MOSTRAR_NAVEGADOR=1), cada ação segue o ritmo de demonstração.
    """

    def __init__(self, driver, base_url: str, cenario: str = ""):
        self.driver = driver
        self.base_url = base_url
        self.cenario = cenario

    # ------------------------------------------------ ritmo de demonstração

    def _pausar(self, fracao: float = 1.0) -> None:
        if PAUSA:
            time.sleep(PAUSA * fracao)

    def _pagina_exibida(self) -> None:
        """Mostra o cenário no canto da página e a deixa na tela por um instante."""
        if PAUSA:
            self.driver.execute_script(MOSTRAR_CENARIO_JS, self.cenario)
            self._pausar()

    def _destacar(self, elemento) -> None:
        if PAUSA:
            self.driver.execute_script(
                "arguments[0].style.outline = '3px solid #e8590c'; arguments[0].style.outlineOffset = '2px';",
                elemento,
            )
            self._pausar(0.5)

    def _remover_destaque(self, elemento) -> None:
        if PAUSA:
            self.driver.execute_script("arguments[0].style.outline = '';", elemento)

    def _digitar(self, campo, valor: str) -> None:
        if not PAUSA:
            campo.send_keys(valor)
            return
        # Até 25 etapas: textos longos (limites de 80 caracteres) não atrasam a demonstração.
        passo = max(1, math.ceil(len(valor) / 25))
        for inicio in range(0, len(valor), passo):
            campo.send_keys(valor[inicio:inicio + passo])
            time.sleep(PAUSA / 20)

    # ------------------------------------------------------------- ações

    def ir(self, caminho: str) -> None:
        """Abre um endereço da aplicação, como /pessoas/?ativo=1."""
        self.driver.get(self.base_url + caminho)
        self._pagina_exibida()

    def abrir(self, pagina: str, acao: str | None = None, id_: int | None = None, **filtros) -> None:
        """Abre /pagina/[id/][acao] com os filtros na query string (ex.: /pessoas/?ativo=0)."""
        caminho = "/".join(str(parte) for parte in (pagina, id_, acao) if parte is not None)
        consulta = f"?{urllib.parse.urlencode(filtros)}" if filtros else ""
        barra = "/" if acao is None and id_ is None else ""  # listas terminam em /, como /pessoas/
        self.ir(f"/{caminho}{barra}{consulta}")

    def elemento(self, id_: str):
        return self.driver.find_element(By.ID, id_)

    def existe(self, id_: str) -> bool:
        return len(self.driver.find_elements(By.ID, id_)) > 0

    def preencher(self, id_: str, valor: str, ignorar_limite: bool = False) -> None:
        campo = self.elemento(id_)
        if ignorar_limite:
            # Remove o maxlength do navegador para verificar a validação no servidor.
            self.driver.execute_script("arguments[0].removeAttribute('maxlength')", campo)
        self._destacar(campo)
        campo.clear()
        if valor:
            self._digitar(campo, valor)
        self._pausar(0.5)
        self._remover_destaque(campo)

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
        self._pagina_exibida()

    def clicar(self, id_: str) -> None:
        """Clica e aguarda a próxima página carregar."""
        botao = self.elemento(id_)
        self._destacar(botao)
        self._navegar(botao.click)

    def escolher(self, id_: str, texto: str) -> None:
        """Escolhe uma opção da lista pelo texto exibido."""
        lista = self.elemento(id_)
        self._destacar(lista)
        Select(lista).select_by_visible_text(texto)
        self._pausar(0.5)
        self._remover_destaque(lista)

    def opcoes(self, id_: str) -> list[str]:
        return [opcao.text for opcao in Select(self.elemento(id_)).options]

    def escolhido(self, id_: str) -> str:
        return Select(self.elemento(id_)).first_selected_option.text

    def forjar_opcao(self, id_: str, valor: str) -> None:
        """Simula um envio adulterado: acrescenta à lista um valor que ela não oferece e o escolhe."""
        self.driver.execute_script(
            "var opcao = document.createElement('option'); opcao.value = arguments[1];"
            "opcao.text = 'valor forjado'; arguments[0].appendChild(opcao); arguments[0].value = arguments[1];",
            self.elemento(id_), valor)

    def destravar(self, id_: str) -> None:
        """Remove o somente leitura de um campo, para verificar que o servidor ignora a alteração."""
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", self.elemento(id_))

    def marcar(self, id_: str) -> None:
        opcao = self.elemento(id_)
        self._destacar(opcao)
        opcao.click()
        self._pausar(0.5)
        self._remover_destaque(opcao)

    def clicar_acao(self, id_registro: int, acao: str) -> None:
        link = self.driver.find_element(By.CSS_SELECTOR, f'#lista tr[data-id="{id_registro}"] a.acao-{acao}')
        self._destacar(link)
        self._navegar(link.click)

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
def tela(navegador, servidor, bd, request) -> Tela:
    return Tela(navegador, servidor, descrever_cenario(request.node))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda uma captura de tela em tests/selenium/saida/ quando um teste falha."""
    resultado = yield
    relatorio = resultado.get_result()
    if relatorio.when == "call" and relatorio.failed and "tela" in item.funcargs:
        SAIDA.mkdir(exist_ok=True)
        item.funcargs["tela"].driver.save_screenshot(str(SAIDA / f"{item.name}.png"))
