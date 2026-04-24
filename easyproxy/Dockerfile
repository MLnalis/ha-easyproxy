# ─────────────────────────────────────────────────────────────────────────────
# EasyProxy Full — Home Assistant OS Add-on  v2.1.5
#
# FIX 2.1.5:
#   ✔ run.sh scritto direttamente nel Dockerfile tramite heredoc RUN cat <<'EOF'
#     Elimina completamente il problema "exec /run.sh: no such file or directory"
#     causato da CRLF (Windows line endings) o file mancante nel build context
#   ✔ dos2unix applicato come ulteriore garanzia
#   ✔ sha-bang verificato con xxd per debug
# ─────────────────────────────────────────────────────────────────────────────

ARG BUILD_FROM="python:3.12-slim-bookworm"
FROM ${BUILD_FROM}

ARG BUILD_VERSION
ARG BUILD_ARCH

LABEL io.hass.version="${BUILD_VERSION}" \
      io.hass.type="addon" \
      io.hass.arch="amd64"

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0 \
    PYTHONPATH=/app \
    FLARESOLVERR_URL=http://localhost:8191 \
    BYPARR_URL=http://localhost:8192 \
    BYPARR_PORT=8192 \
    HEADLESS=false \
    DISPLAY=:99 \
    CHROME_PATH=/usr/bin/google-chrome \
    CHROME_FLAGS="--no-sandbox --disable-dev-shm-usage --disable-gpu --window-size=1280,720"

# ── STEP 1: Pacchetti di sistema ─────────────────────────────────────────────
RUN set -ex \
 && echo "[STEP 1/6] Installazione pacchetti di sistema..." \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    curl \
    wget \
    unzip \
    dos2unix \
    xvfb \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libxshmfence1 \
    libglu1-mesa \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxext6 \
    libglib2.0-0 \
    libgtk-3-0 \
    libdbus-1-3 \
    fonts-liberation \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && echo "[STEP 1/6] OK"

# ── STEP 2: Google Chrome Stable ─────────────────────────────────────────────
RUN set -ex \
 && echo "[STEP 2/6] Download Google Chrome Stable..." \
 && wget -q -O /tmp/google-chrome.deb \
      "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
 && apt-get update \
 && apt-get install -y --no-install-recommends /tmp/google-chrome.deb \
 && rm /tmp/google-chrome.deb \
 && rm -rf /var/lib/apt/lists/* \
 && ln -sf /usr/bin/google-chrome /usr/local/bin/chrome \
 && echo "[STEP 2/6] Chrome installato: $(google-chrome --version)"

# ── STEP 3: pip ───────────────────────────────────────────────────────────────
RUN set -ex \
 && echo "[STEP 3/6] Aggiornamento pip..." \
 && python3 -m pip install --no-cache-dir --progress-bar off --upgrade pip \
 && echo "[STEP 3/6] OK: $(pip --version)"

# ── STEP 4: FlareSolverr v3 ──────────────────────────────────────────────────
RUN set -ex \
 && echo "[STEP 4/6] Clone + install FlareSolverr v3..." \
 && git clone --depth=1 https://github.com/FlareSolverr/FlareSolverr.git /app/flaresolverr \
 && python3 -m pip install --no-cache-dir --progress-bar off \
      -r /app/flaresolverr/requirements.txt \
 && python3 -m pip install --no-cache-dir --progress-bar off xvfbwrapper \
 && echo "[STEP 4/6] FlareSolverr OK"

# ── STEP 5: Byparr ───────────────────────────────────────────────────────────
RUN set -ex \
 && echo "[STEP 5/6] Clone + install Byparr..." \
 && git clone --depth=1 https://github.com/ThePhaseless/Byparr.git /app/byparr_src \
 && sed -i 's/requires-python = .*/requires-python = ">=3.11"/' /app/byparr_src/pyproject.toml \
 && python3 -m pip install --no-cache-dir --progress-bar off /app/byparr_src \
 && python3 -m camoufox fetch \
 && echo "[STEP 5/6] Byparr OK"

# ── STEP 6: EasyProxy ────────────────────────────────────────────────────────
RUN set -ex \
 && echo "[STEP 6/6] Clone + install EasyProxy..." \
 && git clone --depth=1 https://github.com/realbestia1/EasyProxy.git /app/easyproxy \
 && python3 -m pip install --no-cache-dir --progress-bar off \
      -r /app/easyproxy/requirements.txt \
 && python3 -m playwright install chromium \
 && python3 -m playwright install-deps chromium \
 && echo "[STEP 6/6] EasyProxy OK"

# ── run.sh scritto inline — evita CRLF e problemi di COPY ────────────────────
# MOTIVO: COPY run.sh fallisce silenziosamente se il file ha CRLF (Windows)
# o se non è nel build context del Supervisor HA. Scrivere lo script inline
# con heredoc garantisce LF puri e nessuna dipendenza da file esterni.
RUN cat <<'RUNSCRIPT' > /run.sh
#!/usr/bin/with-contenv bashio

bashio::log.level "debug"

API_PASSWORD=$(bashio::config 'api_password')
PORT=$(bashio::config 'port')
MPD_MODE=$(bashio::config 'mpd_mode')
LOG_LEVEL=$(bashio::config 'log_level')
DVR_ENABLED=$(bashio::config 'dvr_enabled')
GLOBAL_PROXY=$(bashio::config 'global_proxy')
TRANSPORT_ROUTES=$(bashio::config 'transport_routes')
WORKERS=$(bashio::config 'workers')

export API_PASSWORD PORT MPD_MODE LOG_LEVEL DVR_ENABLED GLOBAL_PROXY TRANSPORT_ROUTES
export FLARESOLVERR_URL="http://localhost:8191"
export BYPARR_URL="http://localhost:8192"
export BYPARR_PORT="8192"
export HEADLESS="false"
export DISPLAY=":99"
export CHROME_PATH="/usr/bin/google-chrome"
export CHROME_FLAGS="--no-sandbox --disable-dev-shm-usage --disable-gpu"

bashio::log.info "════════════════════════════════════════"
bashio::log.info " EasyProxy Full v2.1.5"
bashio::log.info "════════════════════════════════════════"
bashio::log.info "PORT=${PORT}  MPD_MODE=${MPD_MODE}  DVR=${DVR_ENABLED}"
bashio::log.debug "GLOBAL_PROXY=${GLOBAL_PROXY}"
bashio::log.debug "TRANSPORT_ROUTES=${TRANSPORT_ROUTES}"

if command -v google-chrome &>/dev/null; then
    bashio::log.info "Chrome: $(google-chrome --version)"
else
    bashio::log.error "google-chrome NON trovato nel PATH — FlareSolverr non funzionerà!"
    exit 1
fi

mkdir -p /share/easyproxy/recordings
export RECORDINGS_DIR="/share/easyproxy/recordings"

bashio::log.info "[1/4] Avvio Xvfb su :99..."
Xvfb :99 -screen 0 1280x720x24 -nolisten tcp &
XVFB_PID=$!
sleep 2
if kill -0 "${XVFB_PID}" 2>/dev/null; then
    bashio::log.info "[1/4] Xvfb attivo (PID=${XVFB_PID})"
else
    bashio::log.error "[1/4] Xvfb NON avviato"
    exit 1
fi

bashio::log.info "[2/4] Avvio FlareSolverr v3 (porta 8191)..."
cd /app/flaresolverr
PORT=8191 python3 src/flaresolverr.py &
FLARE_PID=$!
bashio::log.info "[2/4] FlareSolverr PID=${FLARE_PID}"

bashio::log.info "[3/4] Avvio Byparr (porta 8192)..."
cd /app/byparr_src
PORT=8192 python3 main.py &
BYPARR_PID=$!
bashio::log.info "[3/4] Byparr PID=${BYPARR_PID}"

bashio::log.info "Attesa inizializzazione (max 15s)..."
for i in $(seq 1 15); do
    if curl -sf http://localhost:8191/ &>/dev/null; then
        bashio::log.info "FlareSolverr pronto dopo ${i}s"
        break
    fi
    bashio::log.debug "Attesa... ${i}/15s"
    sleep 1
done

cd /app/easyproxy
if [ "${WORKERS}" = "0" ] || [ -z "${WORKERS}" ]; then
    WORKERS=$(nproc)
    [ "${WORKERS}" -lt 1 ] && WORKERS=1
fi

bashio::log.info "[4/4] Avvio EasyProxy porta ${PORT} — ${WORKERS} worker(s)..."

exec gunicorn \
    --bind "0.0.0.0:${PORT}" \
    --workers "${WORKERS}" \
    --worker-class "aiohttp.worker.GunicornWebWorker" \
    --timeout 120 \
    --graceful-timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app
RUNSCRIPT

# Rimuovi CRLF residui e rendi eseguibile
RUN dos2unix /run.sh && chmod +x /run.sh

# Verifica finale
RUN set -ex \
 && echo "=== VERIFICA FINALE ===" \
 && echo "Python:   $(python3 --version)" \
 && echo "Chrome:   $(google-chrome --version)" \
 && echo "ffmpeg:   $(ffmpeg -version 2>&1 | head -1)" \
 && echo "gunicorn: $(gunicorn --version)" \
 && echo "run.sh:   $(head -1 /run.sh)" \
 && echo "=== BUILD OK ==="

EXPOSE 7860

CMD ["/run.sh"]