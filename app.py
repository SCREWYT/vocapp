from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db, close_db, init_db
import random

app = Flask(__name__)
app.secret_key = 'geheimer_schluessel'  # In Produktion durch sicheren Wert ersetzen

# Datenbankverbindung nach jedem Request sauber schließen
app.teardown_appcontext(close_db)

# ----------------------------------
# OPTIONAL: Initialisierung der DB
# ----------------------------------
@app.cli.command("init-db")
def initialize_database():
    """
    Führt init_db() aus, um die Datenbank zu erstellen.
    Aufrufbar im Terminal mit: flask init-db
    """
    init_db()
    print("Datenbank erfolgreich initialisiert.")

# ----------------------------------
# Startseite: Weiterleitung zur Login-Seite
# ----------------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ----------------------------------
# Registrierung
# ----------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        existing = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Benutzername bereits vergeben.')
            return redirect(url_for('register'))

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
    """
    Dashboard mit Sets und deren Karteikarten, alphabetisch sortiert.
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein, um fortzufahren.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    username = session.get('username')
    db = get_db()

    # Alle Sets des Nutzers alphabetisch sortiert abfragen
    sets = db.execute('SELECT id, name FROM sets WHERE user_id = ? ORDER BY name', (user_id,)).fetchall()

    sets_with_cards = []
    for s in sets:
        # Für jedes Set die Karteikarten holen
        flashcards = db.execute(
            'SELECT id, question, answer FROM flashcards WHERE set_id = ? AND user_id = ?',
            (s['id'], user_id)
        ).fetchall()
        sets_with_cards.append({
            'id': s['id'],
            'name': s['name'],
            'flashcards': flashcards
        })

    return render_template('dashboard.html', username=username, sets=sets_with_cards)



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
            return redirect(url_for('sets_overview'))

        exists = db.execute('SELECT id FROM sets WHERE user_id = ? AND name = ?', (user_id, set_name)).fetchone()
        if exists:
            flash('Du hast bereits ein Set mit diesem Namen.')
            return redirect(url_for('sets_overview'))

        db.execute('INSERT INTO sets (user_id, name) VALUES (?, ?)', (user_id, set_name))
        db.commit()
        flash(f'Set "{set_name}" wurde angelegt.')
        return redirect(url_for('sets_overview'))

    sets = db.execute('SELECT id, name FROM sets WHERE user_id = ? ORDER BY name', (user_id,)).fetchall()
    return render_template('sets_overview.html', sets=sets)

# ----------------------------------
# Verwaltung der Karteikarten im Set
# ----------------------------------
@app.route('/sets/<int:set_id>', methods=['GET', 'POST'])
def manage_set(set_id):
    if 'user_id' not in session:
        flash('Bitte logge dich ein.')
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    set_obj = db.execute('SELECT id, name FROM sets WHERE id = ? AND user_id = ?', (set_id, user_id)).fetchone()
    if not set_obj:
        flash('Set nicht gefunden oder kein Zugriff.')
        return redirect(url_for('sets_overview'))

    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()

        if not question or not answer:
            flash('Frage und Antwort dürfen nicht leer sein.')
            return redirect(url_for('manage_set', set_id=set_id))

        db.execute(
            'INSERT INTO flashcards (user_id, set_id, question, answer) VALUES (?, ?, ?, ?)',
            (user_id, set_id, question, answer)
        )
        db.commit()
        flash('Karteikarte erfolgreich hinzugefügt.')
        return redirect(url_for('manage_set', set_id=set_id))

    flashcards = db.execute(
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

    card = db.execute('SELECT * FROM flashcards WHERE id = ? AND user_id = ?', (id, user_id)).fetchone()
    if not card:
        flash('Karte nicht gefunden oder kein Zugriff.')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']

        db.execute('UPDATE flashcards SET question = ?, answer = ? WHERE id = ?', (question, answer, id))
        db.commit()

        flash('Karte erfolgreich aktualisiert.')
        return redirect(url_for('dashboard'))

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

    db.execute('DELETE FROM flashcards WHERE id = ? AND user_id = ?', (id, user_id))
    db.commit()

    flash('Karte wurde gelöscht.')
    return redirect(url_for('dashboard'))

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

    sets = db.execute('SELECT id, name FROM sets WHERE user_id = ? ORDER BY name', (user_id,)).fetchall()
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

# ----------------------------------
# App starten (lokal)
# ----------------------------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
