-- ============================================================================
-- MenHelpHer ODS 5 - Esquema físico do banco de dados (SGBD: SQLite 3)
-- Projeto Integrado Transdisciplinar (PIT I / PIT II) - Engenharia de Software
-- Autor: Julio Costa
--
-- O DDL usa apenas construções SQL padrão (tipos básicos, PK/FK, CHECK,
-- UNIQUE), o que facilita a migração futura para PostgreSQL ou MySQL:
--   * INTEGER PRIMARY KEY AUTOINCREMENT  ->  GENERATED ... AS IDENTITY / AUTO_INCREMENT
--   * TEXT                               ->  VARCHAR(n) / TEXT
-- Modelo normalizado (3FN): tabelas de domínio (papel, tipo_compromisso,
-- perfil_avaliador) referenciadas por chave estrangeira.
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- Domínios --
CREATE TABLE IF NOT EXISTS papel (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tipo_compromisso (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo  TEXT NOT NULL UNIQUE,   -- valor enviado pelo formulário
    rotulo  TEXT NOT NULL           -- texto curto exibido no cartão do mural
);

CREATE TABLE IF NOT EXISTS perfil_avaliador (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL UNIQUE
);

-- ---------------------------------------------------------------- Entidades --
CREATE TABLE IF NOT EXISTS compromisso (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT    NOT NULL CHECK (length(nome) BETWEEN 2 AND 80),
    papel_id  INTEGER NOT NULL REFERENCES papel (id),
    tipo_id   INTEGER NOT NULL REFERENCES tipo_compromisso (id),
    mensagem  TEXT    NOT NULL CHECK (length(mensagem) BETWEEN 10 AND 500),
    apoios    INTEGER NOT NULL DEFAULT 0 CHECK (apoios >= 0),
    criado_em TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS avaliacao (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    perfil_id           INTEGER NOT NULL REFERENCES perfil_avaliador (id),
    clareza             INTEGER NOT NULL CHECK (clareza BETWEEN 1 AND 5),
    aprendizado_vieses  INTEGER NOT NULL CHECK (aprendizado_vieses BETWEEN 1 AND 5),
    relevancia_ods5     INTEGER NOT NULL CHECK (relevancia_ods5 BETWEEN 1 AND 5),
    comentario          TEXT    NOT NULL DEFAULT '' CHECK (length(comentario) <= 500),
    criado_em           TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------------ Índices --
CREATE INDEX IF NOT EXISTS idx_compromisso_papel  ON compromisso (papel_id);
CREATE INDEX IF NOT EXISTS idx_compromisso_data   ON compromisso (criado_em DESC);
CREATE INDEX IF NOT EXISTS idx_avaliacao_perfil   ON avaliacao (perfil_id);
