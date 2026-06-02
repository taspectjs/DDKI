#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"
VERSION=$(python3 -c "exec(open('$SCRIPT_DIR/version.py').read()); print(__version__)")

echo "DDKI Build v$VERSION"
echo "--------------------"

# Docker-Build (kompatibel mit älteren Systemen, GLIBC 2.31)
if command -v docker &>/dev/null && [ "${1}" != "--local" ]; then
    echo "Docker gefunden → baue in Ubuntu 20.04 (GLIBC 2.31, breite Kompatibilität)..."
    docker run --rm \
        -v "$SCRIPT_DIR":/app \
        -w /app \
        ubuntu:20.04 bash -c "
            set -e
            export DEBIAN_FRONTEND=noninteractive
            apt-get update -qq
            apt-get install -y -qq python3 python3-venv python3-pip curl libgl1 libglib2.0-0 \
                libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
                libxcb-render-util0 libxkbcommon-x11-0 >/dev/null
            python3 -m venv /tmp/build_venv
            /tmp/build_venv/bin/pip install --quiet --upgrade pip
            /tmp/build_venv/bin/pip install --quiet -r requirements.txt pyinstaller
            /tmp/build_venv/bin/pyinstaller \
                --onefile \
                --name 'DDKI-${VERSION}-linux' \
                --distpath /app/dist \
                --workpath /tmp/pyibuild \
                --specpath /tmp/pyibuild \
                --hidden-import PySide6.QtXml \
                --collect-all PySide6 \
                /app/main.py
        "
    echo ""
    echo "Fertig (Docker-Build, GLIBC 2.31+):"
    echo "  dist/DDKI-$VERSION-linux"
else
    # Lokaler Build (gleiche GLIBC wie dieses System)
    if [ ! -f "$VENV/bin/python" ]; then
        echo "Fehler: Bitte zuerst ./install.sh ausführen."
        exit 1
    fi
    echo "Lokaler Build (GLIBC dieser Maschine)..."
    "$VENV/bin/python" -m pip install pyinstaller --quiet
    "$VENV/bin/pyinstaller" \
        --onefile \
        --name "DDKI-$VERSION-linux" \
        --distpath "$SCRIPT_DIR/dist" \
        --workpath "$SCRIPT_DIR/build" \
        --specpath "$SCRIPT_DIR/build" \
        --hidden-import "PySide6.QtXml" \
        --collect-all "PySide6" \
        "$SCRIPT_DIR/main.py"
    echo ""
    echo "Fertig (lokaler Build):"
    echo "  dist/DDKI-$VERSION-linux"
fi

echo ""
echo "Release erstellen:"
echo "  git tag v$VERSION && git push origin v$VERSION"
echo "  Dann auf GitHub → Releases → Binary hochladen"
