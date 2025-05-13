-- CREATE TABLE

-- Tabelle für Vokabellisten (Beispielstruktur für die VocApp)
-- CREATE TABLE list (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL
-- );

-- Tabelle für Vokabeln (Beispielstruktur für die VocApp)
-- CREATE TABLE vocab (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     word TEXT NOT NULL,
--     translation TEXT NOT NULL
-- );

-- Tabelle für das Mapping zwischen Vokabellisten und Vokabeln
-- CREATE TABLE list_vocab (
--     list_id INTEGER,
--     vocab_id INTEGER,
--     PRIMARY KEY (list_id, vocab_id),
--     FOREIGN KEY (list_id) REFERENCES list(id) ON DELETE CASCADE,
--     FOREIGN KEY (vocab_id) REFERENCES vocab(id) ON DELETE CASCADE
-- );
