import sqlite3
from flask import g
import os

# Name der SQLite-Datenbankdatei
DATABASE = os.path.join(os.getcwd(), 'database.db')

def get_db():
    """
    Stellt eine Verbindung zur SQLite-Datenbank her.
    Die Verbindung wird im 'g' Objekt gespeichert (global für die aktuelle App-Request).
    """
    if 'db' not in g:
        # Verbindung zur SQLite-Datenbank aufbauen und im 'g' Objekt speichern
        g.db = sqlite3.connect(DATABASE)
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
    Erstellt die Tabellen 'users' und 'flashcards', falls sie noch nicht existieren.
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

    # Tabelle für Karteikarten
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,                     -- Fremdschlüssel zur Zuordnung der Karte zum User
            question TEXT NOT NULL,                       -- Vorderseite der Karte (Frage)
            answer TEXT NOT NULL,                         -- Rückseite der Karte (Antwort)
            box INTEGER DEFAULT 1,                        -- Spaced Repetition Box (1 = neu, 2 = mittel, 3 = sicher)
            last_reviewed DATE,                           -- Letztes Abfragedatum (optional verwendbar)
            FOREIGN KEY (user_id) REFERENCES users(id)    -- Fremdschlüssel-Verknüpfung
        )
    ''')

    db.commit()

# Beispielnutzung: >>> from db import init_db; init_db()
