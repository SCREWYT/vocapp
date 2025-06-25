from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db, close_db, init_db
import random




# Quellen: Von Commit: "Move database.db to instance folder and update app.py to follow Flask best practices" am 24. Juni bis 
# Commit: "Fix error on dashboard by adding card ID to query" am 25. Juni nur dieser Chat hier: https://chatgpt.com/share/685bd087-d1f4-800b-825f-d8f7ec1b94e3
# Name des Chats: Flask Login Struktur Aufbau




app = Flask(__name__)
app.secret_key = 'geheimer_schluessel'  # WICHTIG: In der Produktion durch sicheren Wert ersetzen

# Datenbankverbindung nach jedem Request sauber schließen
app.teardown_appcontext(close_db)

# ----------------------------------
# OPTIONAL: Initialisierung der DB
# Nur einmal bei Projektstart nötig
# ----------------------------------
@app.cli.command("init-db")
def initialize_database():
    """
    Führt die init_db()-Funktion aus, um die Datenbank zu erstellen.
    Aufrufbar über Terminal: flask init-db
    """
    init_db()
    print("Datenbank erfolgreich initialisiert.")

# ----------------------------------
# Startseite – leitet ggf. weiter
# ----------------------------------
@app.route('/')
def index():
    """
    Weiterleitung von der Startseite direkt zur Login-Seite.
    """
    return redirect(url_for('login'))


# ----------------------------------
# Registrierung
# ----------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route zur Benutzerregistrierung.
    GET: Zeigt Registrierungsformular.
    POST: Prüft Eingaben, speichert neuen Nutzer mit gehashtem Passwort.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Prüfen, ob der Benutzername bereits existiert
        existing = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Benutzername bereits vergeben.')
            return redirect(url_for('register'))

        # Passwort sicher hashen und speichern
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        db.commit()

        flash('Registrierung erfolgreich. Du kannst dich jetzt einloggen.')
        return redirect(url_for('login'))

    return render_template('register.html')

# ----------------------------------
# Login
# ----------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route zum Login.
    GET: Zeigt Login-Formular.
    POST: Prüft Anmeldedaten, legt Session an.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            # Session starten
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login erfolgreich.')
            return redirect(url_for('dashboard'))
        else:
            flash('Ungültiger Benutzername oder Passwort.')

    return render_template('login.html')

# ----------------------------------
# Logout
# ----------------------------------
@app.route('/logout')
def logout():
    """
    Beendet die aktuelle Session.
    """
    session.clear()
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('index'))

# ----------------------------------
# Dashboard (nur eingeloggt)
# ----------------------------------
@app.route('/dashboard')
def dashboard():
    """
    Geschützter Bereich. Zeigt alle Karteikarten des eingeloggten Nutzers.
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein, um fortzufahren.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    # Jetzt wird die ID mitgeladen
    rows = db.execute(
        'SELECT id, question, answer FROM flashcards WHERE user_id = ?',
        (user_id,)
    ).fetchall()

    # Wandelt sqlite3.Row-Objekte in echte Dictionaries um (damit card['id'] funktioniert)
    flashcards = [dict(row) for row in rows]

    return render_template('dashboard.html', username=session.get('username'), flashcards=flashcards)


# ----------------------------------
# Karteikarte bearbeiten (nur eigene)
# ----------------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_flashcard(id):
    """
    Bearbeiten einer bestehenden Karteikarte.
    Nur möglich, wenn sie dem eingeloggten Nutzer gehört.
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    # Karte laden und prüfen, ob sie dem Nutzer gehört
    card = db.execute(
        'SELECT * FROM flashcards WHERE id = ? AND user_id = ?',
        (id, user_id)
    ).fetchone()

    if card is None:
        flash('Karte nicht gefunden oder kein Zugriff.')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']

        # Karte aktualisieren
        db.execute(
            'UPDATE flashcards SET question = ?, answer = ? WHERE id = ?',
            (question, answer, id)
        )
        db.commit()

        flash('Karte erfolgreich aktualisiert.')
        return redirect(url_for('dashboard'))

    return render_template('edit_flashcard.html', card=card)

# ----------------------------------
# Karteikarte löschen (nur eigene)
# ----------------------------------
@app.route('/delete/<int:id>', methods=['POST'])
def delete_flashcard(id):
    """
    Löscht eine Karteikarte, wenn sie dem eingeloggten Nutzer gehört.
    Nur per POST-Aufruf erlaubt.
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    # Karte nur löschen, wenn sie dem Nutzer gehört
    db.execute('DELETE FROM flashcards WHERE id = ? AND user_id = ?', (id, user_id))
    db.commit()

    flash('Karte wurde gelöscht.')
    return redirect(url_for('dashboard'))

# ----------------------------------
# Neue Karteikarte erstellen
# ----------------------------------
@app.route('/add', methods=['GET', 'POST'])
def add_flashcard():
    """
    Route zum Erstellen einer neuen Karteikarte.
    Nur für eingeloggte Nutzer zugänglich.
    GET: Zeigt das Formular.
    POST: Speichert die neue Karte in der Datenbank.
    """
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um Karteikarten zu erstellen.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        user_id = session['user_id']

        db = get_db()
        cursor = db.cursor()

        # Neue Karteikarte einfügen
        cursor.execute(
            'INSERT INTO flashcards (user_id, question, answer) VALUES (?, ?, ?)',
            (user_id, question, answer)
        )
        db.commit()

        flash('Karteikarte erfolgreich gespeichert.')
        return redirect(url_for('dashboard'))

    return render_template('add_flashcard.html')

# ---------------------------------------------
# Spaced Repetition Lernmodus (Learn Route)
# ---------------------------------------------
@app.route('/learn', methods=['GET', 'POST'])
def learn():
    """
    Lernfunktion mit Antwortanzeige per Button.
    Zwei Zustände:
    - GET oder show_answer: zeigt Frage (+ optional Antwort)
    - POST mit Ergebnis: aktualisiert Box und lädt nächste Karte
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    # POST: Ergebnis auswerten (gewusst / nicht gewusst)
    if request.method == 'POST':
        if 'result' in request.form:
            card_id = int(request.form['card_id'])
            result = request.form['result']

            card = db.execute(
                'SELECT box FROM flashcards WHERE id = ? AND user_id = ?',
                (card_id, user_id)
            ).fetchone()

            if card:
                current_box = card['box']
                new_box = min(current_box + 1, 3) if result == 'correct' else 1

                db.execute(
                    'UPDATE flashcards SET box = ?, last_reviewed = DATE("now") WHERE id = ? AND user_id = ?',
                    (new_box, card_id, user_id)
                )
                db.commit()

            return redirect(url_for('learn'))

        elif 'show_answer' in request.form:
            # Antwort anzeigen – Karte erneut laden
            card_id = int(request.form['card_id'])
            card = db.execute(
                'SELECT * FROM flashcards WHERE id = ? AND user_id = ?',
                (card_id, user_id)
            ).fetchone()

            if card:
                return render_template('learn.html', card=card, reveal=True)

    # GET: Neue Karte ziehen
    for box in [1, 2, 3]:
        cards = db.execute(
            'SELECT * FROM flashcards WHERE user_id = ? AND box = ?',
            (user_id, box)
        ).fetchall()

        if cards:
            card = random.choice(cards)
            return render_template('learn.html', card=card, reveal=False)

    flash('Keine Karteikarten zum Lernen verfügbar.')
    return redirect(url_for('dashboard'))

# ------------------
# Set-Übersicht
# ------------------

@app.route('/sets', methods=['GET', 'POST'])
def sets_overview():
    """
    Übersichtsseite für Karteikartensets.
    GET: Zeigt alle Sets des Users an.
    POST: Fügt ein neues Set hinzu.
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    if request.method == 'POST':
        # Neues Set anlegen
        set_name = request.form.get('set_name', '').strip()
        if not set_name:
            flash('Der Name des Sets darf nicht leer sein.')
            return redirect(url_for('sets_overview'))

        # Prüfen, ob Setname bereits existiert
        exists = db.execute(
            'SELECT id FROM sets WHERE user_id = ? AND name = ?',
            (user_id, set_name)
        ).fetchone()

        if exists:
            flash('Du hast bereits ein Set mit diesem Namen.')
            return redirect(url_for('sets_overview'))

        # Neues Set speichern
        db.execute(
            'INSERT INTO sets (user_id, name) VALUES (?, ?)',
            (user_id, set_name)
        )
        db.commit()
        flash(f'Set "{set_name}" wurde angelegt.')
        return redirect(url_for('sets_overview'))

    # GET: Alle Sets abrufen
    sets = db.execute(
        'SELECT id, name FROM sets WHERE user_id = ? ORDER BY name',
        (user_id,)
    ).fetchall()

    return render_template('sets_overview.html', sets=sets)


# -----------------------------
# Manage Sets ( Erstmal nur Platzhalter )
# -----------------------------

@app.route('/sets/<int:set_id>', methods=['GET', 'POST'])
def manage_set(set_id):
    """
    Verwaltung der Karteikarten innerhalb eines Sets.
    GET: Zeigt alle Karten im Set und ein Formular zum Hinzufügen.
    POST: Fügt eine neue Karte zum Set hinzu.
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    # Prüfen, ob das Set dem eingeloggten Nutzer gehört
    set_obj = db.execute(
        'SELECT id, name FROM sets WHERE id = ? AND user_id = ?',
        (set_id, user_id)
    ).fetchone()

    if not set_obj:
        flash('Set nicht gefunden oder kein Zugriff.')
        return redirect(url_for('sets_overview'))

    if request.method == 'POST':
        # Neue Karteikarte hinzufügen
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()

        if not question or not answer:
            flash('Frage und Antwort dürfen nicht leer sein.')
            return redirect(url_for('manage_set', set_id=set_id))

        db.execute(
            '''
            INSERT INTO flashcards (user_id, set_id, question, answer)
            VALUES (?, ?, ?, ?)
            ''',
            (user_id, set_id, question, answer)
        )
        db.commit()
        flash('Karteikarte erfolgreich hinzugefügt.')
        return redirect(url_for('manage_set', set_id=set_id))

    # GET: Alle Karten des Sets abfragen
    flashcards = db.execute(
        'SELECT id, question, answer FROM flashcards WHERE user_id = ? AND set_id = ? ORDER BY id DESC',
        (user_id, set_id)
    ).fetchall()

    return render_template('manage_set.html', set_obj=set_obj, flashcards=flashcards)


# -----------------------------
# App starten (nur lokal)
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
