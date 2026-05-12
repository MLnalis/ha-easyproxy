# EasyProxy - Documentazione

EasyProxy è un proxy HTTP/HTTPS avanzato con supporto per stream MPD/DASH, routing per URL pattern e interfaccia web integrata.

## Configurazione

### Opzioni principali

| Opzione         | Tipo   | Default | Descrizione                                        |
|----------------|--------|---------|----------------------------------------------------|
| `api_password`  | string | `ep`    | Password per l'accesso all'API e all'interfaccia web |
| `port`          | int    | `7860`  | Porta su cui EasyProxy è in ascolto                |

### Opzioni avanzate (opzionali)

| Opzione             | Tipo   | Descrizione                                                     |
|--------------------|--------|-----------------------------------------------------------------|
| `global_proxy`      | string | Proxy globale per tutte le richieste. Es: `http://myproxy.com:8080` |
| `transport_routes`  | string | Regole routing avanzato per URL pattern (vedi sotto)           |
| `mpd_mode`          | string | Modalità gestione stream MPD/DASH: `ffmpeg` o `legacy`         |

### Formato TRANSPORT_ROUTES

Formato: `{URL=pattern, PROXY=proxy_url, DISABLE_SSL=true}, {URL=pattern2, ...}`

Esempio:
```
{URL=vavoo.to, PROXY=socks5://proxy1:1080, DISABLE_SSL=true}, {URL=dlhd.dad, PROXY=http://proxy2:8080}
```

## Interfaccia Web

Dopo l'avvio, l'interfaccia web è accessibile tramite il pulsante "APRI WEB UI" nel pannello Add-on, oppure navigando a `http://<ip-homeassistant>:7860`.

## Note

- La porta `7860` deve essere libera sul tuo sistema.
- Se cambi la porta nel config, aggiorna anche il mapping nella sezione "Network" dell'add-on.
