# **VocApp**

Web Entwicklung – HWR Berlin SS2025

---

Dieses Repository enthält den Quellcode und die Dokumentation für **VocApp**, eine Webanwendung zum effizienten Vokabellernen. Die App ermöglicht es Nutzern, eigene Vokabellisten zu erstellen, Lernfortschritte zu machen und Vokabeln über ein interaktives Quizsystem zu wiederholen.

---

## **Schritte zum Starten der Anwendung**

### Schritt 1: Repository klonen
Zuerst muss das Repository lokal geklont werden. Öffnen Sie ein Terminal und führen Sie folgenden Befehl aus:
```bash
git clone https://github.com/SCREWYT/vocapp.git
cd vocapp
```
---
### Schritt 2: Virtuelle Python-Umgebung einrichten

```bash
python3 -m venv env  # macOS/Linux
python -m venv env   # Windows
source env/bin/activate      # macOS/Linux
env\Scripts\activate         # Windows
```
---
### Schritt 3: Erforderliche Pakete installieren und Datenbank initialisieren

Installieren Sie alle benötigten Abhängigkeiten mit:
```bash
pip install -r requirements.txt
```
Falls Flask nicht installiert ist, führen Sie zusätzlich aus:
```bash
pip install flask
```
Überprüfen Sie, ob Flask erfolgreich installiert wurde:
```bash
pip list | grep flask      # macOS/Linux  
pip list | findstr flask   # Windows
```
Initialisieren sie jetzt die Datenbank mit:
```bash
flask init-db
```
---
### Schritt 4: Anwendung starten
```bash
flask run
# oder: flask run --reload
```
---
### Schritt 5: Anwendung öffnen
Nach dem Start kann die Anwendung im Browser aufgerufen werden unter:
```bash
http://127.0.0.1:5000/
```
---

### **Schritt 6: Registrierung und Anmeldung**

Ein eigener Benutzeraccount muss erstellt werden:

Beispiel-Benutzername: `demo`  
Beispiel-Passwort: `demo123`

---

## **Repository-Inhalt**

| Ordner / Datei        | Beschreibung                           |
|-----------------------|----------------------------------------|
| `app.py`              | Hauptanwendung mit Routing             |
| `db.py`               | Datenbanksetup und Initialisierung     |
| `templates/`          | HTML-Dateien (Jinja2)                  |
| `static/`             | CSS-Dateien und Bilder                 |
| `docs/`               | GitHub Pages Dokumentation             |
| `requirements.txt`    | Listet alle Python-Abhängigkeiten auf  |
| `README.md`           | Installationsanleitung & Projektinfos  |
| `LICENSE.txt`         | MIT-Lizenz                             |
| `.gitignore`          | Schließt Dateien vom Git-Tracking aus  |

---

## **Technologie-Stack**

| Komponente   | Technologie        |
|--------------|--------------------|
| Frontend     | HTML, CSS, Jinja2  |
| Backend      | Python (Flask)     |
| Datenbank    | SQLite             |
| Styling      | Custom CSS         |
| Hosting      | GitHub Pages       |

---

## **Dokumentation**

Die vollständige technische Dokumentation finden Sie unter folgendem Link:  
[VocApp Dokumentation](https://screwyt.github.io/vocapp/)

**Inhalte:** Projektstruktur, Architektur, Use-Cases, Figma-Prototyp, Upgradesystem, Fehlerbehandlung, Quellen, etc.

---

## **Projektstatus**

### **Implementierte Funktionen**
- Nutzerregistrierung und -login
- Flashcards anlegen, bearbeiten und löschen
- SQLite-Datenbank
- GitHub Pages Dokumentation inkl. Figma-Prototyp

### **Mögliche Erweiterungen**
- CSV-Import/Export von Vokabellisten
- Fortschrittsanzeige oder Gamification-Features
- Freundesliste und geteilte Sets
- Dark Mode

---

## **Mitwirkende**

- **Görkem Ilias Istemi** – Matrikelnummer: 77211971439  
- **Rouven Becker** – Matrikelnummer: 77211968866

---

## Eidesstattliche Erklärung

Die genannten Teammitglieder erklären an Eides statt:

Diese Arbeit wurde selbständig und eigenhändig erstellt. Die den benutzten Quellen wörtlich oder inhaltlich entnommenen Stellen sind als solche kenntlich gemacht. Diese Erklärung gilt für jeglichen Inhalt und umfasst sowohl diese Dokumentation als auch den als Projektergebnis eingereichten Quellcode.

---

## **Lizenz**

Dieses Projekt wurde für den Kurs an der HWR Berlin entwickelt und steht unter der **MIT License**.  
Die **MIT-Lizenz** erlaubt es, den Code frei zu verwenden, zu verändern und zu verbreiten, solange ein Hinweis auf die ursprünglichen Autoren erhalten bleibt.  
Die vollständige Lizenz finden Sie in der Datei [`License.txt`](License.txt).

