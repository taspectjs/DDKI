# DDKI

**DDKI** ist eine Linux-Desktop-Anwendung zur Erfassung, Verwaltung und Auswertung von täglichen Fahrstrecken – entwickelt mit Python und PySide6 (Qt6).

> Version 0.3.1 · Linux · Python 3.11+

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
- **Vordefinierte Routen mit Autocomplete** – häufig genutzte Orte/Routen in den Einstellungen speichern; beim Klick auf die Ort-Spalte öffnet sich sofort ein Dropdown mit den ersten 4 Einträgen, beim Tippen wird gefiltert
- **Automatische Rundstreckenkalkulation** – eingegebene Kilometer (Fahrstrecke) werden automatisch mit ×2 als Hin-&-Zurück-Strecke berechnet
- **Fehlervalidierung in Echtzeit** – ungültige Werte in der Fahrstrecke-Spalte werden als aufklappbare Fehlerliste angezeigt (max. 4 sichtbar, erweiterbar)
- **Dashboard mit Fehlende-Einträge-Assistent** – zeigt ausstehende Tage des aktuellen Monats zuerst, danach Monat für Monat vergangene unvollständige Monate; direkt von dort eintragen oder überspringen
- **Einstellungen** – vordefinierte Routen/Orte hinzufügen, verwalten und löschen
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

Unter [Releases](https://github.com/taspectjs/DDKI/releases) steht eine vorkompilierte Executable für Linux bereit:

```bash
chmod +x DDKI-x.x.x-linux
./DDKI-x.x.x-linux
```

---

## Starten

```bash
./run.sh
```

---

## Bedienung

### Navigation

| Menü | Funktion |
|------|----------|
| **Dashboard** | Fehlende Einträge & Validierungsfehler aller Monate |
| **Daten** | Monatsübersicht mit direkter Tageseintragung |
| **Einstellungen** | Vordefinierte Routen verwalten |
| Analyse | *(geplant)* |

---

### Daten – Einträge erfassen

1. Im Menü **Daten** den gewünschten Monat auswählen
2. Mit **+ Monat** einen neuen Monat hinzufügen (Vorauswahl = Folgemonat, rückwirkend möglich)
3. Auf eine Zeile klicken → Ort/Route-Feld öffnet Dropdown mit den ersten 4 gespeicherten Routen
4. Route auswählen oder frei eintippen (Autocomplete filtert beim Tippen)
5. Fahrstrecke eintragen → **Hin & Zurück** wird automatisch berechnet (× 2)
6. Speicherung erfolgt sofort

### Daten – Fehlervalidierung

Enthält eine Fahrstrecke-Zelle keinen gültigen Zahlenwert, erscheint ein gelbes Warn-Banner mit den betroffenen Zeilen (max. 4, aufklappbar).

### Daten – Monat löschen

Das **✕**-Symbol neben einem Monat öffnet einen Bestätigungs-Dialog. Erst nach Bestätigung wird der Monat gelöscht.

---

### Dashboard – Fehlende Einträge

Zeigt ausstehende Tage geordnet nach Priorität:

1. **Aktueller Monat zuerst** – alle vergangenen und heutigen Tage ohne Eintrag
2. **Dann Vergangenheit Monat für Monat** – sobald der aktuelle Monat vollständig ist, folgt der älteste unvollständige Vergangenheitsmonat

| Aktion | Funktion |
|--------|----------|
| **+ Eintragen** | Wechselt zu Daten, springt zur Zeile und setzt den Cursor |
| **Überspringen** | Blendet den Tag für die aktuelle Sitzung aus |

---

### Einstellungen – Routen verwalten

Unter **Einstellungen** können vordefinierte Orte/Routen gespeichert werden:
- Eintrag eingeben → **+ Hinzufügen** klicken oder Enter drücken
- **✕** neben einem Eintrag löscht ihn sofort
- Gespeichert in `~/.ddki_settings.json`

---

## Datenspeicherung

| Datei | Inhalt |
|-------|--------|
| `~/.ddki_data.json` | Alle Fahrtenbuch-Einträge nach Monat |
| `~/.ddki_settings.json` | Vordefinierte Routen |

Format `~/.ddki_data.json`:
```json
{
  "01.2026": [
    { "date": "02.01.26", "location": "Swisttal", "km": "27" },
    { "date": "03.01.26", "location": "EU-Neustr.", "km": "12" }
  ]
}
```

---

## Projektstruktur

```
DDKI/
├── main.py               # Einstiegspunkt
├── version.py            # Versionsnummer
├── requirements.txt      # Python-Abhängigkeiten
├── install.sh            # Installations-Skript
├── run.sh                # Start-Skript
├── build.sh              # Kompilier-Skript (PyInstaller)
└── src/
    ├── main_window.py    # Hauptfenster & Navigation
    ├── dashboard.py      # Dashboard (fehlende Einträge & Fehler)
    ├── entry_view.py     # Monats- & Tagesansicht mit Autocomplete
    ├── settings_view.py  # Einstellungsseite
    ├── settings_data.py  # Routen-Speicherung
    ├── models.py         # Datenmodell & JSON-I/O
    ├── theme.py          # Light- / Dark-Theme
    └── updater.py        # Update-Checker
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
