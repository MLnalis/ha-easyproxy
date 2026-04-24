# Changelog

## 1.0.5
- Fix FlareSolverr: Chromium non si avviava in container HAOS
  - Aggiunti flag: --disable-dev-shm-usage, --headless=new, --no-zygote,
    --single-process, --disable-gpu, --disable-software-rasterizer
  - Patch applicata tramite script Python (patch_flaresolverr.py) invece di sed
- Rimosso build.yaml (causava errori tag ghcr.io inesistenti)
- WARP installato ma bloccato via ENV hardcoded

## 1.0.4
- FROM python:3.12-slim-bookworm (identico all'originale)
- run.sh: jq invece di bashio per leggere /data/options.json
- Byparr: patch requires-python >= 3.12

## 1.0.3
- Tentativo base-debian:bookworm (Python 3.11, Byparr crash pydantic)

## 1.0.2 / 1.0.1 / 1.0.0
- Fix progressivi tag ghcr.io, sed Alpine, riga image: