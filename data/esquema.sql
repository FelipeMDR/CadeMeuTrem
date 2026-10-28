-- Cadê Meu Trem? — esquema do banco SQLite (RNF02).
-- Executado a cada conexão; IF NOT EXISTS mantém os dados existentes.
-- As tabelas objeto e emprestimo já existem na R1 para que as exclusões de
-- pessoa (RFS04) e categoria (RFS08) verifiquem vínculos. Suas telas chegam na R2.

CREATE TABLE IF NOT EXISTS pessoa (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome    TEXT    NOT NULL CHECK (length(trim(nome)) BETWEEN 1 AND 80),
    contato TEXT             CHECK (contato IS NULL OR length(contato) <= 80),
    ativo   INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS categoria (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL CHECK (length(trim(nome)) BETWEEN 1 AND 40),
    -- Nome sem espaços nas extremidades e em minúsculas: garante a unicidade de RFS05.
    nome_chave TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS objeto (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo       TEXT    NOT NULL UNIQUE CHECK (length(codigo) BETWEEN 1 AND 20),
    nome         TEXT    NOT NULL CHECK (length(trim(nome)) BETWEEN 1 AND 80),
    categoria_id INTEGER NOT NULL REFERENCES categoria (id) ON DELETE RESTRICT,
    observacao   TEXT             CHECK (observacao IS NULL OR length(observacao) <= 250),
    ativo        INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS emprestimo (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    pessoa_id          INTEGER NOT NULL REFERENCES pessoa (id) ON DELETE RESTRICT,
    objeto_id          INTEGER NOT NULL REFERENCES objeto (id) ON DELETE RESTRICT,
    data_retirada      TEXT    NOT NULL,  -- AAAA-MM-DD
    previsao_devolucao TEXT    NOT NULL,
    data_devolucao     TEXT,
    observacao         TEXT    CHECK (observacao IS NULL OR length(observacao) <= 250),
    CHECK (previsao_devolucao >= data_retirada),
    CHECK (data_devolucao IS NULL OR data_devolucao >= data_retirada)
);

-- Um objeto pode ter somente um empréstimo aberto (RFS13 e RNF02).
CREATE UNIQUE INDEX IF NOT EXISTS emprestimo_um_aberto_por_objeto
    ON emprestimo (objeto_id) WHERE data_devolucao IS NULL;
