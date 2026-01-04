# Stock Volatility Tracker

This project fetches recent stock data and logs per-ticker volatility to `market_data_log.csv`.

Quick setup

1. From project root:

```bash
# create venv and install deps
bash scripts/setup.sh

# activate venv (macOS / Linux)
. .venv/bin/activate

# run the script
python main.py
```

2. To run or debug in VS Code
- Open the workspace in VS Code.
- The workspace includes `.vscode/settings.json` which sets the interpreter to the project's `.venv`.
- Use the `Run` view and select `Python: Run main.py (venv)`, or start the debugger.

Notes & troubleshooting

- Recommended: use Python 3.10+ for best compatibility. The project works on Python 3.9 if `yfinance==0.1.96` is used (see `requirements.txt`).
- If `yfinance` fails to return data for a symbol, the script falls back to `yahooquery`.
- If you see SSL/OpenSSL warnings (LibreSSL), they are usually non-fatal but upgrading system OpenSSL or using a newer Python from `pyenv` can help.

Files changed/added

- `main.py` — improved fetching and fallbacks.
- `requirements.txt` — pinned dependencies.
- `.venv/` — created virtual environment (not checked into source control).
- `.vscode/settings.json`, `.vscode/launch.json` — VS Code config to use the venv.
- `scripts/setup.sh` — setup helper.

If you want, I can:
- Upgrade the project to target Python 3.11 and create a `pyproject.toml`.
- Add logging, a scheduler (cron systemd timer), or a small UI/dashboard.
