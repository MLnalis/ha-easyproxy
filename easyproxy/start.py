"""
EasyProxy Full — Home Assistant Add-on startup script.
Legge /data/options.json, imposta le variabili d'ambiente e avvia
FlareSolverr, Byparr e infine EasyProxy via Gunicorn.
"""
import json
import os
import subprocess
import sys
import time
import socket

CONFIG = "/data/options.json"

# ---------- Leggi configurazione HA ----------
opts = {}
if os.path.exists(CONFIG):
    with open(CONFIG) as f:
        opts = json.load(f)
    print("[INFO] Configurazione letta da Home Assistant")
else:
    print("[WARN] options.json non trovato, uso valori di default")

# ---------- Variabili base ----------
os.environ["API_PASSWORD"]   = str(opts.get("api_password", "ep"))
os.environ["PORT"]           = str(opts.get("port", 7860))
os.environ["MPD_MODE"]       = str(opts.get("mpd_mode", "legacy"))
os.environ["LOG_LEVEL"]      = str(opts.get("log_level", "WARNING"))
os.environ["DVR_ENABLED"]    = str(opts.get("dvr_enabled", False)).lower()
os.environ["GLOBAL_PROXY"]   = str(opts.get("global_proxy", ""))
os.environ["TRANSPORT_ROUTES"] = str(opts.get("transport_routes", ""))

# ---------- WARP ----------
enable_warp = opts.get("enable_warp", False)
os.environ["ENABLE_WARP"]    = str(enable_warp).lower()
os.environ["WARP_LICENSE_KEY"] = str(opts.get("warp_license_key", ""))
os.environ["WARP_EXCLUDED_HOSTS"] = str(opts.get("warp_excluded_hosts", ""))
os.environ["SOLVERS_FORCE_WARP_PROXY"] = str(opts.get("solvers_force_warp_proxy", False)).lower()

# ---------- Workers ----------
workers_opt = opts.get("workers", 0)
if workers_opt and int(workers_opt) > 0:
    os.environ["WORKERS"] = str(workers_opt)

# ---------- DVR directory persistente in /share ----------
recordings_dir = "/share/easyproxy/recordings"
os.makedirs(recordings_dir, exist_ok=True)
os.environ["RECORDINGS_DIR"] = recordings_dir

port = os.environ["PORT"]
print(f"[INFO] PORT={port}")
print(f"[INFO] MPD_MODE={os.environ['MPD_MODE']}")
print(f"[INFO] DVR_ENABLED={os.environ['DVR_ENABLED']}")
print(f"[INFO] ENABLE_WARP={os.environ['ENABLE_WARP']}")

# ---------- Cloudflare WARP ----------
if enable_warp:
    print("[INFO] Avvio Cloudflare WARP...")

    _excluded = os.environ.get(
        "WARP_EXCLUDED_HOSTS",
        "cinemacity.cc,*.cinemacity.cc,cccdn.net,*.cccdn.net,"
        "strem.fun,*.strem.fun,real-debrid.com,*.real-debrid.com,"
        "realdebrid.com,*.realdebrid.com,alldebrid.com,*.alldebrid.com,"
        "debrid-link.com,*.debrid-link.com,torbox.app,*.torbox.app,"
        "dlstreams.com,*.dlstreams.com,dlhd.dad,*.dlhd.dad,"
        "premiumize.me,*.premiumize.me,put.io,*.put.io,offcloud.com,*.offcloud.com",
    )
    os.environ["WARP_EXCLUDED_HOSTS"] = _excluded

    subprocess.Popen(["warp-svc", "--accept-tos"],
                     stdout=open("/var/log/warp-svc.log", "w"),
                     stderr=subprocess.STDOUT)

    # Attendi warp-svc
    for i in range(20):
        ret = subprocess.call(
            ["warp-cli", "--accept-tos", "status"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        if ret == 0:
            break
        print(f"[INFO] Attesa warp-svc... ({i+1}/20)")
        time.sleep(1)
    else:
        print("[WARN] warp-svc non risponde, WARP disabilitato.")
        os.environ["ENABLE_WARP"] = "false"
        enable_warp = False

    if enable_warp:
        # Registrazione
        status = subprocess.check_output(
            ["warp-cli", "--accept-tos", "status"], text=True
        )
        if "Registration Name" not in status:
            subprocess.call(["warp-cli", "--accept-tos", "registration", "delete"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.call(["warp-cli", "--accept-tos", "registration", "new"])

        # Licenza opzionale
        lic = os.environ.get("WARP_LICENSE_KEY", "").strip()
        if lic:
            subprocess.call(["warp-cli", "--accept-tos", "registration", "license", lic])

        # Escludi domini
        for domain in _excluded.split(","):
            domain = domain.strip()
            if not domain:
                continue
            subprocess.call(
                ["warp-cli", "--accept-tos", "tunnel", "host", "add", domain],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            ) or subprocess.call(
                ["warp-cli", "--accept-tos", "add-excluded-domain", domain],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        # Modalità proxy SOCKS5
        subprocess.call(["warp-cli", "--accept-tos", "mode", "proxy"])
        subprocess.call(["warp-cli", "--accept-tos", "proxy", "port", "1080"])
        subprocess.call(["warp-cli", "--accept-tos", "connect"])

        print("[INFO] Attesa stabilizzazione WARP (10s)...")
        time.sleep(10)

        # Verifica SOCKS5
        try:
            s = socket.create_connection(("127.0.0.1", 1080), timeout=2)
            s.close()
            print("[INFO] WARP SOCKS5 in ascolto su porta 1080.")
        except OSError:
            print("[WARN] WARP SOCKS5 non rilevato su porta 1080.")

# ---------- FlareSolverr ----------
print("[INFO] Avvio FlareSolverr...")
flare_env = os.environ.copy()
flare_env["PORT"] = "8191"

force_warp_proxy = os.environ.get("SOLVERS_FORCE_WARP_PROXY", "false") == "true"
if enable_warp and force_warp_proxy:
    flare_env["HTTP_PROXY"]  = "socks5://127.0.0.1:1080"
    flare_env["HTTPS_PROXY"] = "socks5://127.0.0.1:1080"
    flare_env["NO_PROXY"]    = "localhost,127.0.0.1"
    print("[INFO] FlareSolverr instradato tramite WARP.")

subprocess.Popen(
    [sys.executable, "src/flaresolverr.py"],
    cwd="/app/flaresolverr",
    env=flare_env,
)

# ---------- Byparr ----------
print("[INFO] Avvio Byparr...")
byparr_env = os.environ.copy()
byparr_env["PORT"] = "8192"
if enable_warp and force_warp_proxy:
    byparr_env["HTTP_PROXY"]  = "socks5://127.0.0.1:1080"
    byparr_env["HTTPS_PROXY"] = "socks5://127.0.0.1:1080"
    byparr_env["NO_PROXY"]    = "localhost,127.0.0.1"
    print("[INFO] Byparr instradato tramite WARP.")

subprocess.Popen(
    [sys.executable, "main.py"],
    cwd="/app/byparr_src",
    env=byparr_env,
)

# ---------- EasyProxy via Gunicorn ----------
workers_count = os.environ.get("WORKERS") or str(
    max(1, len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 1)
)
print(f"[INFO] Avvio EasyProxy su porta {port} con {workers_count} worker(s)...")

os.chdir("/app/easyproxy")
os.execlp(
    "gunicorn", "gunicorn",
    "--bind", f"0.0.0.0:{port}",
    "--workers", workers_count,
    "--worker-class", "aiohttp.worker.GunicornWebWorker",
    "--timeout", "120",
    "--graceful-timeout", "120",
    "--access-logfile", "-",
    "--error-logfile", "-",
    "app:app",
)
