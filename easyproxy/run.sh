#!/usr/bin/with-contenv bashio

# ─── Leggi configurazione da options.json ───────────────────────────────────
API_PASSWORD=$(bashio::config 'api_password')
WORKERS=$(bashio::config 'workers')
WORKER_CLASS=$(bashio::config 'worker_class')

# ─── Forza disabilitazione WARP ─────────────────────────────────────────────
export ENABLE_WARP=false
export WARP_ENABLED=false
export USE_WARP=false
export DISABLE_WARP=true

# ─── Passa la password come variabile d'ambiente (usata da MediaFlow Proxy) ─
export API_PASSWORD="${API_PASSWORD}"
export MEDIAFLOW_PROXY_API_PASSWORD="${API_PASSWORD}"

bashio::log.info "Avvio EasyProxy (FULL, senza WARP)..."
bashio::log.info "Porta: 7860 | Worker: ${WORKERS} | Worker class: ${WORKER_CLASS}"

cd /app

# Prova ad avviare con gunicorn (se disponibile), altrimenti usa uvicorn
if command -v gunicorn &>/dev/null; then
    exec gunicorn main:app \
        --bind 0.0.0.0:7860 \
        --workers "${WORKERS}" \
        --worker-class "${WORKER_CLASS}" \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -
else
    exec python3 -m uvicorn main:app \
        --host 0.0.0.0 \
        --port 7860 \
        --workers "${WORKERS}"
fi
