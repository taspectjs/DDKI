#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"
VERSION=$(python3 -c "exec(open('$SCRIPT_DIR/version.py').read()); print(__version__)")

echo "DDKI Build v$VERSION"
echo "--------------------"

if [ ! -f "$VENV/bin/python" ]; then
    echo "Fehler: Bitte zuerst ./install.sh ausführen."
    exit 1
fi

echo "Installiere PyInstaller..."
"$VENV/bin/python" -m pip install pyinstaller --quiet

echo "Baue Executable..."
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
echo "Fertig! Executable:"
echo "  dist/DDKI-$VERSION-linux"
echo ""
echo "Release erstellen:"
echo "  git tag v$VERSION"
echo "  git push origin v$VERSION"
echo "  Dann auf GitHub → Releases → 'Draft new release' → Tag wählen → dist/ hochladen"
