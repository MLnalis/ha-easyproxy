# EasyProxy (FULL, no WARP) — Documentazione

Proxy streaming per Stremio basato su [EasyProxy](https://github.com/realbestia1/EasyProxy),
versione **FULL** con FlareSolverr v3 e Byparr integrati, **senza WARP**.

## Opzioni di configurazione

| Opzione | Descrizione | Default |
|---|---|---|
| `api_password` | Password API per proteggere il proxy | `cambia_questa_password` |
| `workers` | Numero di worker Gunicorn | `1` |

## Porte

| Porta | Servizio |
|---|---|
| `7860` | EasyProxy (principale) |
| `8191` | FlareSolverr v3 |
| `8192` | Byparr |

## Utilizzo con Stremio

Configura l'addon Stremio (es. Streamvix) con:
- **Proxy URL**: `http://<IP_HOME_ASSISTANT>:7860`
- **Password**: il valore di `api_password`
