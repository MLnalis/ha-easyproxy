# EasyProxy Full — Home Assistant Add-on

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?logo=home-assistant)](https://www.home-assistant.io/)
[![GitHub](https://img.shields.io/badge/EasyProxy-Source-black?logo=github)](https://github.com/realbestia1/EasyProxy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Add-on **Full** di [EasyProxy](https://github.com/realbestia1/EasyProxy) per Home Assistant OS.
> Versione completa con **FlareSolverr v3** e **Byparr** integrati.

Equivalente di:
```bash
docker run -d -p 7860:7860 --name EasyProxy ghcr.io/realbestia1/easyproxy:full
```

---

## ✨ Funzionalità

| Feature | Light | Full |
|---|:---:|:---:|
| Proxy HLS / M3U8 / MPD | ✅ | ✅ |
| DVR integrato | ✅ | ✅ |
| FFmpeg transcoding | ✅ | ✅ |
| Extractor Vavoo / VixSrc / DaddyliveHD | ✅ | ✅ |
| FlareSolverr v3 (bypass Cloudflare) | ❌ | ✅ |
| Byparr (DoodStream / IP-sticky) | ❌ | ✅ |
| Compatibilità Stremio / MediaFlow Proxy | ✅ | ✅ |

---

## 📋 Requisiti

- **Home Assistant OS** o **Home Assistant Supervised**
- Architettura: `amd64` o `aarch64`
- RAM consigliata: **2 GB**
- Spazio disco: **~3 GB** (immagine Docker + Playwright + Camoufox)

> ⚠️ Il primo build richiede **20–40 minuti**.

---

## 🚀 Installazione

### 1 — Aggiungi il repository

[![Aggiungi a Home Assistant](https://img.shields.io/badge/Aggiungi%20a-Home%20Assistant-blue?logo=home-assistant)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FMLnalis%2Fha-easyproxy)

Oppure manualmente:
1. **Impostazioni → Add-on → Store → ⋮ → Repository**
2. Aggiungi `https://github.com/MLnalis/ha-easyproxy` → **AGGIUNGI**

### 2 — Installa, configura e avvia

Trova **EasyProxy Full** nello Store → **INSTALLA** → configura → **AVVIA**.

---

## ⚙️ Opzioni

| Opzione | Default | Descrizione |
|---|---|---|
| `api_password` | `cambiami` | Password per proteggere le API |
| `port` | `7860` | Porta del server |
| `mpd_mode` | `legacy` | `ffmpeg` / `legacy` / `none` |
| `log_level` | `WARNING` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `dvr_enabled` | `false` | Abilita registrazione stream |
| `global_proxy` | _(vuoto)_ | Proxy HTTP/SOCKS5 globale |
| `transport_routes` | _(vuoto)_ | Routing proxy per dominio |
| `workers` | `0` | Worker Gunicorn (0 = auto) |

---

## 📁 Struttura repository

```
ha-easyproxy/
├── repository.json
└── easyproxy/
    ├── config.yaml
    ├── build.yaml
    ├── Dockerfile
    ├── start.py
    └── readme.md
```

---

## 🙏 Credits

- **EasyProxy** — [realbestia1](https://github.com/realbestia1/EasyProxy)
- **FlareSolverr** — [FlareSolverr/FlareSolverr](https://github.com/FlareSolverr/FlareSolverr)
- **Byparr** — [ThePhaseless/Byparr](https://github.com/ThePhaseless/Byparr)
