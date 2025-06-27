
# **VocApp**

Web Entwicklung - HWR Berlin SS2025

---

Dieses Repository enthält den Quellcode und die Dokumentation für **VocApp**, eine Webanwendung zum effizienten Vokabellernen. Die App ermöglicht es Nutzern, eigene Vokabellisten zu erstellen, Lernfortschritte zu verfolgen und Vokabeln über ein interaktives Quizsystem zu wiederholen.

---

## **Schritte zum Starten der Anwendung**

### **Schritt 1: Repository klonen**
Zuerst muss das Repository lokal geklont werden. Öffnen Sie ein Terminal und führen Sie folgenden Befehl aus:

```bash
git clone https://github.com/SCREWYT/vocapp.git
cd VocApp
```

---

### **Schritt 2: Virtuelle Python-Umgebung einrichten**
Bevor Sie Abhängigkeiten installieren, richten Sie eine virtuelle Umgebung ein und aktivieren Sie diese:

```bash
python -m venv env
source env/bin/activate  # Für macOS/Linux
env\Scripts\activate     # Für Windows
```

---

### **Schritt 3: Erforderliche Pakete installieren und Datenbank initialisieren**
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
pip list | findstr flask  # Windows
pip list | grep flask     # macOS/Linux
```
Initialisieren sie jetzt die Datenbank mit:

```
flask init-db
```
---

### **Schritt 4: Anwendung starten**
Starten Sie die Anwendung: 

```bash
flask run
# Oder auch flask run --reload, Flask erkennt dann automatisch Änderungen im Code
```

---

### **Schritt 5: Anwendung öffnen**
Nach dem Start kann die Anwendung im Browser aufgerufen werden unter:

```
http://127.0.0.1:5000/
```

---

## **Registrierung und Anmeldung**

### **Option 1: Eigene Registrierung**

### **Option 2: Nutzung eines Testaccounts**


## **Repository-Inhalt**

---

## **Technologie-Stack**

---

## **Dokumentation**

Die vollständige technische Dokumentation finden Sie unter folgendem Link:  
[VocApp Dokumentation](https://screwyt.github.io/vocapp/)

**Inhalt der Dokumentation:**  

### **Projektstruktur und Teamreflexion**

<!-- Hier kommen dann die Reiterpunkte links bei der Doku hin --> 

---

## **Projektstatus**

### **Implementierte Funktionen**

### **Mögliche erweiternde Features**

---

## **Mitwirkende**

- **Görkem Ilias Istemi** – Matrikelnummer: 77211971439
- **Rouven Becker** – Matrikelnummer: 77211968866 

---

## **Lizenz**  

Dieses Projekt wurde für den Kurs an der HWR Berlin entwickelt und steht unter der **MIT License**.  
Die **MIT-Lizenz** erlaubt es, den Code frei zu verwenden, zu verändern und zu verbreiten, solange ein Hinweis auf die ursprünglichen Autoren erhalten bleibt.  

Die vollständige Lizenz finden Sie in der Datei [`LICENSE.txt`](LICENSE.txt).
