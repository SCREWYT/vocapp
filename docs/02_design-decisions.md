---
title: Design Entscheidungen
nav_order: 2
---

{: .no_toc }
# Design Entscheidungen

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

# 01. Arbeitsaufteilung

Wir trafen uns auf Discord und besprachen, was in den nächsten Schritten auf uns zukommt. Da es unser erstes Projekt dieser Art ist, haben wir uns vorerst an der Architektur und Struktur der Full-Stack-Webdev-GitHub-Pages von Prof. Dr. Eck orientiert: https://github.com/hwrberlin/fswd-app/tree/main.

## Meta 
- **Status:** abgeschlossen   
- **Termin:** 17.04.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker

## Problemstellung  

Wir kannten Discord bereits aus früheren Semestern, wünschten uns jedoch eine verlässlichere Möglichkeit zur Zusammenarbeit. Immerhin war es durchaus anstrengend, sich per Nachricht Code zuzusenden. 

## Entscheidung  

Durch den Dozenten und weitere Kurse wurde uns Git & GitHub nachdrücklich empfohlen. Obwohl wir uns bisher nur gelegentlich damit beschäftigt hatten, wurde schnell deutlich, wie leistungsstark dieses sogenannte "Versionskontrollsystem" ist. Es ermöglichte uns nämlich, Codeversionen nachzuverfolgen, Änderungen effizient zu verwalten und nahtlos im Team zusammenzuarbeiten. Daher wunderte es uns beide, dass uns nicht bereits in früheren Semestern dazu geraten wurde.

### Alternativen

Diese gab es kaum – GitHub ist schließlich nahezu weltweiter Standard in der Softwareentwicklung.

### Erste Idee
Unsere erste Idee war, die Aufgaben klassisch z.B. in **Frontend** und **Backend** aufzuteilen. Im Gespräch wurde jedoch klar, dass der Backend-Anteil komplexer ist als der des Frontends. Statt diese Aufteilung weiterzuverfolgen, haben wir uns gemeinsam dazu entschieden, zunächst individuell zu arbeiten: Jede Person soll sich eigenständig mit allen Projektteilen vertraut machen, Visual Studio Code kennenlernen und das GitHub-Pages-Dokument des Dozenten durchgehen. Git & GitHub kennenzulernen war ebenfalls Teil davon.

Eine spätere Anpassung der Rollenverteilung bleibt weiterhin offen. Uns war es wichtig, dass jeder Bescheid weiß bevor wir uns zu einem späteren Zeitpunkt dann erneut treffen. <br>

#### Nachtrag: Bis einschließlich Anfang Mai haben wir uns damit beschäftigt.
---
# 02. Add .gitignore + Github Pages

## Meta 
- **Status:** abgeschlossen   
- **Termin:** 10.05.2025 - 14.05.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi


## Problemstellung + Entscheidung: .gitignore

Dank des GitHub Pages Tutorials von Herr Eck wussten wir bereits früh, wie wichtig eine `.gitignore-Datei` ist. Durch das Einbinden dieser Datei wird festgelegt, welche Dateien und Ordner *NICHT* in die Versionsverwaltung von GitHub aufgenommen werden. In anderen Worten wird somit verhindert, dass sie versehentlich ins Repository gelangen.

Das hat unser Projekt deutlich sauberer und einfacher zu verwalten gemacht. Vor allem, da Rouven mit dem Apple Betriebssystem arbeitet und ich (Görkem) mit Windows 11.

```
# Inhalt der .gitignore

# Ignoriere den __pycache__-Ordner (vorkompilierter Python-Code)
__pycache__/

# Ignoriere den Ordner für die virtuelle Umgebung
virtualenvironment/

# Ignoriere den Ordner für die virtuelle Umgebung
venv/

# Ignoriere den instance-Ordner (wird von Flask genutzt, z. B. für die SQLite-Datenbank)
instance/

# Ignoriere den DS-Store, ist eine reine MacOS Geschichte
.DS_Store

```
> Das mit dem .DS_Store kam erst am 27.05.2025 dazu

## Problemstellung + Entscheidung: GitHub Pages 

Ich habe GitHub Pages für unser Projekt eingerichtet und dabei das empfohlene „Just The Docs“-Theme von Herr Eck verwendet. Dieses Theme ist speziell für Projektdokumentationen optimiert und bietet eine klare, übersichtliche Struktur sowie eine einfache Navigation. So können wir unsere Dokumentation ansprechend präsentieren und sie für alle Beteiligten leicht zugänglich machen.


```
# Erste Iteration der Projektstruktur (Kann sich im Verlauf ändern)

docs/
├── 00_Bilder/ 
│ └── ...
├── 03_teambeurteilung/
│ ├── 01_projektziele.md
│ ├── 02_persönliche_ziele.md
│ ├── 03_teamarbeit_reflexion.md
│ └── index.md
├── 04_technische_dokumente/
│ ├── 01_architektur.md
│ ├── 02_datenmodell.md
│ ├── 03_quellen.md
│ ├── 04_werteversprechen.md
│ └── index.md
├── _config.yml
├── 02_design-decisions.md
├── 05_projektverlauf.md
├── 06_personas.md
├── 07_nutzerbewertung.md
├── 08_Minimum_Viable_Product.md
├── 10_ui_komponenten.md
└── index.md
```

# 03. Vergleich SQLite & Firebase

## Meta 
- **Status:** abgeschlossen   
- **Termin:** 15.05.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker

## Problemstellung

Wir haben überlegt, welche Datenbank wir nutzen wollen. Viele Funktionen unserer Website – wie das Speichern, Abrufen oder Sortieren von Daten – sind nur mit einer Datenbank möglich. Daher die Frage, ob SQLite oder Firebase besser zu unserem Projekt passt.

## Entscheidung

Wir haben uns für SQLite entschieden. Funktionen wie Echtzeit-Synchronisation oder besondere Sicherheitsmechanismen von Firebase brauchen wir für Vocapp nicht, da es sich um ein einfaches Projekt handelt, welches am Ende sowieso nicht veröffentlicht wird.

SQLite passt gut zu unserem Vorhaben, die Daten lokal zu speichern. Wir brauchen daher kein kompliziertes Setup. Außerdem haben wir im Modul „Datenbanken“ bereits heranführend mit SQL gearbeitet.

>Implementiert haben wir die Datenbank jedoch erst später

### Betrachtete Optionen

| **Merkmal**                | **SQLite**                          | **Firebase**                          | **Bewertung für unser Projekt (Vocapp)**                                |
|---------------------------|-------------------------------------|---------------------------------------|-------------------------------------------------------------------------|
| **Einrichtung**            | Sehr einfach, direkt nutzbar        | Erfordert Setup bei Firebase & Google | SQLite lässt sich schnell starten. |
| **Echtzeit-Sync**          | Nicht möglich                       | Ja, möglich                           | Nicht wichtig, da wir keine Live-Nutzung oder Mehrnutzer-Szenarien haben. |
| **Skalierbarkeit**         | Gut für kleine Projekte             | Besser für große & viele Nutzer       | SQLite reicht völlig für unsere Karteikarten-App.               |
| **Komplexität**            | Einfach zu verwenden                | Etwas komplexer durch Cloud-Struktur  | SQLite ist leicht verständlich und für unser Team gut umsetzbar.        |
| **Datensicherheit**        | Keine eingebauten Features          | Integrierte Sicherheitsregeln         | Für ein internes Uni-Projekt irrelevant.                        |

>Die Kosten haben wir nicht näher beleuchtet, da beide gebührenfrei  sind.

# 04. Gedankengänge zu getroffenen Entscheidungen

## Meta 
- **Status:** abgeschlossen   
- **Termin:** 18.05.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker

### Commit-Strategie

Zu Beginn des Projekts habe ich bewusst wenige Commits durchgeführt, da ich davon ausging, dass es sinnvoller wäre, größere Fortschritte gesammelt zu committen. Die Meetings innerhalb des Teams fanden regulär statt, und wir haben kontinuierlich gearbeitet – jedoch wollte ich zunächst erst Inhalte sammeln, bevor ich sie zentral ins Repository einpflegte.

Während der Vorlesung wies uns Herr Eck jedoch darauf hin, dass es ratsam ist, auch kleinste Änderungen regelmäßig zu committen. Dies erleichtert das Zurückverfolgen von Fehlern und die Versionskontrolle erheblich. Diese Empfehlung haben wir daraufhin übernommen und unser Vorgehen entsprechend angepasst.

### Aufgabenverteilung

Wir entschieden uns dazu, dass die Implementierung des **Login- und Registrierungssystems** von Rouven übernommen wird. Er hat sich um den Aufbau der Benutzerverwaltung gekümmert, während ich mich in den nächsten Schritten auf die Entwicklung des **Karteikarten-Algorithmus** konzentrieren werde. Das würde jedoch noch dauern, da ich in nächster Zeit mit anderen kurzfristigeren Uniprojekten beschäftigt war.

# 05. Login- und Registrierungsfunktion

## Meta 
- **Status:** abgeschlossen   
- **Termin:** 23.05.2025
- **Entscheidung getroffen von:** Rouven Becker

# Problemstellung

Die grundlegende Login- und Registrierungslogik für unsere App wurde von Rouven implementiert. Ziel war eine einfache, aber funktionale Benutzerverwaltung, mit der sich Nutzer:innen registrieren, anmelden und wieder ausloggen können.

Die Umsetzung erfolgt mit dem **Flask-Webframework** in Kombination mit einer **lokalen SQLite-Datenbank**. Passwörter werden dabei nicht im Klartext gespeichert, sondern sicher mit `generate_password_hash()` gehasht. Beim Login erfolgt die Überprüfung mit `check_password_hash()`.

### Aufbau im Überblick

- **Registrierung (`/register`)**  
  Nutzende können sich mit einem eindeutigen Benutzernamen und Passwort registrieren. Die Eingaben werden validiert und anschließend in die Datenbank geschrieben. Bereits vorhandene Benutzernamen werden erkannt und abgefangen.

- **Login (`/login`)**  
  Nach erfolgreicher Authentifizierung erhalten Nutzende Zugriff auf geschützte Bereiche wie das Dashboard. Ungültige Anmeldedaten führen zu einer klaren Fehlermeldung.

- **Dashboard (`/dashboard`)**  
  Diese Seite ist nur für eingeloggte Benutzer:innen zugänglich und begrüßt sie mit einem personalisierten Hinweis. Ohne Login erfolgt ein automatischer Redirect zurück zur Anmeldeseite.

- **Logout (`/logout`)**  
  Durch das Ausloggen wird die aktuelle Sitzung beendet, und die Nutzer:in wird wieder zum Login weitergeleitet.

## Aufgetretene Herausforderungen

Beim Aufbau der Funktion traten einige typische Entwicklungsprobleme auf:

- Beim Erstellen und Anzeigen der SQLite-Datenbank stellte sich heraus, dass sie standardmäßig in Python nicht direkt sichtbar ist.  
  → Lösung: Über **Homebrew** wurde ein SQL Database Viewer installiert, um die Datenbank visuell zu überprüfen.

- Nach einem Commit wurde festgestellt, dass die **Formatierung der Login- und Registrierungsseiten nicht übernommen** wurde.  
  → Ursache war ein Problem mit dem Import von Flask und der verwendeten Flask-Version in der `app.py`. Nach Anpassung funktionierte die Darstellung korrekt.

Diese Probleme konnte er frühzeitig identifizieren und beheben, was uns geholfen hat, später stabiler weiterzuentwickeln.

## Warum diese Lösung?

Die gewählte Umsetzung erfüllt alle Anforderungen, die wir an unsere einfache **Karteikarten-Web-App** stellen:

- ✅ Keine komplexe Rechteverwaltung notwendig  
- ✅ Kein Drittanbieter-Login erforderlich  
- ✅ Daten bleiben lokal gespeichert  
- ✅ Einfach erweiterbar für weitere Funktionen  

Durch die **frühe Implementierung** dieser Kernfunktion konnten wir sofort in einem realistischen Nutzungsszenario weiterentwickeln, z. B. personalisierte Inhalte speichern oder die spätere Einführung unterschiedlicher Nutzerrollen vorbereiten. Außerdem testeten wir die Datenbank, indem wir TestAccounts anlegten. 
>Nicht zu verwechseln mit den 'Admin Accounts' später

---
