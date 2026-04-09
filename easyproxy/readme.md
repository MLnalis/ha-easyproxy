# EasyProxy — Home Assistant Add-on

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?logo=home-assistant)](https://www.home-assistant.io/)
[![GitHub](https://img.shields.io/badge/EasyProxy-Source-black?logo=github)](https://github.com/realbestia1/EasyProxy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Add-on wrapper per installare [EasyProxy](https://github.com/realbestia1/EasyProxy) come add-on nativo su **Home Assistant OS**.

EasyProxy è un **proxy server universale per stream HLS, M3U8 e IPTV** con supporto nativo per Vavoo, DaddyliveHD, Sportsonline e VixSrc. Offre un'interfaccia web completa, DVR integrato, transcoding MPD→HLS via FFmpeg e compatibilità con Stremio come sostituto di MediaFlow Proxy.

---

## ✨ Funzionalità

- 🎬 **Proxy universale** — HLS, M3U8, MPD/DASH, VIXSRC
- 🔐 **Extractor specializzati** — Vavoo, DaddyliveHD, Sportsonline, VixSrc
- ⚡ **Async** — Connessioni asincrone con keep-alive (aiohttp)
- 🔓 **DRM Decryption** — ClearKey via FFmpeg transcoding
- 📼 **DVR integrato** — Registra mentre guardi, con auto-eliminazione
- 🛠️ **Builder M3U** — Combina e gestisci playlist
- 📱 **Web Interface** — Dashboard completa con Swagger UI
- 🔑 **Autenticazione API** — Protezione con password via header o query param
- 🔄 **Retry automatico** — Resilienza agli errori di rete
- 🌐 **Proxy SOCKS5/HTTP** — Routing per dominio con `TRANSPORT_ROUTES`

---

## 📋 Requisiti

- **Home Assistant OS** (HAOS) o **Home Assistant Supervised**
- Architettura: `amd64` o `aarch64`
- RAM consigliata: **1 GB** (Playwright/Chromium richiede memoria)
- CPU: qualsiasi (usa `mpd_mode: legacy` su hardware debole)

---

## 🚀 Installazione

### 1 — Aggiungi questo repository in Home Assistant

[![Aggiungi Repository](https://img.shields.io/badge/Aggiungi%20a-Home%20Assistant-blue?logo=home-assistant)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FMLnalis%2Fha-easyproxy)

Oppure manualmente:

1. Vai su **Impostazioni → Add-on → Store**
2. Clicca **⋮ → Repository**
3. Aggiungi l'URL:
   ```
   https://github.com/MLnalis/ha-easyproxy
   ```
4. Clicca **AGGIUNGI** → **CHIUDI**

### 2 — Installa l'add-on

1. Trova il tile **EasyProxy** nello Store
2. Clicca **INSTALLA**

> ⚠️ Il primo build richiede **10–20 minuti** per scaricare Playwright/Chromium.

### 3 — Configura

Nella scheda **Configurazione**:

| Opzione | Default | Descrizione |
|---|---|---|
| `api_password` | `cambiami` | Password per proteggere le API |
| `port` | `7860` | Porta del server |
| `mpd_mode` | `legacy` | `ffmpeg` (migliore) o `legacy` (leggero) |
| `log_level` | `WARNING` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `dvr_enabled` | `false` | Abilita registrazione stream |
| `global_proxy` | _(vuoto)_ | Proxy HTTP/SOCKS5 globale |
| `transport_routes` | _(vuoto)_ | Routing proxy per dominio |

### 4 — Avvia

1. Clicca **AVVIA**
2. Accedi tramite **APRI INTERFACCIA WEB** oppure `http://IP_HA:7860`

---

## ⚙️ Configurazione avanzata

### Proxy globale

```yaml
global_proxy: "http://utente:password@proxy.esempio.com:8080"
```

Formati supportati: `http://`, `https://`, `socks5://`, `socks4://`

### Routing per dominio (TRANSPORT_ROUTES)

Per usare proxy diversi in base al sito di destinazione:

```yaml
transport_routes: "{URL=vavoo.to, PROXY=socks5://proxy1:1080, DISABLE_SSL=true}, {URL=dlhd.dad, PROXY=http://proxy2:8080}"
```

### DVR / Registrazione

Con `dvr_enabled: true` i file vengono salvati in:
```
/share/easyproxy/recordings/
```
Accessibile tramite gli add-on **Samba** o **File Editor** di HA.

---

## 🧰 Utilizzo degli endpoint

### Proxy stream HLS / M3U8

```
GET http://IP:7860/proxy/manifest.m3u8?url=URL_ENCODED&api_password=PASSWORD
```

### Proxy stream MPD/DASH → HLS

```
GET http://IP:7860/proxy/mpd/manifest.m3u8?url=URL_ENCODED&api_password=PASSWORD
```

### Estrazione URL (Vavoo, DaddyliveHD, VixSrc...)

```
GET http://IP:7860/extractor?url=URL_ORIGINALE&api_password=PASSWORD
```

### Builder playlist M3U

```
GET http://IP:7860/builder
```

### Info server

```
GET http://IP:7860/api/info
```

### Documentazione API interattiva

```
GET http://IP:7860/docs
```

---

## 📺 Compatibilità Stremio / MediaFlow Proxy

EasyProxy è compatibile come sostituto drop-in di MediaFlow Proxy per gli addon Stremio:

- **Proxy URL**: `http://IP_HA:7860`
- **API Password**: quella impostata nella configurazione

---

## 🔧 Risoluzione problemi

| Problema | Causa | Soluzione |
|---|---|---|
| Build fallisce (`apt-get: not found`) | Immagine base Alpine | Verifica che `build.yaml` sia presente |
| Build lento (20+ min) | Download Playwright/Chromium | Normale al primo avvio, attendi |
| Tile non appare nello Store | Errore in `config.yaml` | Controlla log Supervisor |
| Extractor non funziona | Chromium crash | Controlla log add-on per errori Playwright |
| DVR non salva file | Permessi `/share` | Verifica `map: share:rw` in config.yaml |
| Stream MPD lento | CPU bassa con FFmpeg | Passa a `mpd_mode: legacy` |

### Leggere i log

```
HA → Impostazioni → Add-on → EasyProxy → Log
```

```
HA → Impostazioni → Sistema → Log → Supervisor
```

---

## 📁 Struttura del repository

```
ha-easyproxy/
├── repository.json        ← Metadati repository per HA
└── easyproxy/
    ├── config.yaml        ← Manifesto add-on (opzioni, porte, ingress)
    ├── build.yaml         ← Specifica immagine base Docker
    ├── Dockerfile         ← Build: python:3.11-bookworm + FFmpeg + Playwright
    └── run.sh             ← Legge options.json di HA e avvia gunicorn
```

---

## 🔄 Aggiornamento

Per aggiornare all'ultima versione di EasyProxy:

1. Incrementa `version` in `easyproxy/config.yaml` (es. `1.0.0` → `1.0.1`)
2. Fai commit e push su GitHub
3. In HA comparirà il pulsante **AGGIORNA**

---

## 📄 Licenza

Questo wrapper è distribuito sotto licenza MIT.  
EasyProxy (progetto originale) è di [realbestia1](https://github.com/realbestia1/EasyProxy).

---

## 🙏 Credits

- **EasyProxy** — [realbestia1](https://github.com/realbestia1/EasyProxy)
- **Home Assistant** — [home-assistant.io](https://www.home-assistant.io/)
