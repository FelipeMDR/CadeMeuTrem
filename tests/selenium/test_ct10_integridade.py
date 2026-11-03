"""CT10 — Persistência e integridade (RNF02), conforme a aba Testes da MRB.

Diferente da R1, as exclusões com vínculo são feitas pela tela: pessoa, categoria
e objeto referenciados por empréstimos ou objetos cadastrados nesta release.
"""

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
    tela.preencher("codigo", "FUR001")
    tela.preencher("nome", "Furadeira")
    tela.escolher("categoria", "Ferramentas (1)")
    tela.clicar("salvar")
    tela.abrir("emprestimos", acao="incluir")
    tela.escolher("pessoa", "Ana Souza (1)")
    tela.escolher("objeto", "FUR001 – Furadeira")
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
        assert [(linha["pessoa"], linha["codigo"], linha["situacao"]) for linha in tela.linhas()] == [
            ("Ana Souza", "FUR001", "Aberto")]
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
    tela.preencher("codigo", "FUR100")
    tela.clicar("salvar")

    tela.abrir("objetos")
    assert tela.linhas()[0]["categoria"] == "Ferramentas elétricas"
    tela.abrir("emprestimos")
    assert [(linha["pessoa"], linha["codigo"]) for linha in tela.linhas()] == [("Ana Souza Lima", "FUR100")]
