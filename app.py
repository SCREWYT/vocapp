from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db, close_db, init_db

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
    Geschützter Bereich. Nur sichtbar, wenn eingeloggt.
    """
    if 'user_id' not in session:
        flash('Bitte logge dich ein, um fortzufahren.')
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session.get('username'))


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


# -----------------------------
# App starten (nur lokal)
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
