# DDKI

**DDKI** ist eine Linux-Desktop-Anwendung zur Erfassung, Verwaltung und Auswertung von täglichen Fahrstrecken – entwickelt mit Python und PySide6 (Qt6).

> Version 0.3.0 · Linux · Python 3.11+

---

## Inhalt

- [Features](#features)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Starten](#starten)
- [Bedienung](#bedienung)
- [Datenspeicherung](#datenspeicherung)
- [Projektstruktur](#projektstruktur)
- [Abhängigkeiten](#abhängigkeiten)
- [Lizenz](#lizenz)

---

## Features

- **Monatsbasiertes Fahrtenbuch** – Einträge werden pro Monat verwaltet, Monate lassen sich per Dialog hinzufügen (inkl. rückwirkend) und einzeln löschen (mit Bestätigung)
- **Direkte Tabellenbearbeitung** – alle Tage des Monats werden aufgelistet, Ort/Route und Kilometer werden direkt in die Zeile eingetragen und sofort gespeichert
- **Automatische Rundstreckenkalkulation** – eingegebene Kilometer (Fahrstrecke) werden automatisch mit ×2 als Hin-&-Zurück-Strecke berechnet
- **Fehlervalidierung in Echtzeit** – ungültige Werte in der Fahrstrecke-Spalte werden als aufklappbare Fehlerliste angezeigt (max. 4 sichtbar, erweiterbar)
- **Dashboard mit Fehlende-Einträge-Assistent** – zeigt ausstehende Tage des aktuellen Monats und navigiert danach Monat für Monat durch alle vergangenen unvollständigen Monate; direkt von dort eintragen oder überspringen
- **Light- & Dark-Mode** – per Knopfdruck umschaltbar
- **Moderne Scrollbar** – gradient-gestylte Scrollbar mit Hover-Effekt
- **Automatische Update-Prüfung** – beim Start wird im Hintergrund auf neue GitHub-Releases geprüft

---

## Voraussetzungen

| Anforderung | Version |
|-------------|---------|
| Betriebssystem | Linux (Ubuntu / Debian empfohlen) |
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

### Kompilierte Version (kein Python nötig)

Unter [Releases](https://github.com/taspectjs/DDKI/releases) steht eine vorkompilierte Executable für Linux zum Download bereit:

```bash
chmod +x DDKI-x.x.x-linux
./DDKI-x.x.x-linux
```

---

## Starten

```bash
./run.sh
```

`run.sh` startet die App mit dem Python-Interpreter aus `.venv/`.

---

## Bedienung

### Navigation

Die linke Seitenleiste enthält vier Menüpunkte:

| Menü | Funktion |
|------|----------|
| **Dashboard** | Fehlende Einträge & Validierungsfehler aller Monate |
| **Daten** | Monatsübersicht mit direkter Tageseintragung |
| Analyse | *(geplant)* |
| Einstellungen | *(geplant)* |

---

### Daten – Einträge erfassen

1. Im Menü **Daten** den gewünschten Monat in der linken Liste auswählen
2. Mit **+ Monat** einen neuen Monat hinzufügen – Vorauswahl ist automatisch der Folgemonat, rückwirkende Auswahl über den Dialog möglich
3. In der Tabelle direkt in eine Zeile klicken → **Ort / Route** und **Fahrstrecke** eintragen
4. Die Spalte **Hin & Zurück** berechnet sich automatisch (Fahrstrecke × 2)
5. Speicherung erfolgt sofort nach jeder Zelleingabe

### Daten – Monat löschen

Jeder Monat in der linken Liste hat ein **✕**-Symbol. Ein Klick darauf öffnet einen Bestätigungs-Dialog – erst nach Bestätigung wird der Monat inkl. aller Einträge gelöscht.

### Daten – Fehlervalidierung

Enthält eine Fahrstrecke-Zelle keinen gültigen Zahlenwert (z. B. Buchstaben), erscheint oberhalb der Tabelle ein gelbes Warn-Banner mit den betroffenen Zeilen. Bei mehr als 4 Fehlern lässt sich die Liste auf- und zuklappen.

---

### Dashboard – Fehlende Einträge

Der Dashboard zeigt ausstehende Tage geordnet nach Priorität:

1. **Aktueller Monat zuerst** – alle vergangenen Tage des laufenden Monats ohne Eintrag werden angezeigt
2. **Dann Vergangenheit Monat für Monat** – sobald der aktuelle Monat vollständig ist, erscheint der älteste unvollständige Vergangenheitsmonat, dann der nächste usw.

Pro fehlendem Tag stehen zwei Aktionen zur Verfügung:

| Aktion | Funktion |
|--------|----------|
| **+ Eintragen** | Wechselt direkt zum Menü Daten, springt zum entsprechenden Tag und setzt den Cursor |
| **Überspringen** | Blendet den Tag für die aktuelle Sitzung aus |

Bei mehr als 4 fehlenden Einträgen lässt sich die Liste auf- und zuklappen.

### Dashboard – Ungültige Fahrstrecken

Unterhalb der fehlenden Einträge werden alle Einträge mit ungültigen Fahrstrecken-Werten (über alle Monate) aufgelistet – ebenfalls aufklappbar ab 4 Einträgen.

---

## Datenspeicherung

Alle Daten werden lokal gespeichert:

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
├── build.sh             # Kompilier-Skript (PyInstaller)
└── src/
    ├── main_window.py   # Hauptfenster & Navigation
    ├── dashboard.py     # Dashboard (fehlende Einträge & Fehler)
    ├── entry_view.py    # Monats- & Tagesansicht
    ├── models.py        # Datenmodell & JSON-I/O
    ├── theme.py         # Light- / Dark-Theme
    └── updater.py       # Update-Checker
```

---

## Abhängigkeiten

```
PySide6  >= 6.6.0
requests >= 2.31.0
packaging >= 24.0
```

---

## Lizenz

MIT License – siehe [LICENSE](LICENSE) für Details.
