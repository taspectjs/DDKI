# DDKI

**DDKI** ist eine Linux-Desktop-Anwendung zur Erfassung, Verwaltung und Auswertung von täglichen Fahrstrecken – entwickelt mit Python und PySide6 (Qt6).

> Version 0.5.1 · Linux · Python 3.11+

---

## Inhalt

- [Features](#features)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Starten](#starten)
- [Bedienung](#bedienung)
  - [Navigation](#navigation)
  - [Dashboard](#dashboard)
  - [Daten – Einträge erfassen](#daten--einträge-erfassen)
  - [Daten – Fehlervalidierung](#daten--fehlervalidierung)
  - [Daten – Monat verwalten](#daten--monat-verwalten)
  - [Daten – Import aus Tabellendatei](#daten--import-aus-tabellendatei)
  - [Analyse – Jahresauswertung](#analyse--jahresauswertung)
  - [Einstellungen – Routen verwalten](#einstellungen--routen-verwalten)
- [Datenspeicherung](#datenspeicherung)
- [Projektstruktur](#projektstruktur)
- [Abhängigkeiten](#abhängigkeiten)
- [Changelog](#changelog)
- [Lizenz](#lizenz)

---

## Features

### Kernfunktionen

- **Monatsbasiertes Fahrtenbuch** – Einträge werden pro Monat verwaltet. Monate lassen sich direkt inline hinzufügen und einzeln mit Bestätigungsdialog löschen.
- **Monatsliste mit Jahres-Trennung** – Neueste Monate oben, älteste unten. Jahresgruppen werden mit einem Trennheader abgetrennt. Der aktuelle Monat wird beim Start automatisch ausgewählt und hervorgehoben.
- **Direktes Eintragen** – Alle Tage des gewählten Monats werden tabellarisch aufgelistet. Ort/Route und Kilometer werden direkt in die Tabellenzeile eingetragen. Jede Änderung wird sofort automatisch gespeichert.
- **Automatische Rundstreckenkalkulation** – Eingegebene Kilometer werden automatisch mit ×2 multipliziert und in der Spalte **Hin & Zurück** angezeigt.
- **Vordefinierte Routen mit Autocomplete** – Häufig genutzte Orte/Routen lassen sich in den Einstellungen hinterlegen. Beim Klick auf die Ort-Spalte öffnet sich sofort ein Dropdown mit den ersten 4 gespeicherten Einträgen. Beim Tippen wird die Liste gefiltert (Suche enthält den eingegebenen Begriff, Groß-/Kleinschreibung ignoriert).

### Dashboard

- **Fehlende-Einträge-Assistent** – Zeigt Tage ohne Eintrag geordnet nach Priorität: zuerst alle ausstehenden Tage des aktuellen Monats, danach Monat für Monat (ältester unvollständiger Monat als nächstes). Wochentag wird angezeigt, Wochenenden sind visuell abgesetzt.
- **Direktes Springen** – Per **+ Eintragen** wechselt die App direkt zur betreffenden Zeile im Daten-Tab und setzt den Cursor.
- **Überspringen (sitzungsbasiert)** – Einzelne Tage können für die aktuelle Sitzung ausgeblendet werden. Nach einem Neustart werden sie wieder angezeigt.
- **Fehlerübersicht** – Zeigt alle Monate mit ungültigen Fahrstrecken-Werten in einem gelben Warn-Panel. Mehr als 4 Fehler sind per Klick aufklappbar.

### Import

- **Import aus Tabellendateien** – ODS-, XLSX- und XLS-Dateien können über den **⬆ Import**-Button in der Monats-Sidebar importiert werden.
- **Farbcodierter Vorschau-Dialog** – Jeder Eintrag wird vor dem Import klassifiziert und farblich dargestellt (Details im Abschnitt [Daten – Import](#daten--import-aus-tabellendatei)).
- **Konflikt-Erkennung** – Bei abweichenden Einträgen wird der aktuelle Wert im Vergleich angezeigt.

### Analyse

- **Jahresauswertung** – Statistiken und Diagramm für das gewählte Jahr, umschaltbar per Jahresselektor.
- **4 Statistik-Kacheln** – Gesamt-km (Hin & Zurück), Durchschnitt km/Monat, häufigste Route, stärkster Monat.
- **Interaktives Balkendiagramm** – Monatliche Kilometer (Hin & Zurück) als animiertes Balkendiagramm mit Wertbeschriftung.
- **Routen-Jahresübersicht** – Alle Routen des Jahres mit Fahrtenanzahl und Gesamt-km, absteigend nach km sortiert.

### Benutzeroberfläche

- **Light- & Dark-Mode** – Per Knopfdruck umschaltbar. Die Auswahl wird gespeichert und beim nächsten Start wiederhergestellt.
- **Moderne Scrollbar** – Gradient-gestylte Scrollbar mit Hover-Effekt in allen scrollbaren Bereichen.
- **Fehlervalidierung in Echtzeit** – Ungültige Werte in der Fahrstrecke-Spalte erscheinen als aufklappbares gelbes Warn-Banner (max. 4 sichtbar, vollständig aufklappbar).
- **Automatische Update-Prüfung** – Beim Start wird im Hintergrund auf neue GitHub-Releases geprüft. Bei Verfügbarkeit erscheint ein Dialog mit Download-Link.

---

## Voraussetzungen

| Anforderung | Version / Hinweis |
|-------------|-------------------|
| Betriebssystem | Linux (Ubuntu 20.04+ / Debian 11+ empfohlen) |
| Python | 3.11 oder neuer |
| curl oder wget | für pip-Bootstrap beim Erstinstall (einmalig) |

> **Hinweis:** Auf unterstützten Systemen reicht `./install.sh` – alle weiteren Abhängigkeiten werden automatisch eingerichtet.

---

## Installation

### Aus dem Quellcode (empfohlen)

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

Unter [Releases](https://github.com/taspectjs/DDKI/releases) steht eine vorkompilierte Standalone-Executable für Linux bereit (erstellt mit PyInstaller):

```bash
chmod +x DDKI-x.x.x-linux
./DDKI-x.x.x-linux
```

> Die kompilierte Version ist mit Ubuntu 20.04 (GLIBC 2.31) gebaut und läuft auf allen kompatiblen Distributionen.

---

## Starten

```bash
./run.sh
```

`run.sh` aktiviert automatisch das Virtual Environment und startet `main.py`.

---

## Bedienung

### Navigation

Die Navigationsleiste befindet sich links. Folgende Bereiche stehen zur Verfügung:

| Bereich | Symbol | Funktion |
|---------|--------|----------|
| **Dashboard** | 🏠 | Übersicht fehlender Einträge & Validierungsfehler |
| **Daten** | 📋 | Monatsübersicht mit direkter Tageseintragung |
| **Analyse** | 📊 | Jahresauswertung mit Diagramm und Statistiken |
| **Einstellungen** | ⚙️ | Vordefinierte Routen verwalten |

Unten links befindet sich der **Dark-/Light-Mode-Schalter** sowie die aktuelle Versionsnummer.

---

### Dashboard

Das Dashboard öffnet sich beim Start und zeigt zwei Bereiche:

#### Fehlende Einträge

- Zeigt Tage ohne Ort-Eintrag nach Priorität:
  1. Alle noch ausstehenden Tage des **aktuellen Monats** (bis heute)
  2. Falls der aktuelle Monat vollständig ist: der **älteste unvollständige Vergangenheitsmonat**
- Maximal 4 Zeilen werden standardmäßig angezeigt. Bei mehr Einträgen erscheint ein **▼ Alle (n)**-Button zum Aufklappen.
- Jede Zeile zeigt Wochentag und Datum; Wochenenden werden abgedunkelt dargestellt.

| Schaltfläche | Funktion |
|-------------|---------|
| **+ Eintragen** | Wechselt zu **Daten**, springt zur betreffenden Zeile und aktiviert das Eingabefeld |
| **Überspringen** | Blendet diesen Tag für die aktuelle Sitzung aus (wird nach Neustart wieder angezeigt) |

#### Ungültige Fahrstrecken

- Zeigt alle Monate und Tage, bei denen der km-Wert kein gültiger Zahlenwert ist.
- Das Panel erscheint gelb hervorgehoben, sobald Fehler vorhanden sind.
- Mehr als 4 Fehler sind per **▼ Alle (n)** aufklappbar.

---

### Daten – Einträge erfassen

1. Im Menü **Daten** den gewünschten Monat in der linken Sidebar auswählen (neueste Monate oben, nach Jahr gruppiert).
2. Auf eine Tabellenzeile klicken → das **Ort/Route**-Feld aktiviert sich und zeigt sofort ein Dropdown mit den ersten 4 gespeicherten Routen.
3. Route auswählen oder manuell eintippen (Filterung enthält den getippten Begriff).
4. Mit **Tab** oder Klick in die **Fahrstrecke**-Spalte wechseln und den Kilometer-Wert eingeben.
5. Die Spalte **Hin & Zurück** wird automatisch berechnet (Eingabe × 2).
6. Jede Änderung wird **sofort und automatisch** in `~/.ddki_data.json` gespeichert – kein manuelles Speichern nötig.

> Heutige und zukünftige Tage sowie Wochenenden werden visuell hervorgehoben bzw. abgedunkelt dargestellt.

---

### Daten – Fehlervalidierung

Enthält die Fahrstrecke-Spalte einen ungültigen Wert (kein ganzzahliger Zahlenwert), erscheint direkt über der Tabelle ein gelbes Warn-Banner:

- Zeigt die betroffenen Zeilen mit Datum und fehlerhaftem Wert.
- Maximal 4 Fehler sichtbar; bei mehr erscheint **▼ Alle (n)** zum Aufklappen.
- Das Banner verschwindet automatisch, sobald alle Fehler behoben sind.

---

### Daten – Monat verwalten

#### Monat hinzufügen

1. In der linken Sidebar auf **+ Monat** klicken.
2. Mit den Pfeiltasten (‹ ›) Monat und Jahr wählen.
3. **Hinzufügen** bestätigen → der Monat wird angelegt und direkt ausgewählt.

> Der Picker schlägt automatisch den nächsten Monat nach dem zuletzt vorhandenen Monat vor.

#### Monat löschen

Das **✕**-Symbol neben einem Monatseintrag öffnet einen Bestätigungs-Dialog. Erst nach expliziter Bestätigung werden der Monat und alle seine Einträge gelöscht. Die Aktion kann nicht rückgängig gemacht werden.

---

### Daten – Import aus Tabellendatei

Über den **⬆ Import**-Button am unteren Rand der Monats-Sidebar können bestehende Fahrtenbücher aus Tabellendateien importiert werden.

**Unterstützte Formate:** `.ods` (OpenDocument Spreadsheet), `.xlsx`, `.xls`

**Erwartetes Dateiformat (spaltenweise):**

| Spalte | Inhalt | Beispiel |
|--------|--------|---------|
| A | Datum (TT.MM.JJ) | `02.01.26` |
| B | Ort / Route | `Swisttal` |
| C | Fahrstrecke in km (einfach) | `27` |
| D | Hin & Zurück (optional, wird ignoriert) | `54` |

> Zeilen ohne Ort und mit km = 0 oder leer werden beim Import automatisch übersprungen.

#### Import-Vorschau-Dialog

Nach der Dateiauswahl erscheint ein Vorschau-Dialog mit allen erkannten Einträgen, farblich klassifiziert:

| Farbe | Status | Bedeutung |
|-------|--------|-----------|
| 🟢 Grün | **Identisch** | Eintrag stimmt exakt mit vorhandenen Daten überein – wird automatisch importiert, keine Aktion nötig |
| 🔵 Blau | **Neu** | Datum existiert noch nicht – standardmäßig ausgewählt |
| 🟠 Orange | **Konflikt** | Datum existiert, aber Ort oder km weichen ab – aktueller Wert wird in der letzten Spalte angezeigt, **manuell bestätigen** |

- **Alle auswählen** – Markiert alle Konflikte auf einmal zur Übernahme.
- **Importieren** – Überträgt alle ausgewählten Einträge in die Datenbank. Konflikte werden dabei überschrieben.
- **Abbrechen** – Schließt den Dialog ohne Änderungen.

---

### Analyse – Jahresauswertung

Unter **Analyse** werden alle Fahrten des gewählten Jahres zusammengefasst und ausgewertet. Der Jahresselektor oben rechts (◀ Jahr ▶) ermöglicht das Blättern zwischen Jahren.

#### Statistik-Kacheln

| Kachel | Berechnung |
|--------|-----------|
| **Gesamt km (H & Z)** | Summe aller Fahrstrecken × 2 im gewählten Jahr |
| **Ø km / Monat** | Gesamt-km geteilt durch Anzahl der Monate mit mindestens einem Eintrag |
| **Häufigste Route** | Route/Ort mit den meisten Einzelfahrten |
| **Stärkster Monat** | Monat mit den höchsten Gesamt-km (Hin & Zurück) |

#### Balkendiagramm

Zeigt die monatlichen Kilometer (Hin & Zurück) als animiertes Balkendiagramm für alle 12 Monate des gewählten Jahres. Die Werte werden direkt in den Balken angezeigt. Monate ohne Daten werden mit 0 km dargestellt.

#### Routen-Jahresübersicht

Tabelle aller genutzten Routen im gewählten Jahr, sortiert nach Gesamt-km absteigend:

| Spalte | Inhalt |
|--------|--------|
| Route | Name des Orts / der Route |
| Fahrten | Anzahl der Einzelfahrten |
| km gesamt (H & Z) | Summierte Kilometer (Hin & Zurück) |

---

### Einstellungen – Routen verwalten

Unter **Einstellungen** können vordefinierte Orte und Routen gespeichert werden, die beim Eintragen per Autocomplete vorgeschlagen werden.

- **Eintrag hinzufügen:** Namen eingeben → **+ Hinzufügen** klicken oder **Enter** drücken. Doppelte Einträge werden automatisch ignoriert.
- **Eintrag löschen:** **✕** neben dem Eintrag klicken → sofort entfernt, keine Rückfrage.

Änderungen werden sofort in `~/.ddki_settings.json` gespeichert und stehen beim nächsten Klick in die Ort/Route-Spalte zur Verfügung.

---

## Datenspeicherung

DDKI speichert alle Daten lokal im Home-Verzeichnis des Benutzers. Es werden keine Daten übertragen oder in der Cloud gespeichert.

| Datei | Inhalt |
|-------|--------|
| `~/.ddki_data.json` | Alle Fahrtenbuch-Einträge, nach Monat gegliedert |
| `~/.ddki_settings.json` | Vordefinierte Routen und Theme-Einstellung |

### Format `~/.ddki_data.json`

```json
{
  "06.2026": [
    { "date": "02.06.26", "location": "Swisttal", "km": "27" },
    { "date": "03.06.26", "location": "EU-Neustr.", "km": "12" }
  ],
  "05.2026": [
    { "date": "15.05.26", "location": "Weilerswist", "km": "20" }
  ]
}
```

> Der Monatsschlüssel hat das Format `MM.YYYY`. Das Datumsfeld verwendet das Format `TT.MM.JJ`. Der `km`-Wert ist immer als String gespeichert (einfache Strecke ohne ×2).

### Format `~/.ddki_settings.json`

```json
{
  "routes": ["Swisttal", "EU-Neustr.", "Weilerswist"],
  "theme": "dark"
}
```

> Gültige Werte für `theme`: `"light"` oder `"dark"`. Standard ist `"light"`.

---

## Projektstruktur

```
DDKI/
├── main.py               # Einstiegspunkt – startet die Qt-Anwendung
├── version.py            # Versionsnummer (__version__)
├── requirements.txt      # Python-Abhängigkeiten
├── install.sh            # Installations-Skript (venv + pip)
├── run.sh                # Start-Skript (aktiviert venv)
├── build.sh              # Kompilier-Skript (PyInstaller)
└── src/
    ├── main_window.py    # Hauptfenster, Sidebar-Navigation, Update-Check
    ├── dashboard.py      # Dashboard – fehlende Einträge & Fehlerübersicht
    ├── entry_view.py     # Monats- & Tagesansicht, Autocomplete, Import-Button
    ├── analyse_view.py   # Jahresanalyse – Statistiken, Balkendiagramm, Routentabelle
    ├── importer.py       # ODS/XLSX-Parser, Dateivergleich, Import-Logik
    ├── import_dialog.py  # Farbcodierter Import-Vorschau-Dialog
    ├── settings_view.py  # Einstellungsseite – Routen hinzufügen/entfernen
    ├── settings_data.py  # Persistenz: Routen & Theme lesen/schreiben
    ├── models.py         # Datenmodell (Entry), JSON-I/O, Hilfsfunktionen
    ├── theme.py          # Light-/Dark-Theme-Definitionen und ThemeManager
    └── updater.py        # Hintergrund-Update-Check via GitHub-API
```

---

## Abhängigkeiten

| Paket | Version | Verwendung |
|-------|---------|-----------|
| `PySide6` | ≥ 6.6.0 | Qt6-GUI-Framework (Widgets, Charts, Themes) |
| `requests` | ≥ 2.31.0 | HTTP-Request für Update-Check |
| `packaging` | ≥ 24.0 | Versionsvergleich (Update-Check) |
| `odfpy` | ≥ 1.4.1 | Lesen von `.ods`-Dateien (Import) |
| `openpyxl` | ≥ 3.1.0 | Lesen von `.xlsx`/`.xls`-Dateien (Import) |

Alle Pakete werden durch `install.sh` automatisch im Virtual Environment installiert.

---

## Changelog

### v0.5.1
- **Fix:** Binary-Kompatibilität für Ubuntu 24.04 und ältere Systeme wiederhergestellt (GLIBC 2.43 → 2.31)
- Build auf `python:3.11-slim-bullseye` (Debian 11, GLIBC 2.31) via Docker und GitHub Actions

### v0.5.0
- **Neu:** Import aus ODS-, XLSX- und XLS-Dateien mit farbcodiertem Vorschau-Dialog (identisch / neu / Konflikt)
- **Neu:** Analyse-Tab mit Jahresselektor, 4 Statistik-Kacheln, monatlichem Balkendiagramm und Routen-Jahresübersicht
- Abhängigkeiten: `odfpy` und `openpyxl` hinzugefügt

### v0.4.0
- Inline-Monats-Picker, Jahres-Trennheader in der Sidebar
- Autocomplete-Fix, Theme-Persistenz

### v0.3.1
- Vordefinierte Routen mit Autocomplete
- Einstellungsseite

### v0.3.0
- Dashboard mit Fehlende-Einträge-Assistent
- Moderne Scrollbar, diverse Bugfixes

---

## Lizenz

MIT License – siehe [LICENSE](LICENSE) für Details.
