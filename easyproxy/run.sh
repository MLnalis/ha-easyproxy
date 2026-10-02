#!/bin/bash
OPTS=/data/options.json

export API_PASSWORD="$(jq -r '.api_password // "ep"' "$OPTS")"
export WARP_LICENSE_KEY="$(jq -r '.warp_license_key // ""' "$OPTS")"
export PORT=7860

/bin/bash /app/entrypoint.sh &
pid=$!

# Inoltra lo stop a Python, così l'entrypoint esegue il suo cleanup (wireproxy)
trap 'pkill -TERM -f "python app.py"; kill -TERM $pid 2>/dev/null' TERM INT

wait $pid
wait $pid
