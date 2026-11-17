"""CT12 — Tempo de resposta dos relatórios (RNF04), conforme a aba Testes da MRB.

Com 100 pessoas, 500 objetos e 1.000 empréstimos, mede cinco consultas de cada relatório após
uma consulta de aquecimento. Cada uma deve terminar em até 2 segundos no navegador. Os tempos
ficam em tests/selenium/saida/desempenho.txt e entram no relatório de testes.
"""

from datetime import timedelta

import pytest

from conftest import SAIDA, hoje

LIMITE_MS = 2000
CONSULTAS = [
    ("Pendências, sem filtros", "relatorios/pendencias", {}),
    ("Pendências, somente atrasados", "relatorios/pendencias", {"atrasados": "1"}),
]


@pytest.fixture
def massa_de_dados(bd):
    """100 pessoas, 500 objetos em 5 categorias, 1.000 empréstimos: 600 devolvidos e 400 abertos."""
    h = hoje()
    for n in range(5):
        bd.criar_categoria(f"Categoria {n + 1}")
    bd.executar_varios("INSERT INTO pessoa (nome) VALUES (?)", [(f"Pessoa {n:03d}",) for n in range(1, 101)])
    bd.executar_varios("INSERT INTO objeto (nome, categoria_id) VALUES (?, ?)",
                       [(f"Objeto {n:03d}", n % 5 + 1) for n in range(1, 501)])
    emprestimos = []
    for n in range(1000):
        objeto = n % 500 + 1
        retirada = h - timedelta(days=60 - n % 50)
        aberto = n >= 600 and objeto > 100  # um empréstimo aberto por objeto, nos objetos 101 a 500
        previsao = retirada + timedelta(days=n % 70)
        devolucao = None if aberto else retirada + timedelta(days=1)
        emprestimos.append((n % 100 + 1, objeto, retirada.isoformat(), previsao.isoformat(),
                            devolucao.isoformat() if devolucao else None))
    bd.executar_varios("INSERT INTO emprestimo (pessoa_id, objeto_id, data_retirada, previsao_devolucao,"
                       " data_devolucao) VALUES (?, ?, ?, ?, ?)", emprestimos)
    assert bd.consultar("SELECT (SELECT COUNT(*) FROM pessoa), (SELECT COUNT(*) FROM objeto),"
                        " (SELECT COUNT(*) FROM emprestimo)") == [(100, 500, 1000)]


def tempo_da_pagina_ms(tela) -> float:
    return tela.driver.execute_script("return performance.getEntriesByType('navigation')[0].duration;")


def test_rnf04_relatorios_respondem_em_ate_2_segundos(tela, massa_de_dados):
    linhas = [f"Massa: 100 pessoas, 500 objetos e 1.000 empréstimos. Limite: {LIMITE_MS} ms por consulta."]
    for descricao, pagina, filtros in CONSULTAS:
        tela.abrir(pagina, **filtros)  # aquecimento
        assert tela.existe("total"), f"{pagina} não exibiu o relatório"
        tempos = []
        for _ in range(5):
            tela.abrir(pagina, **filtros)
            assert tela.existe("lista")
            tempos.append(tempo_da_pagina_ms(tela))
        linhas.append(f"{descricao}: " + ", ".join(f"{t:.0f}" for t in tempos) + f" ms (máximo {max(tempos):.0f} ms)")
        assert max(tempos) <= LIMITE_MS, (descricao, tempos)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "desempenho.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
