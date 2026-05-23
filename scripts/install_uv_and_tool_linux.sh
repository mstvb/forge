#!/usr/bin/env bash
set -euo pipefail

# Usage: ./install_uv_and_tool_linux.sh [tool]
# Default tool: forge

TOOL="${1:-forge}"

echo "==> Prüfe, ob 'uv' installiert ist..."
if ! command -v uv >/dev/null 2>&1; then
  echo "'uv' nicht gefunden — versuche Installation via curl..."
  if command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "Hinweis: Falls 'uv' nach der Installation nicht im PATH ist, lade die Shell neu oder füge ~/.local/bin hinzu."
  else
    echo "Fehler: 'curl' nicht gefunden. Bitte installiere 'curl' oder installiere 'uv' manuell." >&2
    exit 1
  fi
else
  echo "'uv' ist bereits installiert."
fi

echo "==> Installiere Tool: $TOOL"
uv tool install "$TOOL"

echo "Fertig. Überprüfe mit: uv tool list"
