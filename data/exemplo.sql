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

INSERT INTO objeto (codigo, nome, categoria_id, observacao, ativo) VALUES
    ('LIV001', 'Dom Casmurro', 1, 'Estante da sala', 1),
    ('LIV002', 'Cálculo volume 1', 1, NULL, 1),
    ('FUR001', 'Furadeira de impacto', 2, 'Maleta azul com brocas', 1),
    ('ESC001', 'Escada de 7 degraus', 2, NULL, 1),
    ('PAN001', 'Panela de pressão', 3, 'Trocar a borracha', 1),
    ('CAI001', 'Caixa de som', 4, 'Quebrada, retirada de uso', 0);

-- Datas relativas ao dia da carga: um empréstimo aberto no prazo, um aberto vencido e um devolvido.
INSERT INTO emprestimo (pessoa_id, objeto_id, data_retirada, previsao_devolucao, data_devolucao, observacao) VALUES
    (1, 3, date('now', 'localtime', '-2 days'), date('now', 'localtime', '+5 days'), NULL, 'Com maleta'),
    (2, 1, date('now', 'localtime', '-12 days'), date('now', 'localtime', '-2 days'), NULL, NULL),
    (3, 5, date('now', 'localtime', '-20 days'), date('now', 'localtime', '-15 days'),
        date('now', 'localtime', '-16 days'), 'Devolvida limpa');
