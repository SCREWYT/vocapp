# Optimized with ChatGPT Chat 
# https://chatgpt.com/share/685bd087-d1f4-800b-825f-d8f7ec1b94e3 

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# render_template = HTML-Dateien laden und anzeigen
# request = Zugriff auf Formulardaten (z. B. GET/POST)
# redirect = Weiterleitung zu anderer Route
# url_for = URL aus Funktionsnamen erstellen (z. B. url_for('login') → "/login")
# session = Daten zwischen Seitenaufrufen speichern für Nutzer (z. B. user_id)
# flash = Kurzmeldungen anzeigen (z. B. "Erfolgreich registriert")

from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash = verschlüsselt ein Passwort (nicht im Klartext speichern)
# check_password_hash = prüft, ob ein eingegebenes Passwort zur verschlüsselten Version passt

from db import get_db, close_db, init_db
import random

app = Flask(__name__)
app.secret_key = 'geheimer_schluessel'  # In echter App sollte der Geheim sein

# Flask schließt DB Verbindung nach jedem Request (teardown)
app.teardown_appcontext(close_db)

# ----------------------------------
# Initialisierung der DB
# ----------------------------------
@app.cli.command("init-db") # Ein Command nur für das Terminal
def initialize_database():
    """
    Führt init_db() aus, um die Datenbank zu erstellen.
    Aufrufbar im Terminal mit: flask init-db
    """
    init_db()
    print("Datenbank erfolgreich initialisiert.")

# ----------------------------------
# Startseite: Weiterleitung zur Login-Seite. Erfolgt automatisch durch Flask
# ----------------------------------
@app.route('/') # Root
def index():
    return redirect(url_for('login'))

# ----------------------------------
# Registrierung
# ----------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: Zeigt das Registrierungsformular.
    POST: Speichert den neuen Nutzer und legt das Standard-Set mit Karten an.
    """
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Passwörter vergleichen
        if password != password_confirm:
            flash('Die Passwörter stimmen nicht überein.')
            return redirect(url_for('register'))

        db = get_db()
        cursor = db.cursor()

        # Prüfen, ob der Benutzername bereits existiert
        existing = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Benutzername bereits vergeben.')
            return redirect(url_for('register'))

        # Passwort hashen und neuen Nutzer speichern
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        db.commit()

        # User-ID des neu angelegten Nutzers holen
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()['id']

        # Standard-Karteikartenset mit Beispielvokabeln anlegen
        create_default_english_set(user_id)

        flash('Registrierung erfolgreich. Du kannst dich jetzt einloggen.')
        return redirect(url_for('login'))

    # Bei GET Anfrage Registrierungsformular anzeigen
    return render_template('register.html')

# ----------------------------------
# Standard-Englischset
# ----------------------------------
def create_default_english_set(user_id):
    db = get_db()

    # Erstellt ein neues Set für den Nutzer
    db.execute('INSERT INTO sets (user_id, name) VALUES (?, ?)', (user_id, 'Englisch Basiswortschatz'))
    db.commit()

    # Hole die ID des gerade erstellten Sets
    set_id = db.execute(
        'SELECT id FROM sets WHERE user_id = ? AND name = ?',
        (user_id, 'Englisch Basiswortschatz')
    ).fetchone()['id']

    # Beispiel-Vokabelliste mit 10 Paaren
    vocab_list = [
        ('hello', 'hallo'),
        ('world', 'Welt'),
        ('book', 'Buch'),
        ('car', 'Auto'),
        ('tree', 'Baum'),
        ('water', 'Wasser'),
        ('house', 'Haus'),
        ('dog', 'Hund'),
        ('cat', 'Katze'),
        ('food', 'Essen')
    ]

    # Karten in die DB einfügen
    for question, answer in vocab_list:
        db.execute(
            'INSERT INTO flashcards (user_id, set_id, question, answer) VALUES (?, ?, ?, ?)',
            (user_id, set_id, question, answer)
        )
    db.commit()


# ----------------------------------
# Login
# ----------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
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
    session.clear()
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('index'))

# ----------------------------------
# Dashboard
# ----------------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Bitte logge dich ein, um fortzufahren.')
        return redirect(url_for('login'))

    return render_template('dashboard.html')

# ----------------------------------
# Sets Übersicht / Anlegen
# ----------------------------------
@app.route('/sets', methods=['GET', 'POST'])
def sets_overview():
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    if request.method == 'POST':
        set_name = request.form.get('set_name', '').strip()
        if not set_name:
            flash('Der Name des Sets darf nicht leer sein.')
            return redirect(url_for('sets_overview')) # Sonst kommt immer dieses: "Möchten Sie das Formular neu laden?"

        exists = db.execute('SELECT id FROM sets WHERE user_id = ? AND name = ?', (user_id, set_name)).fetchone()
        if exists:
            flash('Du hast bereits ein Set mit diesem Namen.')
            return redirect(url_for('sets_overview'))

        db.execute('INSERT INTO sets (user_id, name) VALUES (?, ?)', (user_id, set_name))
        db.commit()
        flash(f'Set "{set_name}" wurde angelegt.')
        return redirect(url_for('sets_overview'))

    sets = db.execute('SELECT id, name FROM sets WHERE user_id = ? ORDER BY name', (user_id,)).fetchall() # Gibt alle Sets, die existieren
    return render_template('sets_overview.html', sets=sets) # Zusätzlich wird die Variable "sets" ans Template weitergegeben

# ----------------------------------
# Verwaltung der Karteikarten im Set
# ----------------------------------
@app.route('/sets/<int:set_id>', methods=['GET', 'POST'])
def manage_set(set_id):
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id'] # Flask verwendet sogenannte "Secure Cookies" , die im Browser die "Sessions" speichern

    set_obj = db.execute('SELECT id, name FROM sets WHERE id = ? AND user_id = ?', (set_id, user_id)).fetchone() # Holt Set
    if not set_obj:
        flash('Set nicht gefunden oder kein Zugriff.')
        return redirect(url_for('sets_overview'))

    if request.method == 'POST': # Neue Karte
        question = request.form.get('question', '').strip() 
        answer = request.form.get('answer', '').strip()

        if not question or not answer:
            flash('Felder dürfen nicht leer sein.')
            return redirect(url_for('manage_set', set_id=set_id))

        db.execute(
            'INSERT INTO flashcards (user_id, set_id, question, answer) VALUES (?, ?, ?, ?)',
            (user_id, set_id, question, answer)
        )
        db.commit()
        flash('Karteikarte erfolgreich hinzugefügt.')
        return redirect(url_for('manage_set', set_id=set_id))

    flashcards = db.execute( # Holt alle Karten, um sie dann anzeigen zu können
        'SELECT id, question, answer FROM flashcards WHERE user_id = ? AND set_id = ? ORDER BY id DESC',
        (user_id, set_id)
    ).fetchall()

    return render_template('manage_set.html', set_obj=set_obj, flashcards=flashcards)

# ----------------------------------
# Karte bearbeiten
# ----------------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_flashcard(id):
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    # Karte abfragen
    card = db.execute('SELECT * FROM flashcards WHERE id = ? AND user_id = ?', (id, user_id)).fetchone()

    # Falls Karte nicht existiert oder fremd ist
    if not card:
        flash('Karte nicht gefunden oder kein Zugriff.')
        return redirect(url_for('dashboard'))  # In diesem Beispiel gibts ja auch keine set_id, deshalb schickts einen sicherheitshalber zurück zum Dashboard 

    set_id = card['set_id']  # Mit der ID finden wir dann zurück zum richtigen Set

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']

        db.execute('UPDATE flashcards SET question = ?, answer = ? WHERE id = ?', (question, answer, id))
        db.commit()

        flash('Karte erfolgreich aktualisiert.')
        return redirect(url_for('manage_set', set_id=set_id))

    return render_template('edit_flashcard.html', card=card)

# ----------------------------------
# Karte löschen
# ----------------------------------
@app.route('/delete/<int:id>', methods=['POST'])
def delete_flashcard(id):
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    # set_id zuerst aus der Datenbank holen
    set_id_row = db.execute(
        'SELECT set_id FROM flashcards WHERE id = ? AND user_id = ?', 
        (id, user_id)
    ).fetchone()

    if not set_id_row:
        flash('Karte nicht gefunden oder kein Zugriff.')
        return redirect(url_for('dashboard'))

    set_id = set_id_row['set_id']  # aus fetchone Dictionary holen

    # Karte löschen
    db.execute('DELETE FROM flashcards WHERE id = ? AND user_id = ?', (id, user_id))
    db.commit()

    flash('Karte wurde gelöscht.')
    return redirect(url_for('manage_set', set_id=set_id))

# ----------------------------------
# Lern-Set Auswahl
# ----------------------------------
@app.route('/learn/sets')
def learn_select_set():
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    sets = db.execute('SELECT id, name FROM sets WHERE user_id = ? ORDER BY name', (user_id,)).fetchall() # Holt alle Sets, alphabetisch sortiert
    return render_template('learn_select_set.html', sets=sets)

# ----------------------------------
# Lernen eines ausgewählten Sets
# ----------------------------------
@app.route('/learn/<int:set_id>', methods=['GET', 'POST'])
def learn_set(set_id):
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    set_obj = db.execute('SELECT id, name FROM sets WHERE id = ? AND user_id = ?', (set_id, user_id)).fetchone()
    if not set_obj:
        flash('Set nicht gefunden oder kein Zugriff.')
        return redirect(url_for('learn_select_set'))

    if request.method == 'POST':
        if 'result' in request.form:
            card_id = int(request.form['card_id'])
            result = request.form['result']

            card = db.execute(
                'SELECT box FROM flashcards WHERE id = ? AND user_id = ? AND set_id = ?',
                (card_id, user_id, set_id)
            ).fetchone()

            if card:
                current_box = card['box']
                new_box = min(current_box + 1, 3) if result == 'correct' else 1

                db.execute(
                    'UPDATE flashcards SET box = ?, last_reviewed = DATE("now") WHERE id = ? AND user_id = ? AND set_id = ?',
                    (new_box, card_id, user_id, set_id)
                )
                db.commit()

            return redirect(url_for('learn_set', set_id=set_id))

        elif 'show_answer' in request.form:
            card_id = int(request.form['card_id'])
            card = db.execute(
                'SELECT * FROM flashcards WHERE id = ? AND user_id = ? AND set_id = ?',
                (card_id, user_id, set_id)
            ).fetchone()

            if card:
                return render_template('learn.html', card=card, reveal=True, set_obj=set_obj)

    for box in [1, 2, 3]:
        cards = db.execute(
            'SELECT * FROM flashcards WHERE user_id = ? AND set_id = ? AND box = ?',
            (user_id, set_id, box)
        ).fetchall()

        if cards:
            card = random.choice(cards)
            return render_template('learn.html', card=card, reveal=False, set_obj=set_obj)

    flash('Keine Karteikarten zum Lernen im Set vorhanden.')
    return redirect(url_for('learn_select_set'))


# ----------------------------------------------------------------------------------
# JSON File - Karteikarten - Reine Rohdaten, Headless = Kein Header/Footer etc.
# ----------------------------------------------------------------------------------

@app.route('/api/flashcards')
def api_flashcards():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401 # Fehlercode 401 = Unauthorized

    db = get_db()
    user_id = session['user_id']

    cards = db.execute(
        'SELECT id, set_id, question, answer, box, last_reviewed FROM flashcards WHERE user_id = ?', # Holt alle Karten inklusive Box = Lernstufe
        (user_id,)
    ).fetchall()

    # Konvertiere sqlite3.Row-Objekte in Dictionaries
    cards_list = [dict(card) for card in cards] # Hier werden sie in normale Python Dictionaries umgewandelt, die dann als JSON ausgegeben werden können

    return jsonify({'flashcards': cards_list}) # Gibt eine strukturierte JSON File zurück


# http://127.0.0.1:5000/api/flashcards im Browser aufrufen, nachdem man sich eingeloggt hat

# ----------------------------------
# App starten (lokal)
# ----------------------------------
if __name__ == '__main__': # Benutze ich z. B "flask run --reload" statt python app.py wird das hier nie gestartet
    app.run(debug=True, use_reloader=True) # Debug = Aktiviert Fehlermeldungen, reloader = Server startet automatisch neu, wenn man eine Datei ändert
    
# ----------------------------------
# Impressum
# ----------------------------------
@app.route('/imprint')
def imprint():
    return render_template('imprint.html')

# JSON = Javascript Object Notation
