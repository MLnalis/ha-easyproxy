#!/bin/bash
set -e

echo "======================================="
echo "  EasyProxy - Home Assistant Add-on"
echo "======================================="

CONFIG_FILE="/data/options.json"

read_option() {
    local key="$1"
    local default="$2"
    python3 -c "
import json
try:
    d = json.load(open('${CONFIG_FILE}'))
    val = d.get('${key}', '${default}')
    print(val if val is not None else '${default}')
except Exception:
    print('${default}')
"
}

if [ -f "$CONFIG_FILE" ]; then
    echo "[INFO] Lettura configurazione da Home Assistant..."

    export API_PASSWORD="$(read_option 'api_password' '')"
    export PORT="$(read_option 'port' '7860')"
    export MPD_MODE="$(read_option 'mpd_mode' 'legacy')"
    export LOG_LEVEL="$(read_option 'log_level' 'WARNING')"
    export DVR_ENABLED="$(read_option 'dvr_enabled' 'false')"
    export GLOBAL_PROXY="$(read_option 'global_proxy' '')"
    export TRANSPORT_ROUTES="$(read_option 'transport_routes' '')"

    echo "[INFO] PORT=${PORT}"
    echo "[INFO] MPD_MODE=${MPD_MODE}"
    echo "[INFO] LOG_LEVEL=${LOG_LEVEL}"
    echo "[INFO] DVR_ENABLED=${DVR_ENABLED}"
else
    echo "[WARN] options.json non trovato, uso valori di default"
    export PORT="${PORT:-7860}"
fi

export RECORDINGS_DIR="/share/easyproxy/recordings"
mkdir -p "${RECORDINGS_DIR}"
echo "[INFO] RECORDINGS_DIR=${RECORDINGS_DIR}"

cd /app

echo "[INFO] Avvio EasyProxy su porta ${PORT}..."
exec gunicorn \
    --bind "0.0.0.0:${PORT}" \
    --workers 4 \
    --worker-class aiohttp.worker.GunicornWebWorker \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app