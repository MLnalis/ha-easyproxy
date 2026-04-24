# EasyProxy (FULL, no WARP)

Proxy streaming per Stremio — versione FULL con FlareSolverr v3 e Byparr, senza WARP.
Basato sull'originale [Dockerfile.full](https://github.com/realbestia1/EasyProxy/blob/main/Dockerfile.full).

## Configurazione

| Opzione | Descrizione | Default |
|---|---|---|
| `api_password` | Password per proteggere il proxy | `cambia_questa_password` |
| `workers` | Worker Gunicorn | `1` |

## Porte interne

| Porta | Servizio |
|---|---|
| `7860` | EasyProxy (principale) |
| `8191` | FlareSolverr v3 |
| `8192` | Byparr |

## Utilizzo con Stremio

- **Proxy URL**: `http://<IP_HA>:7860`
- **Password**: valore di `api_password`

## Note

- WARP è installato nell'immagine ma **mai avviato** (ENV ENABLE_WARP=false)
- Prima build: 10-15 minuti (scarica Chromium, Playwright, dipendenze)
