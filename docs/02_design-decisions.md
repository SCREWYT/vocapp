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

# 01. Der Anfang

Da es unser erstes Projekt dieser Art ist, haben wir uns vorerst an der Architektur und Struktur der Full-Stack-Webdev-GitHub-Pages von Prof. Dr. Eck orientiert: https://github.com/hwrberlin/fswd-app/tree/main.

## Meta 

- **Status:** abgeschlossen   
- **Datum:** 17.04.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker

## Problemstellung  

Wir kommunizierten hauptsächlich über Whatsapp, uns fehlte jedoch ein verlässliches Tool, um gemeinsam am selben Code zu arbeiten.

## Entscheidung  

Durch den Dozenten und weitere Kurse wurden uns Git & GitHub ausdrücklich empfohlen. Obwohl wir uns bisher nur gelegentlich damit beschäftigt hatten, wurde schnell deutlich, wie leistungsstark dieses sogenannte "Versionskontrollsystem" ist. Es ermöglichte uns nämlich, Codeversionen nachzuverfolgen, Änderungen effizient zu verwalten und nahtlos im Team zusammenzuarbeiten. Daher wunderte es uns beide, dass uns nicht bereits in früheren Semestern und Kursen dazu geraten wurde.

## Alternativen

GitHub ist weltweiter Standard in der Softwareentwicklung - Alternativen kamen somit nicht infrage.

## Erste Idee
Unsere erste Idee war, die Aufgaben klassisch z.B. in **Frontend** und **Backend** aufzuteilen. Im Gespräch wurde jedoch klar, dass der Backend-Anteil komplexer ist als der des Frontends. Statt diese Aufteilung weiterzuverfolgen, haben wir uns gemeinsam dazu entschieden, zunächst individuell zu arbeiten: Jede Person soll sich eigenständig mit allen Projektteilen vertraut machen, Visual Studio Code kennenlernen und das GitHub-Pages-Dokument des Dozenten durchgehen. Git & GitHub kennenzulernen war ebenfalls Teil davon.

Eine spätere Anpassung der Rollenverteilung bleibt weiterhin offen. Uns war es wichtig, dass jeder Bescheid weiß bevor wir uns zu einem späteren Zeitpunkt dann erneut treffen. <br>

#### Nachtrag: Bis einschließlich Anfang Mai haben wir uns damit beschäftigt.
---
# 02. Add .gitignore + Github Pages

## Meta 

- **Status:** abgeschlossen   
- **Datum:** 10.05.2025 - 14.05.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi


## Problemstellung + Entscheidung: .gitignore

Dank des GitHub Pages Tutorials von Herr Eck wussten wir bereits früh, wie wichtig eine `.gitignore-Datei` ist. Durch das Einbinden dieser Datei wird festgelegt, welche Dateien und Ordner *NICHT* in die Versionsverwaltung von GitHub aufgenommen werden. In anderen Worten wird somit verhindert, dass sie versehentlich ins Repository gelangen.

Das hat unser Projekt deutlich sauberer und einfacher zu verwalten gemacht. Vor allem, da Rouven mit dem Apple Betriebssystem arbeitet und ich (Görkem) mit Windows 11.

```
# Inhalt der .gitignore

# Ignoriere den __pycache__-Ordner (vorkompilierter Python-Code)
__pycache__/

# Ignoriere den Ordner für die virtuelle Umgebung
venv/

# Ignoriere den instance-Ordner (wird von Flask genutzt, z. B. für die SQLite-Datenbank)
instance/

# Ignoriere den DS-Store, ist eine reine MacOS Geschichte
.DS_Store


```
> Der Eintrag zum .DS_Store kam erst am 27.05.2025 dazu

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
- **Datum:** 15.05.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker

## Problemstellung

Wir haben überlegt, welche Datenbank wir nutzen wollen. Viele Funktionen unserer Website – wie das Speichern, Abrufen oder Sortieren von Daten – sind nur mit einer Datenbank möglich. Daher die Frage, ob SQLite oder Firebase besser zu unserem Projekt passt.

## Entscheidung

Wir haben uns für SQLite entschieden. Funktionen wie Echtzeit-Synchronisation oder besondere Sicherheitsmechanismen von Firebase brauchen wir für Vocapp nicht, da es sich um ein einfaches Projekt handelt, welches am Ende sowieso nicht veröffentlicht wird.

SQLite passt gut zu unserem Vorhaben, die Daten lokal zu speichern. Wir brauchen daher kein kompliziertes Setup. Außerdem haben wir im Modul „Datenbanken“ bereits heranführend mit SQL gearbeitet.

>Implementiert haben wir die Datenbank jedoch erst später

## Betrachtete Optionen

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
- **Datum:** 18.05.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker

## Commit-Strategie

Zu Beginn des Projekts haben wir bewusst wenige Commits durchgeführt, da wir davon ausgingen, dass das sinnvoller ist. 

Während der Vorlesung wies uns Herr Eck jedoch darauf hin, dass es ratsam ist, auch kleinste Änderungen regelmäßig zu committen. Dies erleichtert das Zurückverfolgen von Fehlern und die Versionskontrolle erheblich. Diese Empfehlung haben wir daraufhin übernommen und unser Vorgehen entsprechend angepasst.

## Aufgabenverteilung

Wir entschieden uns dazu, dass die Implementierung des **Login- und Registrierungssystems** von Rouven übernommen wird. Er hat sich um den Aufbau der Benutzerverwaltung gekümmert, während ich mich in den nächsten Schritten auf die Entwicklung des **Karteikarten-Algorithmus** konzentrieren werde.

# 05. Login- und Registrierungsfunktion

## Meta 
- **Status:** abgeschlossen   
- **Datum:** 23.05.2025
- **Entscheidung getroffen von:** Rouven Becker

## Problemstellung

Die grundlegende Login- und Registrierungslogik für unsere App wurde von Rouven implementiert. Ziel war eine einfache, aber funktionale Benutzerverwaltung, mit der sich Nutzer registrieren, anmelden und wieder ausloggen können.

Die Umsetzung erfolgt mit dem **Flask-Webframework** in Kombination mit einer **lokalen SQLite-Datenbank**. Passwörter werden dabei nicht im Klartext gespeichert, sondern sicher mit `generate_password_hash()` gehasht. Beim Login erfolgt die Überprüfung mit `check_password_hash()`.

## Aufbau im Überblick

- **Registrierung (`/register`)**  
  Nutzende können sich mit einem eindeutigen Benutzernamen und Passwort registrieren. Die Eingaben werden validiert und anschließend in die Datenbank geschrieben. Bereits vorhandene Benutzernamen werden erkannt und abgefangen.

- **Login (`/login`)**  
  Nach erfolgreicher Authentifizierung erhalten Nutzende Zugriff auf geschützte Bereiche wie das Dashboard. Ungültige Anmeldedaten führen zu einer klaren Fehlermeldung.

- **Dashboard (`/dashboard`)**  
  Diese Seite ist nur für eingeloggte Benutzer zugänglich und begrüßt sie mit einem personalisierten Hinweis. Ohne Login erfolgt ein automatischer Redirect zurück zur Anmeldeseite.

- **Logout (`/logout`)**  
  Durch das Ausloggen wird die aktuelle Sitzung beendet, und der Nutzer zum Login weitergeleitet.

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

Durch die frühe Implementierung dieser Kernfunktion konnten wir nahtlos weitere Funktionen entwickeln, die eine Anmeldung voraussetzten – etwa das Speichern und Abrufen von **benutzerspezifischen Karteikarten**. So war es möglich, die Lerninhalte auf einzelne Nutzer zuzuschneiden und personalisierte Fortschritte zu erfassen.

---

# 06. Verzicht auf Freitexteingabe bei Vokabelabfrage

## Meta 

- **Status:** abgeschlossen   
- **Datum:** 13.06.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker
- Hier stand die **Idee** dafür fest, implementiert haben wir es später

##  Problemstellung

Im klassischen Vokabeltrainer wird die Übersetzung oft als Freitext erwartet. Das birgt jedoch Probleme:

- Frust durch Rechtschreibfehler (Trotz richtiger Antwort)
- Mehraufwand bei Auswertung und Validierung
- Erhöhte Komplexität bei Mehrwortlösungen, Synonymen etc.

## Entscheidung

**Freitext wurde vollständig durch ein „Ja/Nein“-Prinzip ersetzt.**  
Der Nutzer bewertet, ob er das Wort gewusst hätte („ja“) oder nicht („nein“).
Man spart sich Fehler und muss nur zwei statt drei Buttons klicken, um weiterzukommen. Bei Freitext müsse man die Antwort erst eintippen, bestätigen und im Anschluss noch einmal bestätigen, dass man die nächste Karte sehen möchte.

## Alternativen

- **Tolerante Freitext-Eingabe** (1-2 Zeichen falsch noch ok)
- **Multiple-Choice-Tests** statt aktiver Eingabe
- **Spracherkennung**, z. B. „Sprich die Übersetzung“ (Hätte den Rahmen des Projektes gesprengt)

## Fazit / Umsetzung

Die Lösung ist minimalistisch, schnell und nutzerfreundlich.  
Sie passt zum gewünschten Flow und reduziert Frustration. Auch ohne Freitexteingabe bleibt der aktive Erinnerungsprozess erhalten, da bewusstes Denken gefordert wird.

---

# 07. Spaced-Repetition-System

## Meta 

- **Status:** abgeschlossen   
- **Datum:** 25.06.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi & Rouven Becker basierend auf dem Feedback von Herr Eck

## Problemstellung

Einfaches Wiederholen aller Karteikarten in fester Reihenfolge führt oft zu wenig effektivem Lernen – es kommt kaum zur sinnvollen Wiederholung und es entsteht ein falsches Gefühl von Selbstsicherheit.
→ Wie lässt sich smart wiederholen, um langfristiges Behalten zu fördern?

## Entscheidung

**Implementierung eines einfachen Spaced-Repetition-Algorithmus auf Empfehlung unseres Dozenten**:  
- Es existieren drei Boxen (Box 1 | Box 2 | Box 3)
- Jede Karte befindet sich anfangs in Box 1
- „Ja“ erhöht das Level um eins → längere Pause bis zur nächsten Abfrage  
- „Nein“ setzt das Level auf Box 1 zurück → baldige Wiederholung relativ zum eingeordneten Level aller anderen Karten

## Mögliche Alternativen

- **SM2-Algorithmus (Anki)**: komplexer, mathematisch genau, aber schwer zu debuggen  
- **Zufällige Wiederholung ohne System**  
- **Feste Lernsets** (z. B. „heute nur 10 Karten“)

## Fazit / Umsetzung

Das gewählte System ist einfach, verständlich und lässt sich gut mit Flask umsetzen. Es motiviert durch spürbaren Fortschritt und unterstützt sinnvolles Lernen – ohne externe Tools.

---
# 08. Navigationsleiste nur bei Login sichtbar

## Meta 

- **Status:** abgeschlossen   
- **Datum:** 29.06.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi

## Problemstellung

Die Navigationsleiste wurde zu Beginn auf jedem Screen angezeigt – ergibt aber wenig Sinn, wenn man noch nicht eingeloggt ist.
 
## Das führte zu zwei Problemen:

- Unlogisches Verhalten: z. B. Anzeige von Menüpunkten, obwohl der Nutzer nicht eingeloggt war  
- Technische Fehler durch unerlaubte Zugriffsversuche auf geschützte Bereiche

## Entscheidung

Die Navigationsleiste wird **nur nach erfolgreichem Login eingeblendet**.  
Nicht eingeloggte Nutzer sehen sie also nicht.

## Mögliche Alternativen

- Navbar immer sichtbar vielleicht mit ausgegrauten Links - stilistisch unschön
- Dynamisches Anzeigen/Verstecken einzelner Menüpunkte je nach Route - jedoch ehrlicherweise zu viel Aufwand 
- Soft-Redirects bei unautorisierten Zugriffen - vermutlich die plausibelste Alternative, wir haben uns jedoch für unsere Logik entschieden

## Fazit / Umsetzung

Die gewählte Lösung ist logisch nachvollziehbar und verbessert die User Experience.  
Sie verhindert Navigationsfehler. Nur autorisierte Nutzer haben so Zugriff.

---
# 09. Verzicht auf Tabellenanzeige im Dashboard

## Meta 

- **Status:** abgeschlossen   
- **Datum:** 29.06.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi

## Problemstellung

Ursprünglich geplant war, dem Nutzer alle Karteikarten tabellarisch im Dashboard anzuzeigen.

Folge:
- Überladung des Dashboards ( Ebenfalls kein wirklicher Nutzen )
- Technisch fehleranfällig ( Viele Tabellensets nebeneinander führten zu Übersichtsproblemen )

## Entscheidung

**Die Tabellenansicht wurde komplett entfernt.**  
Das Dashboard zeigt nur noch die beiden Buttons zum Lernen oder zu den Sets.

## Mögliche Alternativen

- Suchfunktion mit Filter statt vollständiger Liste - Nettes Extra, jedoch sonst nicht zweckmäßig
- Anzeige nur der heute zu lernenden Karten - Wäre höchstens - Keine wirkliche Alternative, wäre aber immerhin eine Überlegung für ein anderes Feature

## Fazit / Umsetzung

Die Entfernung stärkt den minimalistischen Gedanken der App. Nutzer brauchen besprochenes Feature schlichtweg nicht. So wird zusätzlich das Dashboard nicht überladen.

---

# 10. Routen entfernen, die wir nicht brauchten dank Karteisets

- **Status:** abgeschlossen   
- **Datum:** 02.07.2025
- **Entscheidung getroffen von:** Görkem Ilias Istemi
## Problemstellung

Ursprünglich konnte man man einfach einzelne Karteikarten erstellen – ohne jegliche Gruppierung. Das führte zu wenig Übersicht im System, in dem Karten völlig wahllos existierten und keine Zuweisung hatten.

## Entscheidung

Wir haben uns entschieden, den Aufbau grundlegend zu überdenken und Karteisets einzuführen. Diese Sets sind thematische Sammlungen, die einem Nutzer gehören und unter denen beliebig viele Karten gespeichert werden können.

## Alternativen

Eine Option wäre gewesen, bei Einzelkarten zu bleiben und über Tags oder Filter nachträglich Struktur einzuführen. Diese Lösung wäre aber deutlich weniger praktikabel gewesen.

## Fazit

Mehrere unnötige Routen konnten wir entfernen. Das macht die App übersichtlicher und wartbarer. Innerhalb eines Sets können Karten einfach erstellt, bearbeitet und gelöscht werden – logisch gruppiert und direkt nutzerbezogen ohne unausgereifte Komplexität.




















