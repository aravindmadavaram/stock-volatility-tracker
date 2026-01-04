#!/usr/bin/env bash
set -e

echo "Creating venv (.venv) and installing dependencies..."
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

echo "Setup complete. To activate the venv run:"
echo "  . .venv/bin/activate"
