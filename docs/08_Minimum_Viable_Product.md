---
title: MVP von VocApp
nav_order: 15
---

## Ziel

Die Webanwendung **VocApp** verfolgt das Ziel, das digitale Lernen von Vokabeln durch ein **einfaches**, aber **effektives** Karteikartensystem zu unterstützen. Nutzer können eigene Karteikarten-Sets anlegen, bearbeiten und gezielt über eine Lernfunktion abfragen lassen. 

Dabei liegt der Fokus auf einem stabilen Backend, einer klaren Trennung von Logik und Oberfläche sowie einer intuitiven und möglichst **schlanken** Benutzerführung.

---

## Funktionen im MVP

### Backend-Fokus

1. **Nutzerregistrierung und Login**
   - Funktionale Nutzerverwaltung mit Login über SQLite; Fokus liegt auf eindeutigen Nutzern, nicht auf Sicherheitsaspekten.
2. **Karteikarten-Sets verwalten**
   - Anlegen, Bearbeiten und Löschen von Sets und einzelnen Karten über eine eigene Datenbankstruktur.
3. **Lernmodus**
   - Abfrage einzelner Karten mit Frage-/Antwort-Logik und einfachem Fortschrittskonzept.

---

### UI-Fokus

1. **Grunddesign**
   - Einfaches, responsives Layout mit Navigation zwischen Startseite, Login, Dashboard und Lernbereich.
2. **Formulare**
   - Registrierung, Login, Karteikarten-Erstellung und Bearbeitung mit grundlegender Validierung.
3. **Datenanzeige**
   - Übersichtliche Darstellung der vorhandenen Karteikartensets in Tabellenform mit Bearbeitungsoptionen.

---

## Aufgabenliste

### Backend
- [x] Datenbankmodell mit Nutzern, Sets und Karten definieren
- [x] Login- und Registrierungslogik mit Passwort-Hashing
- [x] Karten erstellen, bearbeiten und löschen (CRUD)
- [x] Simple Spaced Repetition Logik für Abfragen umsetzen

### Frontend
- [x] HTML-Templates mit Jinja2 anlegen
- [x] Formulare und Buttons mit Backend verknüpfen
- [x] Navigation über Navbar implementieren
- [x] Styling optimieren (z. B. Tabellen, Buttons mittig und einheitlich gestalten)

---

## Technologien

- **Backend**: Flask (Python), SQLite, SQLAlchemy
- **Frontend**: HTML, CSS (teilweise Bootstrap), Jinja2
- **Tools**: Git, GitHub, VS Code
---

## Nicht im MVP

- Kein Benutzer-Ranking oder Gamification
- Kein Fortschrittsspeicher pro Karteikarte (z. B. Lernstandsanzeige)
