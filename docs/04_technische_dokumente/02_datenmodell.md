---
title: Datenmodell
parent: Technische Dokumente
nav_order: 2
---

# Datenmodell – VocApp

Dieses Datenmodell beschreibt den Aufbau der SQLite-Datenbank von VocApp. Es besteht aus drei zentralen Tabellen: **users**, **sets** und **flashcards**. Die Datenbank wird lokal im `instance`-Ordner gespeichert und per `flask init-db` erstellt.

---

## users (Benutzerkonten)

| Spalte    | Typ     | Beschreibung                              |
|-----------|---------|-------------------------------------------|
| id        | INTEGER | Primärschlüssel (eindeutige Benutzer-ID)  |
| username  | TEXT    | Benutzername (muss eindeutig sein)        |
| password  | TEXT    | Gehashter Wert des Passworts              |
| role      | TEXT    | Benutzerrolle, Standardwert = `'user'`    |

---

## sets (Karteikartensets)

| Spalte   | Typ     | Beschreibung                                       |
|----------|---------|----------------------------------------------------|
| id       | INTEGER | Primärschlüssel des Sets                           |
| user_id  | INTEGER | Fremdschlüssel, verweist auf `users(id)`           |
| name     | TEXT    | Name/Titel des Sets                                |

---

## flashcards (Karteikarten)

| Spalte         | Typ     | Beschreibung                                               |
|----------------|---------|------------------------------------------------------------|
| id             | INTEGER | Primärschlüssel der Karte                                  |
| user_id        | INTEGER | Fremdschlüssel zu `users(id)`                              |
| set_id         | INTEGER | Fremdschlüssel zu `sets(id)`                               |
| question       | TEXT    | Vorderseite der Karte (Frage)                              |
| answer         | TEXT    | Rückseite der Karte (Antwort)                              |
| box            | INTEGER | Boxnummer für Spaced Repetition (Standard: 1)              |
| last_reviewed  | DATE    | Datum der letzten Wiederholung                             |

---

## Hinweise

- Alle Karten sind eindeutig einem Set **und** einem Benutzer zugeordnet.
- Benutzerrollen werden aktuell nicht genutzt, könnten aber später für Adminfunktionen relevant sein.
- Die Datenbank wird bei Bedarf manuell per `flask init-db` neu erzeugt.
- Gespeichert wird sie unter: `instance/database.db`

---

## Beziehungen

- **Ein Benutzer** kann mehrere Sets besitzen (`1:n`)
- **Ein Set** gehört zu genau **einem Benutzer**
- **Ein Set** enthält mehrere Karteikarten (`1:n`)
- **Jede Karte** gehört zu genau **einem Set und einem Benutzer**

