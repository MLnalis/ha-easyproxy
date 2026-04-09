import json
import os
import subprocess
import sys

CONFIG = "/data/options.json"

# Leggi opzioni da Home Assistant
opts = {}
if os.path.exists(CONFIG):
    with open(CONFIG) as f:
        opts = json.load(f)
    print("[INFO] Configurazione letta da Home Assistant")
else:
    print("[WARN] options.json non trovato, uso valori di default")

# Imposta variabili d'ambiente
os.environ["API_PASSWORD"]  = str(opts.get("api_password", "ep"))
os.environ["PORT"]          = str(opts.get("port", 7860))
os.environ["MPD_MODE"]      = str(opts.get("mpd_mode", "legacy"))
os.environ["LOG_LEVEL"]     = str(opts.get("log_level", "WARNING"))
os.environ["DVR_ENABLED"]   = str(opts.get("dvr_enabled", False)).lower()
os.environ["GLOBAL_PROXY"]  = str(opts.get("global_proxy", ""))
os.environ["TRANSPORT_ROUTES"] = str(opts.get("transport_routes", ""))

# Directory DVR persistente in /share
recordings_dir = "/share/easyproxy/recordings"
os.makedirs(recordings_dir, exist_ok=True)
os.environ["RECORDINGS_DIR"] = recordings_dir

port = os.environ["PORT"]
print(f"[INFO] PORT={port}")
print(f"[INFO] MPD_MODE={os.environ['MPD_MODE']}")
print(f"[INFO] DVR_ENABLED={os.environ['DVR_ENABLED']}")
print(f"[INFO] Avvio EasyProxy su porta {port}...")

# Avvia gunicorn
os.execlp("gunicorn", "gunicorn",
    "--bind", f"0.0.0.0:{port}",
    "--workers", "4",
    "--worker-class", "aiohttp.worker.GunicornWebWorker",
    "--timeout", "120",
    "--access-logfile", "-",
    "--error-logfile", "-",
    "app:app"
)
