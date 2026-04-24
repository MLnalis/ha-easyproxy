EasyProxy Full è un proxy server asincrono per stream HLS, M3U8, MPD/DASH e IPTV.
Include nativamente **FlareSolverr v3** (bypass Cloudflare) e **Byparr** (sessioni IP-sticky),
ed è compatibile come sostituto drop-in di **MediaFlow Proxy** per gli add-on Stremio.

## Installazione

1. Vai su **Impostazioni → Add-on → Store → ⋮ → Repository**
2. Aggiungi: `https://github.com/MLnalis/ha-easyproxy`
3. Trova **EasyProxy Full** nello Store e clicca **INSTALLA**

> ⚠️ Il primo build richiede **20–40 minuti** (download Chrome, Playwright, Camoufox).

## Configurazione

| Opzione | Default | Descrizione |
|---|---|---|
| `api_password` | `cambiami` | Password per proteggere le API |
| `port` | `7860` | Porta del server |
| `mpd_mode` | `legacy` | `ffmpeg` (qualità migliore) / `legacy` (leggero) / `none` |
| `log_level` | `WARNING` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `dvr_enabled` | `false` | Abilita registrazione stream |
| `global_proxy` | _(vuoto)_ | Proxy HTTP/SOCKS5 globale (es. `socks5://host:1080`) |
| `transport_routes` | _(vuoto)_ | Routing proxy per dominio (vedi sotto) |
| `workers` | `0` | Worker Gunicorn — `0` = auto (n. CPU) |

### Transport Routes

Routing proxy differenziato per dominio:

```yaml
transport_routes: "{URL=vavoo.to, PROXY=socks5://proxy1:1080, DISABLE_SSL=true}, {URL=dlhd.dad, PROXY=http://proxy2:8080}"
```

## Utilizzo

Accedi tramite **APRI INTERFACCIA WEB** o direttamente a `http://<IP_HA>:7860`.

### Stremio / MediaFlow Proxy

- **Proxy URL**: `http://<IP_HA>:7860`
- **API Password**: quella impostata in configurazione

### Endpoint principali

| Endpoint | Descrizione |
|---|---|
| `/proxy/manifest.m3u8?url=URL&api_password=PWD` | Proxy HLS / M3U8 |
| `/proxy/mpd/manifest.m3u8?url=URL&api_password=PWD` | MPD/DASH → HLS |
| `/extractor?url=URL&api_password=PWD` | Estrazione URL da provider |
| `/builder` | Builder playlist M3U |
| `/api/info` | Info server JSON |
| `/docs` | Swagger UI |

### DVR / Registrazioni

Con `dvr_enabled: true` i file vengono salvati in:

```
/share/easyproxy/recordings/
```

Accessibile tramite gli add-on **Samba** o **File Editor** di Home Assistant.

## Supporto

- [EasyProxy su GitHub](https://github.com/realbestia1/EasyProxy)
- [Repository add-on](https://github.com/MLnalis/ha-easyproxy)
