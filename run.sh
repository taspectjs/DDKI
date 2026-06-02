#!/bin/bash
set -e

DIR="$(dirname "$0")"

if [ ! -d "$DIR/.venv" ]; then
    echo "Bitte zuerst ./install.sh ausführen."
    exit 1
fi

"$DIR/.venv/bin/python" "$DIR/main.py" "$@"
