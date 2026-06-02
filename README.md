# DDKI

**DDKI** ist eine Linux-Desktop-Anwendung zur Erfassung, Verwaltung und Auswertung von täglichen Fahrstrecken – entwickelt mit Python und PySide6 (Qt6).

> Version 0.4.0 · Linux · Python 3.11+

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

- **Monatsbasiertes Fahrtenbuch** – Einträge werden pro Monat verwaltet; Monate lassen sich inline hinzufügen und einzeln löschen (mit Bestätigung)
- **Monatsliste mit Jahres-Trennung** – neueste Monate oben, älteste unten; Jahresgruppen werden mit einem Header abgetrennt; aktueller Monat wird beim Start automatisch hervorgehoben
- **Direktes Eintragen** – alle Tage des Monats werden aufgelistet, Ort/Route und Kilometer werden direkt in die Zeile eingetragen und sofort gespeichert
- **Vordefinierte Routen mit Autocomplete** – häufig genutzte Orte/Routen in den Einstellungen hinterlegen; beim Klick auf die Ort-Spalte öffnet sich sofort ein Dropdown mit den ersten 4 Einträgen, beim Tippen wird gefiltert
- **Automatische Rundstreckenkalkulation** – eingegebene Kilometer werden automatisch mit ×2 als Hin-&-Zurück-Strecke berechnet
- **Fehlervalidierung in Echtzeit** – ungültige Werte in der Fahrstrecke-Spalte erscheinen als aufklappbare Fehlerliste (max. 4 sichtbar)
- **Dashboard mit Fehlende-Einträge-Assistent** – zeigt ausstehende Tage des aktuellen Monats zuerst, danach Monat für Monat; direkt von dort eintragen oder überspringen
- **Einstellungen** – vordefinierte Routen/Orte hinzufügen und verwalten
- **Light- & Dark-Mode** – per Knopfdruck umschaltbar, Auswahl wird gespeichert und beim nächsten Start wiederhergestellt
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

Unter [Releases](https://github.com/taspectjs/DDKI/releases) steht eine vorkompilierte Executable bereit:

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

1. Im Menü **Daten** den gewünschten Monat in der Sidebar auswählen (neueste oben, nach Jahr gruppiert)
2. Mit **+ Monat** einen Monat direkt inline hinzufügen – per Pfeiltasten Monat und Jahr wählen → **Hinzufügen**
3. Auf eine Zeile klicken → Ort/Route-Feld öffnet Dropdown mit gespeicherten Routen; beim Tippen wird gefiltert
4. Fahrstrecke eintragen → **Hin & Zurück** wird automatisch berechnet (× 2)
5. Speicherung erfolgt sofort bei jeder Zelleingabe

### Daten – Fehlervalidierung

Enthält eine Fahrstrecke-Zelle keinen gültigen Zahlenwert, erscheint ein gelbes Warn-Banner mit den betroffenen Zeilen (max. 4 sichtbar, aufklappbar).

### Daten – Monat löschen

Das **✕**-Symbol neben einem Monat öffnet einen Bestätigungs-Dialog. Erst nach Bestätigung wird der Monat gelöscht.

---

### Dashboard – Fehlende Einträge

Zeigt ausstehende Tage geordnet nach Priorität:

1. **Aktueller Monat zuerst** – alle Tage bis heute ohne Eintrag
2. **Dann Vergangenheit Monat für Monat** – ältester unvollständiger Monat als nächstes

| Aktion | Funktion |
|--------|----------|
| **+ Eintragen** | Wechselt zu Daten, springt zur Zeile und setzt Cursor |
| **Überspringen** | Blendet den Tag für die aktuelle Sitzung aus |

---

### Einstellungen – Routen verwalten

Unter **Einstellungen** können vordefinierte Orte/Routen gespeichert werden:
- Eintrag eingeben → **+ Hinzufügen** oder Enter
- **✕** löscht einen Eintrag sofort
- Gespeichert in `~/.ddki_settings.json`

---

## Datenspeicherung

| Datei | Inhalt |
|-------|--------|
| `~/.ddki_data.json` | Alle Fahrtenbuch-Einträge nach Monat |
| `~/.ddki_settings.json` | Vordefinierte Routen + Theme-Einstellung |

Format `~/.ddki_data.json`:
```json
{
  "06.2026": [
    { "date": "02.06.26", "location": "Swisttal", "km": "27" }
  ],
  "05.2026": []
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
    ├── dashboard.py      # Dashboard
    ├── entry_view.py     # Monats- & Tagesansicht mit Autocomplete
    ├── settings_view.py  # Einstellungsseite
    ├── settings_data.py  # Routen & Theme-Speicherung
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
