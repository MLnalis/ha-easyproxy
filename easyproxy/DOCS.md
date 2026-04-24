# EasyProxy (FULL, no WARP)

Proxy streaming per Stremio — versione FULL con FlareSolverr v3 e Byparr, senza WARP.

## Configurazione

| Opzione | Descrizione | Default |
|---|---|---|
| `api_password` | Password API | `cambia_questa_password` |
| `workers` | Worker Gunicorn | `1` |

## Porte

| Porta | Servizio |
|---|---|
| `7860` | EasyProxy (principale) |
| `8191` | FlareSolverr v3 |
| `8192` | Byparr |

## Utilizzo con Stremio

- **Proxy URL**: `http://<IP_HA>:7860`
- **Password**: valore di `api_password`

## Note tecniche

- WARP è installato ma **mai avviato** (ENV ENABLE_WARP=false)
- FlareSolverr usa Chromium in modalità `--single-process --no-zygote` per compatibilità con i container HAOS
- Prima build: ~10-15 minuti