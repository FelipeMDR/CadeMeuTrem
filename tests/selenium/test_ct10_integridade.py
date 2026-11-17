"""CT10 — Persistência e integridade (RNF02), conforme a aba Testes da MRB.

Diferente da R1, as exclusões com vínculo são feitas pela tela: pessoa, categoria
e objeto referenciados por empréstimos ou objetos cadastrados nesta release.
"""

import sqlite3
from datetime import timedelta

from conftest import Tela, aplicacao_rodando, br, hoje


def cadastrar_pela_tela(tela):
    tela.abrir("pessoas", acao="incluir")
    tela.preencher("nome", "Ana Souza")
    tela.clicar("salvar")
    tela.abrir("categorias", acao="incluir")
    tela.preencher("nome", "Ferramentas")
    tela.clicar("salvar")
    tela.abrir("objetos", acao="incluir")
    tela.preencher("nome", "Furadeira")
    tela.escolher("categoria", "Ferramentas (1)")
    tela.clicar("salvar")
    tela.abrir("emprestimos", acao="incluir")
    tela.escolher("pessoa", "Ana Souza (1)")
    tela.escolher("objeto", "Furadeira (1)")
    tela.preencher("previsao-devolucao", br(hoje() + timedelta(days=7)))
    tela.clicar("salvar")


def test_rnf02_dados_persistem_apos_reiniciar_o_servidor(navegador, tmp_path, request):
    banco = tmp_path / "persistencia.sqlite"
    cenario = "CT10 · RNF02 — dados persistem apos reiniciar o servidor"
    with aplicacao_rodando(banco, "servidor_ct10.log") as url:
        tela = Tela(navegador, url, cenario)
        cadastrar_pela_tela(tela)
        assert tela.mensagem() == "Empréstimo registrado com sucesso."

    # Servidor encerrado e iniciado de novo com o mesmo arquivo de banco.
    with aplicacao_rodando(banco, "servidor_ct10.log") as url:
        tela = Tela(navegador, url, cenario)
        tela.abrir("emprestimos")
        assert [(linha["pessoa"], linha["objeto"], linha["situacao"]) for linha in tela.linhas()] == [
            ("Ana Souza", "Furadeira (1)", "Aberto")]
        tela.abrir("objetos")
        assert tela.linhas()[0]["disponibilidade"] == "Emprestado"


def test_rnf02_exclusoes_com_vinculo_sao_bloqueadas_pela_tela(tela, bd):
    cadastrar_pela_tela(tela)

    tela.abrir("pessoas")
    tela.clicar_acao(1, "excluir")
    assert "possui empréstimos registrados e não pode ser excluída" in tela.mensagem_erro()

    tela.abrir("categorias")
    tela.clicar_acao(1, "excluir")
    assert "possui objetos vinculados e não pode ser excluída" in tela.mensagem_erro()

    tela.abrir("objetos")
    tela.clicar_acao(1, "excluir")
    assert "possui empréstimos registrados e não pode ser excluído" in tela.mensagem_erro()

    assert bd.consultar("SELECT (SELECT COUNT(*) FROM pessoa), (SELECT COUNT(*) FROM categoria),"
                        " (SELECT COUNT(*) FROM objeto), (SELECT COUNT(*) FROM emprestimo)") == [(1, 1, 1, 1)]


def test_rnf02_referencias_continuam_validas_apos_renomear(tela, bd):
    cadastrar_pela_tela(tela)
    tela.abrir("categorias", acao="alterar", id_=1)
    tela.preencher("nome", "Ferramentas elétricas")
    tela.clicar("salvar")
    tela.abrir("pessoas", acao="alterar", id_=1)
    tela.preencher("nome", "Ana Souza Lima")
    tela.clicar("salvar")
    tela.abrir("objetos", acao="alterar", id_=1)
    tela.preencher("nome", "Furadeira sem fio")
    tela.clicar("salvar")

    tela.abrir("objetos")
    assert tela.linhas()[0]["categoria"] == "Ferramentas elétricas"
    tela.abrir("emprestimos")
    assert [(linha["pessoa"], linha["objeto"]) for linha in tela.linhas()] == [
        ("Ana Souza Lima", "Furadeira sem fio (1)")]


ESQUEMA_DA_R2 = """
CREATE TABLE pessoa (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, contato TEXT,
                     ativo INTEGER NOT NULL DEFAULT 1);
CREATE TABLE categoria (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, nome_chave TEXT NOT NULL UNIQUE);
CREATE TABLE objeto (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     codigo TEXT NOT NULL UNIQUE CHECK (length(codigo) BETWEEN 1 AND 20),
                     nome TEXT NOT NULL, categoria_id INTEGER NOT NULL REFERENCES categoria (id) ON DELETE RESTRICT,
                     observacao TEXT, ativo INTEGER NOT NULL DEFAULT 1);
CREATE TABLE emprestimo (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         pessoa_id INTEGER NOT NULL REFERENCES pessoa (id) ON DELETE RESTRICT,
                         objeto_id INTEGER NOT NULL REFERENCES objeto (id) ON DELETE RESTRICT,
                         data_retirada TEXT NOT NULL, previsao_devolucao TEXT NOT NULL, data_devolucao TEXT,
                         observacao TEXT);
INSERT INTO pessoa (nome) VALUES ('Ana Souza');
INSERT INTO categoria (nome, nome_chave) VALUES ('Ferramentas', 'ferramentas');
INSERT INTO objeto (codigo, nome, categoria_id) VALUES ('FUR001', 'Furadeira', 1), ('ESC001', 'Escada', 1);
"""


def test_rnf02_banco_da_r2_com_codigo_e_migrado_sem_perder_dados(navegador, tmp_path):
    """O código do objeto deixou de existir na R3; bancos antigos são migrados ao abrir."""
    banco = tmp_path / "banco_da_r2.sqlite"
    with sqlite3.connect(banco) as conexao:
        conexao.executescript(ESQUEMA_DA_R2)
        conexao.execute("INSERT INTO emprestimo (pessoa_id, objeto_id, data_retirada, previsao_devolucao)"
                        " VALUES (1, 2, ?, ?)", (hoje().isoformat(), hoje().isoformat()))

    with aplicacao_rodando(banco, "servidor_ct10.log") as url:
        tela = Tela(navegador, url, "CT10 · RNF02 — banco da R2 com codigo e migrado sem perder dados")
        tela.abrir("objetos")
        assert [(linha["id"], linha["nome"], linha["disponibilidade"]) for linha in tela.linhas()] == [
            (2, "Escada", "Emprestado"), (1, "Furadeira", "Disponível")]
        tela.abrir("objetos", acao="incluir")
        tela.preencher("nome", "Furadeira")
        tela.escolher("categoria", "Ferramentas (1)")
        tela.clicar("salvar")
        assert tela.mensagem() == "Objeto cadastrado com sucesso."
        tela.abrir("emprestimos")
        assert [(linha["pessoa"], linha["objeto"]) for linha in tela.linhas()] == [("Ana Souza", "Escada (2)")]

    with sqlite3.connect(banco) as conexao:
        assert "codigo" not in [linha[1] for linha in conexao.execute("PRAGMA table_info(objeto)")]
        assert conexao.execute("SELECT id, nome FROM objeto ORDER BY id").fetchall() == [
            (1, "Furadeira"), (2, "Escada"), (3, "Furadeira")]
