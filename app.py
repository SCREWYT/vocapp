# Immer ein neues Terminal öffnen, danach: python3 -m venv venv
# Dann die virtuelle Umgebung aktivieren: source venv/bin/activate
# Als nächstes Abhängigkeiten installieren: pip install -r requirements.txt


# Importiert Flask & Abhängigkeiten
from flask import Flask, render_template, request, redirect, url_for, flash, session
# Für Passwortverschlüsselung (Hashing & Überprüfung)
from werkzeug.security import generate_password_hash, check_password_hash
# Für die Datenbank
import sqlite3
# Zur Überprüfung, ob eine beliebige Datei existiert
import os

# Dadurch darf Flask relativ zum instance/ Ordner arbeiten, dort liegt/wird die Datenbank erstellt
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'dein_geheimer_schluessel'  # In der echten Welt wäre das so nicht zulässig und würde durch einen zufälligen, sichereren Wert ersetzt werden

# Name der Datenbank
DATABASE = os.path.join(app.instance_path, 'database.db')

# Stellt erstmal sicher, dass der Pfad zum "instance/" Ordner überhaupt existiert
os.makedirs(app.instance_path, exist_ok=True)

# Initialisiert die SQL-Datenbank. Dank "if not os.path.exists" aber auch nur, wenn noch keine existiert
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            flash("Bitte Benutzername und Passwort eingeben")
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            flash("Registrierung erfolgreich! Bitte logge dich ein.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Benutzername existiert bereits!")
            return redirect(url_for('register'))
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['username'] = username
            flash("Login erfolgreich!")
            return redirect(url_for('dashboard'))
        else:
            flash("Ungültiger Benutzername oder Passwort!")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Bitte erst einloggen!")
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Du wurdest ausgeloggt.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
