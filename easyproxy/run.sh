#!/bin/bash
set -e

CONFIG_FILE="/data/options.json"

if [ -f "$CONFIG_FILE" ]; then
    PORT=$(jq -r '.port // 7860' "$CONFIG_FILE")
    API_PASSWORD=$(jq -r '.api_password // "ep"' "$CONFIG_FILE")
    export PORT="$PORT"
    export API_PASSWORD="$API_PASSWORD"
fi

mkdir -p /data/config /data/recordings /data/logs
echo "🚀 Avvio EasyProxy..."
exec python3 /app/app.py
