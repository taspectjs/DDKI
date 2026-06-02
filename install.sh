#!/bin/bash
set -e

echo "DDKI – Abhängigkeiten installieren"
echo "----------------------------------"

# Python prüfen
if ! command -v python3 &>/dev/null; then
    echo "Fehler: Python 3 ist nicht installiert."
    exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

# python-venv installieren falls nötig
if ! python3 -c "import ensurepip" &>/dev/null; then
    echo "Installiere python${PY_VER}-venv (benötigt sudo)..."
    sudo apt install -y "python${PY_VER}-venv"
fi

# curl oder wget installieren falls nötig
if ! command -v curl &>/dev/null && ! command -v wget &>/dev/null; then
    echo "Installiere curl (benötigt sudo)..."
    sudo apt install -y curl
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Virtual Environment erstellen
if [ ! -f "$VENV_DIR/bin/python" ]; then
    [ -d "$VENV_DIR" ] && rm -rf "$VENV_DIR"
    echo "Erstelle Virtual Environment..."
    python3 -m venv --without-pip "$VENV_DIR"
fi

# pip bootstrappen
if ! "$VENV_DIR/bin/python" -m pip --version &>/dev/null; then
    echo "Bootstrappe pip..."
    if command -v curl &>/dev/null; then
        curl -sS https://bootstrap.pypa.io/get-pip.py | "$VENV_DIR/bin/python"
    else
        wget -qO- https://bootstrap.pypa.io/get-pip.py | "$VENV_DIR/bin/python"
    fi
fi

echo "Installiere Pakete..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip --quiet
"$VENV_DIR/bin/python" -m pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "Fertig. Starten mit:  ./run.sh"
