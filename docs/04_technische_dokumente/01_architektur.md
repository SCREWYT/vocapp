---
title: Architektur
parent: Technische Dokumente
nav_order: 8
---

# Architektur

## Überblick

**VocApp** ist eine webbasierte Lernanwendung zum Erstellen und Abfragen von digitalen Karteikarten. Nutzer können sich registrieren, eigene Karteikartensets anlegen, Fragen und Antworten einpflegen und diese im Lernmodus durchgehen.  
Die Anwendung besteht aus einem **Flask-Backend**, einer **SQLite-Datenbank** und einer einfachen, funktionalen Weboberfläche auf Basis von **HTML, CSS** und **Jinja2-Templates**.

---

## Strukturübersicht

Die Anwendung ist in **drei Hauptbereiche** unterteilt:

### 1. Frontend

- **HTML-Templates:** Strukturieren die Oberfläche und bilden die Basis für das Layout der Seiten (Login, Dashboard, Lernen etc.).
- **Jinja2:** Ermöglicht die dynamische Anzeige von Inhalten aus dem Backend (z. B. Karteikartenlisten, Begrüßungstexte).
- **CSS:** Für einfache Formatierungen und visuelle Strukturierung.

### 2. Backend

- **Flask:** Kümmert sich um Routing, Formularverarbeitung, Datenbankzugriffe und die Verarbeitung von Benutzeraktionen.
- **SQLite (via `sqlite3`):** Speichert Daten zu Nutzern, Karteikartensets und einzelnen Karten lokal ab.
- **Session-Verwaltung:** Über Flask’s `session`-Dictionary werden eingeloggte Nutzer erkannt und weitergeleitet.

### 3. Datenbank (SQLite)

- **Nutzer:** Speichert Anmeldedaten (Benutzername, Passwort).
- **Sets:** Ein Karteikartenset mit Titel, Benutzer-ID und Metainformationen.
- **Karte:** Einzelne Frage-Antwort-Paare, jeweils einem Set und Nutzer zugeordnet.

---

## Querschnittsthemen

### Datenmodell

Die Anwendung nutzt eine relationale SQLite-Datenbank. Ein Benutzer kann mehrere **Karteikartensets** anlegen, die wiederum jeweils mehrere **Karten** enthalten. Die Tabellen sind miteinander über IDs verknüpft.  
Die Datenbank muss einmalig manuell mit dem Befehl `flask init-db` erstellt werden. Sie wird anschließend im `instance`-Ordner des Projekts gespeichert.

### Authentifizierung & Sitzungsverwaltung

- Nutzer registrieren sich mit Benutzername und Passwort.
- Die Login-Session wird über Flask-Sessions gespeichert (`session['user']`).
- Nach dem Login werden Nutzerdaten geladen und passende Inhalte angezeigt.
- Logout erfolgt über `session.clear()`.

### Lernlogik

- Nutzer können ihre Karteikarten in einem einfachen Lernmodus mit einer einfachen Spaced-Repetition-Logik durchgehen.
- Fragen werden angezeigt, bei Klick auf `Antwort anzeigen` folgt die Antwort.
- Im Anschluss wählt der Nutzer zwischen `Ja` und `Nein`, wenn er die Antwort wusste oder nicht.
- Die Karte rutscht in der Spaced Repetition Logik entweder in eine höhere Box bei `Ja` oder wieder in Box 1 bei `Nein` und eine weitere Karte wird automatisch geladen.

### Benutzerführung & Navigation

- Die Navigation erfolgt über Buttons und direkte Links zur Set-Ansicht, Lernen etc.
- Alle Templates folgen einem konsistenten Layout.
- Eine Rückkehr zur Startseite ist jederzeit möglich.
- Man kann sich von jedem Screen aus direkt ausloggen.

---

## Architekturübersicht

Die App folgt dem **MVC-Prinzip (Model-View-Controller)** in vereinfachter Form:

1. **Model (SQLite-Datenbank):** Speichert alle Nutzer-, Set- und Karteninformationen.
2. **View (Jinja2, HTML, CSS):** Zeigt Inhalte dynamisch und strukturiert im Browser an.
3. **Controller (Flask-Routing):** Verarbeitet Nutzereingaben, kommuniziert mit der Datenbank und leitet Seitenaufrufe.

---

## Fazit

Die Architektur von **VocApp** ist bewusst einfach gehalten und leicht nachvollziehbar. Durch die klare Trennung von Daten, Logik und Darstellung ist sie gut erweiterbar und eignet sich hervorragend für kleinere Lernszenarien - die minimalistische Vision wurde somit erfolgreich umgesetzt. 

Potenzial für zukünftige Erweiterungen besteht z. B. in einer Fortschrittsanzeige, Kategorien-System oder einer mobilen Darstellung, die jedoch bewusst nicht Teil des MVP waren, um den Rahmen des Projekts nicht zu sprengen.

