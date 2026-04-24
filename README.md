# EasyProxy HAOS Add-on v1.0.4

EasyProxy FULL (FlareSolverr v3 + Byparr) senza WARP per Home Assistant OS.
Basato su `python:3.12-slim-bookworm`, identico all'originale `Dockerfile.full`.

## Struttura

```
easyproxy/
├── config.yaml     ← Metadati add-on (NO build.yaml, NO riga image:)
├── Dockerfile      ← FROM python:3.12-slim-bookworm, WARP installato ma off
├── run.sh          ← Avvio con jq (no bashio), ENABLE_WARP=false hardcoded
├── DOCS.md
└── CHANGELOG.md
```

## Installazione

1. Copia la cartella `easyproxy/` in `/addons/easyproxy/` su HAOS
2. Impostazioni → Add-on → Store → ⋮ → Controlla aggiornamenti
3. Installa "EasyProxy" dai Local add-on
4. Configura `api_password` nella scheda Configurazione
5. Avvia (prima build: ~10-15 min)

## Utilizzo

- **Proxy URL**: `http://<IP_HA>:7860`
- **Password**: quella impostata in `api_password`
