#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"
VERSION=$(python3 -c "exec(open('$SCRIPT_DIR/version.py').read()); print(__version__)")

echo "DDKI Build v$VERSION"
echo "--------------------"

# Gemeinsame PyInstaller-Flags
PYINSTALLER_FLAGS=(
    --onefile
    --name "DDKI-${VERSION}-linux"
    --distpath /app/dist
    --workpath /tmp/pyibuild
    --specpath /tmp/pyibuild
    # Qt-Module die PyInstaller nicht automatisch erkennt
    --hidden-import "PySide6.QtXml"
    --hidden-import "PySide6.QtCharts"
    --hidden-import "PySide6.QtOpenGL"
    # ODS-Import (odfpy nutzt interne Plugin-Registrierung)
    --collect-all "odf"
    # XLSX-Import
    --collect-all "openpyxl"
    # Alle PySide6-Komponenten einschließen (Charts, Widgets, usw.)
    --collect-all "PySide6"
    /app/main.py
)

# Docker-Build (python:3.11-slim-bullseye = Debian 11, GLIBC 2.31, Python 3.11)
# → kompatibel mit Ubuntu 20.04+, Debian 11+, und allen neueren Distros
if command -v docker &>/dev/null && [ "${1}" != "--local" ]; then
    echo "Docker gefunden → baue in python:3.11-slim-bullseye (GLIBC 2.31, Python 3.11)..."
    docker run --rm \
        -v "$SCRIPT_DIR":/app \
        -w /app \
        python:3.11-slim-bullseye bash -c "
            set -e
            export DEBIAN_FRONTEND=noninteractive
            apt-get update -qq
            # Qt-Laufzeitbibliotheken die PySide6 zur Build-Zeit braucht
            apt-get install -y -qq \
                libgl1 \
                libglib2.0-0 \
                libxcb-xinerama0 \
                libxcb-icccm4 \
                libxcb-image0 \
                libxcb-keysyms1 \
                libxcb-render-util0 \
                libxkbcommon-x11-0 \
                >/dev/null
            pip install --quiet --upgrade pip
            pip install --quiet -r requirements.txt pyinstaller
            pyinstaller ${PYINSTALLER_FLAGS[*]}
        "
    echo ""
    echo "Fertig (Docker-Build, GLIBC 2.31+, Python 3.11):"
    echo "  dist/DDKI-$VERSION-linux"
else
    # Lokaler Build – nutzt die GLIBC dieser Maschine
    if [ ! -f "$VENV/bin/python" ]; then
        echo "Fehler: Bitte zuerst ./install.sh ausführen."
        exit 1
    fi
    # distpath/workpath/specpath auf lokale Verzeichnisse umbiegen
    LOCAL_FLAGS=("${PYINSTALLER_FLAGS[@]}")
    LOCAL_FLAGS=("${LOCAL_FLAGS[@]/\/app\/dist/$SCRIPT_DIR\/dist}")
    LOCAL_FLAGS=("${LOCAL_FLAGS[@]/\/tmp\/pyibuild/$SCRIPT_DIR\/build}")
    LOCAL_FLAGS=("${LOCAL_FLAGS[@]/\/app\/main.py/$SCRIPT_DIR\/main.py}")

    echo "Lokaler Build (GLIBC dieser Maschine)..."
    "$VENV/bin/pip" install pyinstaller --quiet
    "$VENV/bin/pyinstaller" "${LOCAL_FLAGS[@]}"
    echo ""
    echo "Fertig (lokaler Build):"
    echo "  dist/DDKI-$VERSION-linux"
fi

echo ""
echo "Release erstellen:"
echo "  git tag v$VERSION && git push origin v$VERSION"
echo "  Dann auf GitHub → Releases → Binary hochladen"
