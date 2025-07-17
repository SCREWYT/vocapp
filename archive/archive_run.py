# created with help of this tutorial (https://www.youtube.com/watch?v=71EU8gnZqZQ&t=330s)
# immer neues terminal öffnen dann: python3 -m venv venv
# dann virtuelle umgebung aktivieren: source venv/bin/activate
# dann abhängigkeiten istallieren: pip install -r requirements.txt


from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'  # In der Produktion durch einen sicheren, zufälligen Schlüssel ersetzen

DATABASE = 'database.db'

def init_db():
    # Erstelle die SQLite-Datenbank, falls sie noch nicht existiert
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
