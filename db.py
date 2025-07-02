# Quelle: https://www.youtube.com/watch?v=IBgWKTaG_Bs

import sqlite3                    
from flask import g, current_app  # 'g' = globale Variable pro Anfrage,
import os                         # Modul zur Arbeit mit Dateien und Verzeichnissen


def get_db():
    """
    Verbindung zur SQLite-Datenbank.
    Verbindung wird im 'g' Objekt gespeichert, damit sie während einer einzelnen Anfrage
    mehrfach genutzt werden kann, ohne sie erneut zu öffnen.
    """

    if 'db' not in g:
        db_path = os.path.join(current_app.instance_path, 'database.db')

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        g.db = sqlite3.connect(db_path)

        # Zeile wird nicht als Tupel sondern wie in einem Dictionary gespeichert, so kann man mit "rows" arbeiten (z. B. row ['password'])
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Schließt Datenbankverbindung nach jedem Requests.
    """

    # Entferne ggf. die Verbindung aus 'g' und speichere sie in 'db'. Wenn nichts existiert dann "None" und kein Fehler
    db = g.pop('db', None)

    # Wenn tatsächlich eine Verbindung bestand, schließe sie
    if db is not None:
        db.close()


def init_db():
    """
    Wird über den Befehl `flask init-db` ausgeführt.
    """

    db = get_db()         
    cursor = db.cursor()  

    # -------------------------------------------------------
    # Tabelle: Benutzerkonten
    # -------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   
            username TEXT NOT NULL UNIQUE,          
            password TEXT NOT NULL,                 -- gehashed
            role TEXT DEFAULT 'user'                -- Benutzerrolle (Standard: "user")
        )
    ''')

    # -------------------------------------------------------
    # Tabelle: Karteikartensets
    # -------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   
            user_id INTEGER NOT NULL,               
            name TEXT NOT NULL,                     
            FOREIGN KEY (user_id) REFERENCES users(id)  
        )
    ''')

    # -------------------------------------------------------
    # Tabelle: Karteikarten (Vokabeln)
    # -------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   
            user_id INTEGER NOT NULL,              
            set_id INTEGER NOT NULL,                
            question TEXT NOT NULL,                 -- Vorderseite der Karte
            answer TEXT NOT NULL,                   -- Rückseite der Karte
            box INTEGER DEFAULT 1,                  -- Lernbox (für Spaced Repetition)
            last_reviewed DATE,                     -- Datum der letzten Wiederholung
            FOREIGN KEY (user_id) REFERENCES users(id),  
            FOREIGN KEY (set_id) REFERENCES sets(id)     
        )
    ''')

    # Änderungen in der Datenbank dauerhaft speichern
    db.commit()
