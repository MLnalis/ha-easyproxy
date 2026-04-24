"""
EasyProxy Full — Home Assistant Add-on startup script.
Legge /data/options.json, imposta le variabili d'ambiente e avvia
FlareSolverr, Byparr e infine EasyProxy via Gunicorn.
"""
import json
import os
import shutil
import subprocess
import sys

CONFIG = "/data/options.json"

opts = {}
if os.path.exists(CONFIG):
    with open(CONFIG) as f:
        opts = json.load(f)
    print("[INFO] Configurazione letta da Home Assistant")
else:
    print("[WARN] options.json non trovato, uso valori di default")

os.environ["API_PASSWORD"]     = str(opts.get("api_password", "ep"))
os.environ["PORT"]             = str(opts.get("port", 7860))
os.environ["MPD_MODE"]         = str(opts.get("mpd_mode", "legacy"))
os.environ["LOG_LEVEL"]        = str(opts.get("log_level", "WARNING"))
os.environ["DVR_ENABLED"]      = str(opts.get("dvr_enabled", False)).lower()
os.environ["GLOBAL_PROXY"]     = str(opts.get("global_proxy", ""))
os.environ["TRANSPORT_ROUTES"] = str(opts.get("transport_routes", ""))
os.environ["FLARESOLVERR_URL"] = "http://localhost:8191"
os.environ["BYPARR_URL"]       = "http://localhost:8192"
os.environ["BYPARR_PORT"]      = "8192"

workers_opt = int(opts.get("workers", 0))
if workers_opt > 0:
    os.environ["WORKERS"] = str(workers_opt)

recordings_dir = "/share/easyproxy/recordings"
os.makedirs(recordings_dir, exist_ok=True)
os.environ["RECORDINGS_DIR"] = recordings_dir

port = os.environ["PORT"]
print(f"[INFO] PORT={port}")
print(f"[INFO] MPD_MODE={os.environ['MPD_MODE']}")
print(f"[INFO] DVR_ENABLED={os.environ['DVR_ENABLED']}")
print(f"[INFO] FLARESOLVERR_URL={os.environ['FLARESOLVERR_URL']}")
print(f"[INFO] BYPARR_URL={os.environ['BYPARR_URL']}")

# ---------- Copia template info.html personalizzato ----------
_info_src = "/info.html"
_info_dst = "/app/easyproxy/templates/info.html"
if os.path.exists(_info_src) and os.path.exists("/app/easyproxy/templates"):
    shutil.copy2(_info_src, _info_dst)
    print(f"[INFO] Template info.html copiato in {_info_dst}")
else:
    print(f"[WARN] Template info.html non copiato (src={_info_src} dst_dir={os.path.dirname(_info_dst)})")

# ---------- FlareSolverr ----------
print("[INFO] Avvio FlareSolverr v3 (porta 8191)...")
flare_env = os.environ.copy()
flare_env["PORT"] = "8191"
subprocess.Popen(
    [sys.executable, "src/flaresolverr.py"],
    cwd="/app/flaresolverr",
    env=flare_env,
)

# ---------- Byparr ----------
print("[INFO] Avvio Byparr (porta 8192)...")
byparr_env = os.environ.copy()
byparr_env["PORT"] = "8192"
subprocess.Popen(
    [sys.executable, "main.py"],
    cwd="/app/byparr_src",
    env=byparr_env,
)

# ---------- EasyProxy via Gunicorn ----------
try:
    cpu_count = len(os.sched_getaffinity(0))
except AttributeError:
    cpu_count = os.cpu_count() or 1

workers_count = str(os.environ.get("WORKERS") or max(1, cpu_count))
print(f"[INFO] Avvio EasyProxy su porta {port} con {workers_count} worker(s)...")

os.chdir("/app/easyproxy")
os.execlp(
    "gunicorn", "gunicorn",
    "--bind",             f"0.0.0.0:{port}",
    "--workers",          workers_count,
    "--worker-class",     "aiohttp.worker.GunicornWebWorker",
    "--timeout",          "120",
    "--graceful-timeout", "120",
    "--access-logfile",   "-",
    "--error-logfile",    "-",
    "app:app",
)
