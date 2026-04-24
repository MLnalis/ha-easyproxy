"""
EasyProxy Full — Home Assistant OS Add-on startup script.

Ordine di avvio:
  1. Xvfb :99        display virtuale per Chrome/FlareSolverr
  2. FlareSolverr    porta 8191  bypass Cloudflare
  3. Byparr          porta 8192  DoodStream / IP-sticky
  4. EasyProxy       porta <PORT> via Gunicorn+aiohttp
"""
import json
import os
import subprocess
import sys
import time

CONFIG = "/data/options.json"

opts = {}
if os.path.exists(CONFIG):
    with open(CONFIG) as f:
        opts = json.load(f)
    print("[INFO] Configurazione letta da Home Assistant")
else:
    print("[WARN] /data/options.json non trovato — uso valori di default")

os.environ.update({
    "API_PASSWORD":     str(opts.get("api_password",     "ep")),
    "PORT":             str(opts.get("port",             7860)),
    "MPD_MODE":         str(opts.get("mpd_mode",         "legacy")),
    "LOG_LEVEL":        str(opts.get("log_level",        "WARNING")),
    "DVR_ENABLED":      str(opts.get("dvr_enabled",      False)).lower(),
    "GLOBAL_PROXY":     str(opts.get("global_proxy",     "")),
    "TRANSPORT_ROUTES": str(opts.get("transport_routes", "")),
    "FLARESOLVERR_URL": "http://localhost:8191",
    "BYPARR_URL":       "http://localhost:8192",
    "BYPARR_PORT":      "8192",
    "HEADLESS":         "false",
    "DISPLAY":          ":99",
})

workers_opt = int(opts.get("workers", 0))
if workers_opt > 0:
    os.environ["WORKERS"] = str(workers_opt)

recordings_dir = "/share/easyproxy/recordings"
os.makedirs(recordings_dir, exist_ok=True)
os.environ["RECORDINGS_DIR"] = recordings_dir

port = os.environ["PORT"]
for k in ("PORT", "MPD_MODE", "DVR_ENABLED", "FLARESOLVERR_URL", "BYPARR_URL"):
    print(f"[INFO] {k}={os.environ[k]}")

print("[INFO] Avvio Xvfb su :99 ...")
xvfb = subprocess.Popen(
    ["Xvfb", ":99", "-screen", "0", "1280x720x24", "-nolisten", "tcp"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(2)
if xvfb.poll() is not None:
    print("[WARN] Xvfb non avviato — FlareSolverr potrebbe non funzionare")
else:
    print(f"[INFO] Xvfb attivo (PID {xvfb.pid})")

print("[INFO] Avvio FlareSolverr v3 (porta 8191) ...")
subprocess.Popen(
    [sys.executable, "src/flaresolverr.py"],
    cwd="/app/flaresolverr",
    env={**os.environ, "PORT": "8191"},
)

print("[INFO] Avvio Byparr (porta 8192) ...")
subprocess.Popen(
    [sys.executable, "main.py"],
    cwd="/app/byparr_src",
    env={**os.environ, "PORT": "8192"},
)

time.sleep(3)

try:
    cpu_count = len(os.sched_getaffinity(0))
except AttributeError:
    cpu_count = os.cpu_count() or 1

workers_count = os.environ.get("WORKERS") or str(max(1, cpu_count))
print(f"[INFO] Avvio EasyProxy porta {port} con {workers_count} worker(s) ...")

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