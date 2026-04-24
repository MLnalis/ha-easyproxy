#!/usr/bin/with-contenv bashio

# ── Config dall'UI di HA ─────────────────────────────────────────────────────
API_PASSWORD=$(bashio::config 'api_password')
WORKERS=$(bashio::config 'workers')

# ── WARP forzato OFF (impostato anche nel Dockerfile, doppia sicurezza) ───────
export ENABLE_WARP=false
export WARP_ENABLED=false
export USE_WARP=false

export API_PASSWORD="${API_PASSWORD}"
export PORT=7860
export WORKERS="${WORKERS}"
export PYTHONPATH=/app

bashio::log.info "=============================="
bashio::log.info " EasyProxy FULL (no WARP)"
bashio::log.info "=============================="

# ── FlareSolverr (porta 8191) ────────────────────────────────────────────────
bashio::log.info "Avvio FlareSolverr sulla porta 8191..."
cd /app/flaresolverr && PORT=8191 python3 src/flaresolverr.py &

# ── Byparr (porta 8192) ──────────────────────────────────────────────────────
bashio::log.info "Avvio Byparr sulla porta 8192..."
cd /app/byparr_src && PORT=8192 python3 main.py &

# ── EasyProxy (porta 7860) — processo principale ─────────────────────────────
bashio::log.info "Avvio EasyProxy sulla porta 7860..."
cd /app
exec gunicorn \
    --bind 0.0.0.0:7860 \
    --workers "${WORKERS}" \
    --worker-class aiohttp.worker.GunicornWebWorker \
    --timeout 120 \
    --graceful-timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app
