# EasyProxy (FULL, no WARP)

Proxy streaming per Stremio basato su [EasyProxy](https://github.com/realbestia1/EasyProxy)
(fork di MediaFlow Proxy), versione **FULL** ma **senza WARP**.

---

## Installazione

1. Vai su **Impostazioni → Add-on → Store → ⋮ → Repository**
2. Aggiungi il percorso locale `/addons/easyproxy`
3. Cerca **EasyProxy (FULL, no WARP)** e clicca **Installa**

---

## Configurazione

| Opzione | Descrizione | Default |
|---|---|---|
| `api_password` | Password per proteggere il proxy | `cambia_questa_password` |
| `workers` | Numero di worker Uvicorn | `1` |
| `worker_class` | Classe worker ASGI | `uvicorn.workers.UvicornWorker` |

---

## Utilizzo con Stremio

Una volta avviato l'add-on, accedi alla UI su:

```
http://<IP_HOME_ASSISTANT>:7860
```

Nella configurazione dell'add-on Stremio (es. Streamvix), imposta:

- **Proxy URL**: `http://<IP_HOME_ASSISTANT>:7860`
- **Password**: quella impostata in `api_password`

---

## Note

- WARP è **disabilitato** tramite variabili d'ambiente (`ENABLE_WARP=false`)
- L'add-on non richiede accesso a Internet tramite Cloudflare WARP
- Compatibile con HAOS su mini PC (amd64 / aarch64)
