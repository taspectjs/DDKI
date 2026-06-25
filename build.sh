#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"
VERSION=$(python3 -c "exec(open('$SCRIPT_DIR/version.py').read()); print(__version__)")

echo "DDKI Build v$VERSION"
echo "--------------------"

# ── Docker-Build (empfohlen) ──────────────────────────────────────────────────
# Basis: python:3.11-slim-bullseye = Debian 11, GLIBC 2.31, Python 3.11
# Regel: auf dem ÄLTESTEN glibc bauen, das unterstützt werden soll.
#        glibc ist rückwärtskompatibel → Binary läuft auf allen neueren Systemen.
# Ergebnis: läuft auf Ubuntu 20.04, 22.04, 24.04 und kompatiblen Distros.
# ─────────────────────────────────────────────────────────────────────────────
if command -v docker &>/dev/null && [ "${1}" != "--local" ]; then
    echo "Docker gefunden → baue in python:3.11-slim-bullseye (GLIBC 2.31, Python 3.11)..."
    echo "  (läuft auf Ubuntu 20.04 / 22.04 / 24.04 und neuer)"
    echo ""

    docker run --rm \
        -v "$SCRIPT_DIR":/app \
        -w /app \
        python:3.11-slim-bullseye bash -c "
            set -e
            export DEBIAN_FRONTEND=noninteractive

            echo '→ Qt-Abhängigkeiten installieren...'
            apt-get update -qq
            apt-get install -y -qq \
                binutils \
                libgl1 \
                libglib2.0-0 \
                libxcb-xinerama0 \
                libxcb-icccm4 \
                libxcb-image0 \
                libxcb-keysyms1 \
                libxcb-render-util0 \
                libxkbcommon-x11-0 \
                >/dev/null

            echo '→ Python-Pakete installieren...'
            pip install --quiet --upgrade pip
            pip install --quiet -r requirements.txt pyinstaller

            echo '→ PyInstaller läuft...'
            pyinstaller \
                --onefile \
                --name 'DDKI-${VERSION}-linux' \
                --distpath /app/dist \
                --workpath /tmp/pyibuild \
                --specpath /tmp/pyibuild \
                --hidden-import 'PySide6.QtXml' \
                --hidden-import 'PySide6.QtCharts' \
                --hidden-import 'PySide6.QtOpenGL' \
                --collect-all 'PySide6' \
                --collect-all 'odf' \
                --collect-all 'openpyxl' \
                /app/main.py
        "

    echo ""
    echo "✓ Fertig (Docker-Build, GLIBC 2.31+):"
    echo "  dist/DDKI-$VERSION-linux"

# ── Lokaler Build (Fallback) ──────────────────────────────────────────────────
else
    if [ "${1}" != "--local" ]; then
        echo "⚠  Docker nicht gefunden."
        echo "   Für maximale Kompatibilität Docker installieren und erneut ausführen."
        echo "   Lokaler Build nutzt GLIBC dieser Maschine → Binary läuft ggf. nicht"
        echo "   auf älteren Ubuntu-Versionen."
        echo ""
    fi

    if [ ! -f "$VENV/bin/python" ]; then
        echo "Fehler: Bitte zuerst ./install.sh ausführen."
        exit 1
    fi

    PYTHON_VER=$("$VENV/bin/python" --version 2>&1)
    echo "Lokaler Build mit $PYTHON_VER..."

    "$VENV/bin/pip" install pyinstaller --quiet

    "$VENV/bin/pyinstaller" \
        --onefile \
        --name "DDKI-$VERSION-linux" \
        --distpath "$SCRIPT_DIR/dist" \
        --workpath "$SCRIPT_DIR/build" \
        --specpath "$SCRIPT_DIR/build" \
        --hidden-import "PySide6.QtXml" \
        --hidden-import "PySide6.QtCharts" \
        --hidden-import "PySide6.QtOpenGL" \
        --collect-all "PySide6" \
        --collect-all "odf" \
        --collect-all "openpyxl" \
        "$SCRIPT_DIR/main.py"

    echo ""
    echo "✓ Fertig (lokaler Build):"
    echo "  dist/DDKI-$VERSION-linux"
fi

echo ""
echo "Release erstellen (via GitHub Actions – empfohlen):"
echo "  git tag v$VERSION && git push origin v$VERSION"
echo "  → GitHub Actions baut und veröffentlicht automatisch"
echo ""
echo "Manuell hochladen:"
echo "  GitHub → Releases → New Release → Binary anhängen"
