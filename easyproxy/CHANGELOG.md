# Changelog

## 1.0.4
- FROM python:3.12-slim-bookworm (identico all'originale Dockerfile.full)
- Rimosso build.yaml: causa warning deprecation e tag inesistenti su ghcr.io
- WARP installato ma disabilitato via ENV hardcoded (ENABLE_WARP=false)
- run.sh: rimosso bashio (non disponibile), usa jq per leggere /data/options.json
- Byparr: patch requires-python >= 3.12 (fix crash pydantic TypedDict su Python < 3.12)
- EasyProxy clonato in /app/easyproxy (evita conflitti con /app root)

## 1.0.3
- Tentativo ghcr.io/home-assistant/amd64-base-debian:bookworm
- Fallito: Python 3.11 causa crash Byparr (pydantic TypedDict)

## 1.0.2
- Tentativo base-python:3.12-bookworm (tag inesistente)

## 1.0.1
- Fix: rimossa riga image: da config.yaml

## 1.0.0
- Prima release
