# DDKI

**DDKI** ist eine Linux-Desktop-Anwendung zur Erfassung, Verwaltung und Auswertung von täglichen Fahrstrecken – entwickelt mit Python und PySide6 (Qt6).

> Version 0.2.1 · Linux · Python 3.11+

---

## Inhalt

- [Features](#features)
- [Screenshots](#screenshots)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Starten](#starten)
- [Bedienung](#bedienung)
- [Datenspeicherung](#datenspeicherung)
- [Projektstruktur](#projektstruktur)
- [Lizenz](#lizenz)

---

## Features

- **Monatsbasiertes Fahrtenbuch** – Einträge werden pro Monat verwaltet, Monate lassen sich per Dialog hinzufügen (inkl. rückwirkend) und löschen
- **Direkte Tabellenbearbeitung** – alle Tage des Monats werden aufgelistet, Ort/Route und Kilometer werden direkt in die Zeile eingetragen
- **Automatische Rundstreckenkalkulation** – eingegebene Kilometer werden automatisch mit ×2 als Hin-&-Zurück-Strecke berechnet
- **Fehlervalidierung** – ungültige Einträge in der Fahrstrecke-Spalte (Buchstaben o.ä.) werden als aufklappbare Fehlerliste angezeigt (max. 4 sichtbar)
- **Dashboard** – Übersicht aller Validierungsfehler über alle Monate hinweg
- **Light- & Dark-Mode** – per Knopfdruck umschaltbar, persistiert nicht (Standard: Light)
- **Moderne Scrollbar** – schmale, gradient-gestylte Scrollbar mit Hover-Effekt
- **Automatische Update-Prüfung** – beim Start wird im Hintergrund auf neue Releases geprüft (konfigurierbar via `src/updater.py`)

---

## Screenshots

> folgen in Kürze

---

## Voraussetzungen

| Anforderung | Version |
|-------------|---------|
| Betriebssystem | Linux (Ubuntu/Debian empfohlen) |
| Python | 3.11 oder neuer |
| curl | für pip-Bootstrap (einmalig) |

---

## Installation

```bash
git clone https://github.com/taspectjs/DDKI.git
cd DDKI
./install.sh
```

`install.sh` erledigt automatisch:
1. Prüft ob Python 3 installiert ist
2. Installiert `python3.x-venv` falls nötig (via `sudo apt`)
3. Erstellt ein Virtual Environment unter `.venv/`
4. Bootstrappt `pip` via `get-pip.py` (falls nicht vorhanden)
5. Installiert alle Abhängigkeiten aus `requirements.txt`

---

## Starten

```bash
./run.sh
```

`run.sh` startet die App automatisch mit dem Python-Interpreter aus `.venv/`.

---

## Bedienung

### Navigation
Die linke Seitenleiste enthält vier Menüpunkte:

| Menü | Funktion |
|------|----------|
| Dashboard | Zeigt alle ungültigen Fahrstrecken-Einträge über alle Monate |
| Daten | Monatsübersicht mit Tageseintragung |
| Analyse | *(geplant)* |
| Einstellungen | *(geplant)* |

### Daten eintragen
1. Im Menü **Daten** den gewünschten Monat in der linken Liste auswählen
2. Mit **+ Monat** einen neuen Monat hinzufügen – Vorauswahl ist der Folgemonat, rückwirkende Auswahl möglich
3. In der Tabelle direkt in die Spalten **Ort / Route** und **Fahrstrecke** klicken und tippen
4. Die Spalte **Hin & Zurück** berechnet sich automatisch (Fahrstrecke × 2)
5. Einträge werden sofort gespeichert

### Fehler
Enthält eine Fahrstrecke-Zelle keinen gültigen Zahlenwert, erscheint oberhalb der Tabelle ein gelbes Warn-Banner mit den betroffenen Zeilen. Bei mehr als 4 Fehlern lässt sich die Liste auf- und zuklappen.

### Monat löschen
Jeder Monat in der Liste hat ein **✕**-Symbol. Nach Bestätigung wird der Monat inkl. aller Einträge unwiderruflich gelöscht.

---

## Datenspeicherung

Alle Daten werden lokal in einer JSON-Datei gespeichert:

```
~/.ddki_data.json
```

Format:
```json
{
  "01.2026": [
    { "date": "02.01.26", "location": "Swisttal", "km": "27" },
    { "date": "03.01.26", "location": "EU-Neustr.", "km": "12" }
  ],
  "02.2026": []
}
```

---

## Projektstruktur

```
DDKI/
├── main.py              # Einstiegspunkt
├── version.py           # Versionsnummer
├── requirements.txt     # Python-Abhängigkeiten
├── install.sh           # Installations-Skript
├── run.sh               # Start-Skript
└── src/
    ├── main_window.py   # Hauptfenster & Navigation
    ├── dashboard.py     # Dashboard-Seite
    ├── entry_view.py    # Monats- & Tagesansicht
    ├── models.py        # Datenmodell & JSON-I/O
    ├── theme.py         # Light- / Dark-Theme
    └── updater.py       # Update-Checker
```

---

## Abhängigkeiten

```
PySide6 >= 6.6.0
requests >= 2.31.0
packaging >= 24.0
```

---

## Lizenz

MIT License – siehe [LICENSE](LICENSE) für Details.
