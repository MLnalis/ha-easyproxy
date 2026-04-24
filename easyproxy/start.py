"""
EasyProxy Full — Home Assistant Add-on startup script.
Avvia nell'ordine:
  1. Xvfb         → display virtuale :99 (necessario per FlareSolverr/Chrome)
  2. FlareSolverr → porta 8191
  3. Byparr       → porta 8192
  4. EasyProxy    → porta configurata (default 7860) via Gunicorn
"""
import json
import os
import subprocess
import sys
import time

CONFIG = "/data/options.json"

# ── Leggi opzioni HA ────────────────────────────────────────────────────────
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
# FlareSolverr: headless=false + Xvfb (più stabile in container HA senza GPU)
os.environ["HEADLESS"]         = "false"
os.environ["DISPLAY"]          = ":99"

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

# ── 1. Xvfb (display virtuale per Chrome/FlareSolverr) ──────────────────────
print("[INFO] Avvio Xvfb su :99...")
xvfb = subprocess.Popen(
    ["Xvfb", ":99", "-screen", "0", "1280x720x24", "-nolisten", "tcp"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
# Attende che il display sia pronto
time.sleep(2)
if xvfb.poll() is not None:
    print("[WARN] Xvfb non è avviato, FlareSolverr potrebbe non funzionare")
else:
    print("[INFO] Xvfb avviato (PID {})".format(xvfb.pid))

# ── 2. FlareSolverr ─────────────────────────────────────────────────────────
print("[INFO] Avvio FlareSolverr v3 (porta 8191)...")
flare_env = os.environ.copy()
flare_env["PORT"]    = "8191"
flare_env["DISPLAY"] = ":99"
flare_env["HEADLESS"] = "false"
subprocess.Popen(
    [sys.executable, "src/flaresolverr.py"],
    cwd="/app/flaresolverr",
    env=flare_env,
)

# ── 3. Byparr ───────────────────────────────────────────────────────────────
print("[INFO] Avvio Byparr (porta 8192)...")
byparr_env = os.environ.copy()
byparr_env["PORT"] = "8192"
subprocess.Popen(
    [sys.executable, "main.py"],
    cwd="/app/byparr_src",
    env=byparr_env,
)

# Attesa breve per permettere ai servizi di inizializzarsi
time.sleep(3)

# ── 4. EasyProxy via Gunicorn ────────────────────────────────────────────────
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
