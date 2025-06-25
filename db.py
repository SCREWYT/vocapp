import sqlite3
from flask import g, current_app
import os

def get_db():
    """
    Stellt eine Verbindung zur SQLite-Datenbank her.
    Die Verbindung wird im 'g' Objekt gespeichert (global für die aktuelle App-Request).
    Die Datei wird im Flask-Standardordner 'instance/' gespeichert.
    """
    if 'db' not in g:
        # Pfad zur Datenbank im instance-Verzeichnis
        db_path = os.path.join(current_app.instance_path, 'database.db')

        # Stelle sicher, dass der Ordner existiert
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Verbindung zur SQLite-Datenbank aufbauen und im 'g' Objekt speichern
        g.db = sqlite3.connect(db_path)
        # Rückgabe von Ergebnissen als Dictionary (für lesbaren Zugriff auf Spaltennamen)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Schließt die Datenbankverbindung am Ende des Requests.
    Wird z. B. beim App-Teardown automatisch aufgerufen.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """
    Initialisiert die Datenbankstruktur:
    Erstellt die Tabellen 'users', 'sets' und 'flashcards', falls sie noch nicht existieren.
    Diese Funktion wird z. B. beim Start über 'flask init-db' aufgerufen.
    """
    db = get_db()
    cursor = db.cursor()

    # Tabelle für Benutzer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')

    # Neue Tabelle: Karteikartensets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Erweiterte flashcards-Tabelle: Zuordnung zu Sets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,                     -- Fremdschlüssel zur Zuordnung der Karte zum User
            set_id INTEGER NOT NULL,                      -- Fremdschlüssel zur Zuordnung der Karte zu einem Set
            question TEXT NOT NULL,                       -- Vorderseite der Karte (Frage)
            answer TEXT NOT NULL,                         -- Rückseite der Karte (Antwort)
            box INTEGER DEFAULT 1,                        -- Spaced Repetition Box (1 = neu, 2 = mittel, 3 = sicher)
            last_reviewed DATE,                           -- Letztes Abfragedatum (optional verwendbar)
            FOREIGN KEY (user_id) REFERENCES users(id),  -- Fremdschlüssel-Verknüpfung zum User
            FOREIGN KEY (set_id) REFERENCES sets(id)     -- Fremdschlüssel-Verknüpfung zum Set
        )
    ''')

    db.commit()

# Beispielnutzung: >>> from db import init_db; init_db()
