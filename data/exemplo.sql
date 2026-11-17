-- Dados de demonstração fictícios (RNF05). Carregados por scripts/carregar_exemplo.py.

INSERT INTO pessoa (nome, contato, ativo) VALUES
    ('Ana Beatriz Lima', 'ana.lima@exemplo.com', 1),
    ('Bruno Carvalho', '(35) 90000-0001', 1),
    ('Carla Mendes', NULL, 1),
    ('Diego Rocha', 'Quarto 3', 0);

INSERT INTO categoria (nome, nome_chave) VALUES
    ('Livros', 'livros'),
    ('Ferramentas', 'ferramentas'),
    ('Cozinha', 'cozinha'),
    ('Eletrônicos', 'eletrônicos');

INSERT INTO objeto (nome, categoria_id, observacao, ativo) VALUES
    ('Dom Casmurro', 1, 'Estante da sala', 1),
    ('Cálculo volume 1', 1, NULL, 1),
    ('Furadeira de impacto', 2, 'Maleta azul com brocas', 1),
    ('Escada de 7 degraus', 2, NULL, 1),
    ('Panela de pressão', 3, 'Trocar a borracha', 1),
    ('Caixa de som', 4, 'Quebrada, retirada de uso', 0);

-- Datas relativas ao dia da carga: um empréstimo aberto no prazo, um aberto vencido e três devolvidos,
-- dois deles no mês anterior, para o histórico.
INSERT INTO emprestimo (pessoa_id, objeto_id, data_retirada, previsao_devolucao, data_devolucao, observacao) VALUES
    (1, 3, date('now', 'localtime', '-2 days'), date('now', 'localtime', '+5 days'), NULL, 'Com maleta'),
    (2, 1, date('now', 'localtime', '-12 days'), date('now', 'localtime', '-2 days'), NULL, NULL),
    (3, 5, date('now', 'localtime', '-20 days'), date('now', 'localtime', '-15 days'),
        date('now', 'localtime', '-16 days'), 'Devolvida limpa'),
    (4, 4, date('now', 'localtime', '-40 days'), date('now', 'localtime', '-33 days'),
        date('now', 'localtime', '-34 days'), 'Antes de Diego ser inativado'),
    (1, 2, date('now', 'localtime', '-35 days'), date('now', 'localtime', '-28 days'),
        date('now', 'localtime', '-30 days'), NULL);
