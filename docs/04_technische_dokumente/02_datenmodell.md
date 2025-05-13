---
title: Datenmodell
parent: 04_technische_dokumente
nav_order: 9
---

# Datenmodell Vocapp

<!-- Das sind erstmal nur Ideen, am Ende wird viel entfernt -->

## Vokabel

| Spalte         | Typ     | Beschreibung                           |
|----------------|---------|----------------------------------------|
| Vokabel_id     | INTEGER | PK, eindeutige ID der Vokabel         |
| Wort           | TEXT    | Das Vokabelwort                       |
| Bedeutung      | TEXT    | Die Bedeutung des Wortes              |
| Sprache        | TEXT    | Die Sprache des Wortes                |
| Beispiel       | TEXT    | Beispiel für die Verwendung des Wortes |

## Benutzer

| Spalte         | Typ     | Beschreibung                           |
|----------------|---------|----------------------------------------|
| Benutzer_id    | INTEGER | PK, eindeutige ID des Benutzers       |
| Email          | TEXT    | PK, E-Mail-Adresse des Benutzers      |
| Benutzername   | TEXT    | Benutzername                          |
| Passwort       | TEXT    | Gehashter Wert des Passworts          |

## Lernfortschritt

| Spalte         | Typ     | Beschreibung                           |
|----------------|---------|----------------------------------------|
| Fortschritt_id | INTEGER | PK, eindeutige ID des Lernfortschritts|
| Benutzer_id    | INTEGER | FK, Referenz auf den Benutzer         |
| Vokabel_id     | INTEGER | FK, Referenz auf die Vokabel          |
| Lernstatus     | TEXT    | Der Status (z. B. "neu", "gelernt", "wiederholen") |
| Lernrate       | INTEGER | Häufigkeit, mit der die Vokabel wiederholt wird |

## Lernsets

| Spalte         | Typ     | Beschreibung                           |
|----------------|---------|----------------------------------------|
| Set_id         | INTEGER | PK, eindeutige ID des Lernsets        |
| Benutzer_id    | INTEGER | FK, Referenz auf den Benutzer         |
| Set_name       | TEXT    | Name des Lernsets (z. B. "Englisch Level 1") |
| Vokabel_ids    | TEXT    | Liste der Vokabel_ids, die zu diesem Set gehören |

## Notizen

| Spalte         | Typ     | Beschreibung                           |
|----------------|---------|----------------------------------------|
| Notiz_id       | INTEGER | PK, eindeutige ID der Notiz           |
| Benutzer_id    | INTEGER | FK, Referenz auf den Benutzer         |
| Vokabel_id     | INTEGER | FK, Referenz auf die Vokabel          |
| Notiz          | TEXT    | Benutzerdefinierte Notiz zu einer Vokabel |
