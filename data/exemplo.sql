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
