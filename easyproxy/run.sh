#!/bin/bash
set -e

OPTIONS_FILE="/data/options.json"
if [ -f "$OPTIONS_FILE" ]; then
    API_PASSWORD=$(jq -r '.api_password // "changeme"' "$OPTIONS_FILE")
    WORKERS=$(jq -r '.workers // 1' "$OPTIONS_FILE")
else
    API_PASSWORD="changeme"
    WORKERS=1
fi

export ENABLE_WARP=false
export WARP_ENABLED=false
export USE_WARP=false
export API_PASSWORD="${API_PASSWORD}"
export PORT=7860
export WORKERS="${WORKERS}"
export PYTHONPATH=/app/easyproxy

echo "[INFO] =============================="
echo "[INFO]  EasyProxy FULL (no WARP)"
echo "[INFO]  API_PASSWORD set: $([ -n "$API_PASSWORD" ] && echo 'yes' || echo 'no')"
echo "[INFO]  WORKERS: ${WORKERS}"
echo "[INFO] =============================="

echo "[INFO] Avvio FlareSolverr sulla porta 8191..."
cd /app/flaresolverr && PORT=8191 python src/flaresolverr.py &

echo "[INFO] Avvio Byparr sulla porta 8192..."
cd /app/byparr_src && PORT=8192 python main.py &

echo "[INFO] Avvio EasyProxy sulla porta 7860..."
cd /app/easyproxy
exec gunicorn \
    --bind 0.0.0.0:7860 \
    --workers "${WORKERS}" \
    --worker-class aiohttp.worker.GunicornWebWorker \
    --timeout 120 \
    --graceful-timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app