#!/bin/bash
set -e

echo "DDKI – Abhängigkeiten installieren"
echo "----------------------------------"

if ! command -v python3 &>/dev/null; then
    echo "Fehler: Python 3 ist nicht installiert."
    exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

if ! python3 -c "import ensurepip" &>/dev/null; then
    echo "Installiere python${PY_VER}-venv (benötigt sudo)..."
    sudo apt install -y "python${PY_VER}-venv"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -f "$VENV_DIR/bin/python" ]; then
    [ -d "$VENV_DIR" ] && rm -rf "$VENV_DIR"
    echo "Erstelle Virtual Environment..."
    python3 -m venv --without-pip "$VENV_DIR"
fi

if ! "$VENV_DIR/bin/python" -m pip --version &>/dev/null; then
    echo "Bootstrappe pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | "$VENV_DIR/bin/python"
fi

echo "Installiere Pakete..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip --quiet
"$VENV_DIR/bin/python" -m pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "Fertig. Starten mit:  ./run.sh"
