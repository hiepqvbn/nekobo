#!/usr/bin/env bash
# Simple launcher for Nekobo application on Raspberry Pi
# Usage: place this script under software/tools/startup/ or call it from systemd

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="/usr/bin/python3"

# repo root is three levels up when installed under software/tools/startup
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

cd "$SCRIPT_DIR/../../.."/software || cd "$SCRIPT_DIR"

# activate virtualenv if present
if [ -f "$REPO_ROOT/software/venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$REPO_ROOT/software/venv/bin/activate"
  PYTHON="$REPO_ROOT/software/venv/bin/python"
fi

# ensure imports can find both the repo root and the software directory
export PYTHONPATH="$REPO_ROOT:$REPO_ROOT/software:$PYTHONPATH"

echo "Starting Nekobo app from $REPO_ROOT/software (PYTHONPATH=$REPO_ROOT)"
# run as a module so package imports behave correctly
exec "$PYTHON" -m application.nekobo_main
