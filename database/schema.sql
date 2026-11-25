-- =====================================================================
-- Cadastro de Papéis de Parede — esquema do banco (SQLite)
-- Relacionamentos:
--   categoria 1 --- N wallpaper         (cada wallpaper tem UMA categoria)
--   wallpaper N --- N tag               (via tabela associativa wallpaper_tag)
-- =====================================================================
PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS vw_wallpaper_completo;
DROP TABLE IF EXISTS wallpaper_tag;
DROP TABLE IF EXISTS wallpaper;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS categoria;

CREATE TABLE categoria (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT    NOT NULL UNIQUE CHECK (length(nome) BETWEEN 1 AND 40),
    descricao      TEXT    NOT NULL DEFAULT '' CHECK (length(descricao) <= 200),
    data_cadastro  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE wallpaper (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo         TEXT    NOT NULL CHECK (length(titulo) BETWEEN 1 AND 80),
    descricao      TEXT    NOT NULL DEFAULT '' CHECK (length(descricao) <= 300),
    arquivo        TEXT    NOT NULL,
    largura        INTEGER NOT NULL CHECK (largura > 0),
    altura         INTEGER NOT NULL CHECK (altura > 0),
    autor          TEXT    NOT NULL DEFAULT '' CHECK (length(autor) <= 60),
    favorito       INTEGER NOT NULL DEFAULT 0 CHECK (favorito IN (0, 1)),
    categoria_id   INTEGER NOT NULL,
    data_cadastro  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (categoria_id) REFERENCES categoria (id) ON DELETE RESTRICT
);

CREATE TABLE tag (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL UNIQUE CHECK (length(nome) BETWEEN 1 AND 20)
);

CREATE TABLE wallpaper_tag (
    wallpaper_id  INTEGER NOT NULL,
    tag_id        INTEGER NOT NULL,
    PRIMARY KEY (wallpaper_id, tag_id),
    FOREIGN KEY (wallpaper_id) REFERENCES wallpaper (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)       REFERENCES tag (id)       ON DELETE CASCADE
);

CREATE INDEX idx_wallpaper_categoria ON wallpaper (categoria_id);
CREATE INDEX idx_wallpaper_tag_tag   ON wallpaper_tag (tag_id);

-- Visão usada pela galeria: junta a categoria e calcula a orientação.
CREATE VIEW vw_wallpaper_completo AS
SELECT  w.*,
        c.nome AS categoria_nome,
        CASE
            WHEN w.largura > w.altura THEN 'Paisagem'
            WHEN w.largura < w.altura THEN 'Retrato'
            ELSE 'Quadrado'
        END AS orientacao
FROM wallpaper w
JOIN categoria c ON c.id = w.categoria_id;
