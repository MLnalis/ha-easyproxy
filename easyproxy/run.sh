#!/usr/bin/with-contenv bashio

# Leggi configurazione da /data/options.json
API_PASSWORD=$(bashio::config 'api_password')
PORT=$(bashio::config 'port')
GLOBAL_PROXY=$(bashio::config 'global_proxy' || echo "")
TRANSPORT_ROUTES=$(bashio::config 'transport_routes' || echo "")
MPD_MODE=$(bashio::config 'mpd_mode' || echo "")

export API_PASSWORD
export PORT

if bashio::config.has_value 'global_proxy'; then
    export GLOBAL_PROXY
fi

if bashio::config.has_value 'transport_routes'; then
    export TRANSPORT_ROUTES
fi

if bashio::config.has_value 'mpd_mode'; then
    export MPD_MODE
fi

bashio::log.info "Avvio EasyProxy sulla porta ${PORT}..."
bashio::log.info "Password API impostata."

exec /start.sh
