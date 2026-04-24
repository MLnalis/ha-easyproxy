#!/usr/bin/with-contenv bashio
# ─────────────────────────────────────────────────────────────────────────────
# EasyProxy Full — run.sh  v2.1.3
#
# Equivalenza con il docker-compose originale:
#   API_PASSWORD  → bashio::config 'api_password'    (era: - API_PASSWORD=ep)
#   PORT          → bashio::config 'port'             (era: - PORT=7860)
#   MPD_MODE      → bashio::config 'mpd_mode'         (era: #- MPD_MODE=legacy)
#   GLOBAL_PROXY  → bashio::config 'global_proxy'     (era: #- GLOBAL_PROXY=)
#   TRANSPORT_ROUTES → bashio::config 'transport_routes'
#
# In più rispetto all'originale:
#   - Xvfb per Chrome headless (Chrome non può girare senza display in container)
#   - FlareSolverr v3 su porta interna 8191
#   - Byparr su porta interna 8192
#   - DVR directory su /share (montata da HA)
# ─────────────────────────────────────────────────────────────────────────────

# ── Lettura config da Home Assistant (/data/options.json) ────────────────────
API_PASSWORD=$(bashio::config 'api_password')
PORT=$(bashio::config 'port')
MPD_MODE=$(bashio::config 'mpd_mode')
LOG_LEVEL=$(bashio::config 'log_level')
DVR_ENABLED=$(bashio::config 'dvr_enabled')
GLOBAL_PROXY=$(bashio::config 'global_proxy')
TRANSPORT_ROUTES=$(bashio::config 'transport_routes')
WORKERS=$(bashio::config 'workers')

# Esporta tutte le variabili — identiche a quelle del docker-compose originale
export API_PASSWORD
export PORT
export MPD_MODE
export LOG_LEVEL
export DVR_ENABLED
export GLOBAL_PROXY
export TRANSPORT_ROUTES

# Variabili aggiuntive per FlareSolverr e Byparr (non presenti nell'originale base)
export FLARESOLVERR_URL="http://localhost:8191"
export BYPARR_URL="http://localhost:8192"
export BYPARR_PORT="8192"
export HEADLESS="false"
export DISPLAY=":99"
export CHROME_PATH="/usr/bin/google-chrome"
export CHROME_FLAGS="--no-sandbox --disable-dev-shm-usage --disable-gpu"

bashio::log.info "════════════════════════════════════"
bashio::log.info " EasyProxy Full v2.1.3"
bashio::log.info "════════════════════════════════════"
bashio::log.info "PORT=${PORT}  MPD_MODE=${MPD_MODE}  DVR=${DVR_ENABLED}"

# Verifica Chrome nel PATH (debug — aiuta a identificare problemi di build)
if command -v google-chrome &>/dev/null; then
    bashio::log.info "Chrome: $(google-chrome --version)"
else
    bashio::log.error "google-chrome NON trovato nel PATH — FlareSolverr non funzionerà!"
    bashio::log.error "Controlla il Dockerfile: il .deb di Google Chrome deve essere installato."
fi

# Directory DVR su /share (montata da HA tramite map: share:rw in config.yaml)
mkdir -p /share/easyproxy/recordings
export RECORDINGS_DIR="/share/easyproxy/recordings"

# ── 1. Xvfb — display virtuale :99 ──────────────────────────────────────────
# Necessario perché Chrome non accetta HEADLESS=true in alcuni ambienti container
# senza un display reale. Xvfb simula un display X11 virtuale.
bashio::log.info "Avvio Xvfb su :99 ..."
Xvfb :99 -screen 0 1280x720x24 -nolisten tcp &
XVFB_PID=$!
sleep 2

if kill -0 "${XVFB_PID}" 2>/dev/null; then
    bashio::log.info "Xvfb attivo (PID=${XVFB_PID})"
else
    bashio::log.warning "Xvfb non avviato — Chrome potrebbe non funzionare"
fi

# ── 2. FlareSolverr v3 — porta 8191 ─────────────────────────────────────────
# FlareSolverr v3 usa undetected_chromedriver + xvfbwrapper.
# Legge: PORT (override a 8191), DISPLAY, CHROME_PATH, HEADLESS
bashio::log.info "Avvio FlareSolverr v3 (porta 8191) ..."
cd /app/flaresolverr
PORT=8191 python3 src/flaresolverr.py &
FLARE_PID=$!
bashio::log.info "FlareSolverr PID=${FLARE_PID}"

# ── 3. Byparr — porta 8192 ──────────────────────────────────────────────────
# Byparr usa Camoufox (Firefox stealth), non dipende da Chrome/Xvfb.
# BYPARR_URL e BYPARR_PORT sono letti da EasyProxy per delegare l'estrazione.
bashio::log.info "Avvio Byparr (porta 8192) ..."
cd /app/byparr_src
PORT=8192 python3 main.py &
BYPARR_PID=$!
bashio::log.info "Byparr PID=${BYPARR_PID}"

# Attesa inizializzazione (FlareSolverr + Byparr impiegano 2-5s per partire)
sleep 4

# ── 4. EasyProxy — porta $PORT ───────────────────────────────────────────────
# Avvio identico all'originale: gunicorn + aiohttp worker
# L'originale usa: gunicorn --bind 0.0.0.0:$PORT ... app:app
# Workers: 0 = auto (nproc), altrimenti valore da config HA
cd /app/easyproxy

if [ "${WORKERS}" = "0" ] || [ -z "${WORKERS}" ]; then
    WORKERS=$(nproc)
    [ "${WORKERS}" -lt 1 ] && WORKERS=1
fi

bashio::log.info "Avvio EasyProxy porta ${PORT} — ${WORKERS} worker(s) ..."

exec gunicorn \
    --bind "0.0.0.0:${PORT}" \
    --workers "${WORKERS}" \
    --worker-class "aiohttp.worker.GunicornWebWorker" \
    --timeout 120 \
    --graceful-timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app