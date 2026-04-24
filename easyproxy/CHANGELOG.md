# Changelog

## 1.0.3
- Immagine base cambiata a ghcr.io/home-assistant/{arch}-base-debian:bookworm (Debian ufficiale HA)
- Python 3.12 installato via apt (no Alpine, no conflitti sed)
- WARP installato ma disabilitato via ENV (ENABLE_WARP=false)
- Fix sed BusyBox: rimossa flag -I, usato GNU sed nativo Debian
- Fix immagine base inesistente (bookworm era solo per base-debian, non base-python)
- Inclusi FlareSolverr v3 e Byparr (versione FULL)

## 1.0.2
- Tentativo immagine base python:3.12-bookworm (non trovata su ghcr.io)

## 1.0.1
- Fix: rimossa riga image: da config.yaml (causava pull da ghcr.io)

## 1.0.0
- Prima release
