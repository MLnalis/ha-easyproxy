# EasyProxy Full — Home Assistant Add-on

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Add--on-blue?logo=home-assistant)](https://www.home-assistant.io/)
[![GitHub](https://img.shields.io/badge/EasyProxy-Source-black?logo=github)](https://github.com/realbestia1/EasyProxy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Add-on **Full** di [EasyProxy](https://github.com/realbestia1/EasyProxy) per Home Assistant OS.
> Versione completa con **FlareSolverr v3**, **Byparr** e **Cloudflare WARP** integrati.

---

## ✨ Funzionalità (Full vs Light)

| Feature | Light | Full |
|---|:---:|:---:|
| Proxy HLS/M3U8/MPD | ✅ | ✅ |
| DVR integrato | ✅ | ✅ |
| FFmpeg transcoding | ✅ | ✅ |
| Extractor Vavoo/VixSrc | ✅ | ✅ |
| FlareSolverr v3 (Cloudflare bypass) | ❌ | ✅ |
| Byparr (DoodStream/IP-sticky) | ❌ | ✅ |
| Cloudflare WARP (IP residenziale) | ❌ | ✅ |

---

## 📋 Requisiti

- **Home Assistant OS** o **Home Assistant Supervised**
- Architettura: `amd64` o `aarch64`
- RAM consigliata: **2 GB** (FlareSolverr + Byparr + Chromium richiedono memoria)
- Il dispositivo `/dev/net/tun` deve essere disponibile per WARP

> ⚠️ Il primo build richiede **20–40 minuti** (download Playwright, Camoufox, Chromium).

---

## 🚀 Installazione

### 1 — Aggiungi il repository

[![Aggiungi Repository](https://img.shields.io/badge/Aggiungi%20a-Home%20Assistant-blue?logo=home-assistant)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FMLnalis%2Fha-easyproxy)

Oppure manualmente: **Impostazioni → Add-on → Store → ⋮ → Repository** → `https://github.com/MLnalis/ha-easyproxy`

### 2 — Installa, configura e avvia

Trova il tile **EasyProxy Full** → **INSTALLA** → configura le opzioni → **AVVIA**.

---

## ⚙️ Opzioni di configurazione

| Opzione | Default | Descrizione |
|---|---|---|
| `api_password` | `cambiami` | Password per le API |
| `port` | `7860` | Porta del server |
| `mpd_mode` | `legacy` | `ffmpeg` (migliore qualità) / `legacy` (leggero) / `none` |
| `log_level` | `WARNING` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `dvr_enabled` | `false` | Abilita registrazione stream |
| `global_proxy` | _(vuoto)_ | Proxy HTTP/SOCKS5 globale |
| `transport_routes` | _(vuoto)_ | Routing proxy per dominio |
| `enable_warp` | `false` | **[Full]** Abilita Cloudflare WARP |
| `warp_license_key` | _(vuoto)_ | **[Full]** Licenza WARP Team/Zero Trust |
| `warp_excluded_hosts` | _(vuoto)_ | **[Full]** Domini da escludere da WARP (CSV) |
| `solvers_force_warp_proxy` | `false` | **[Full]** Forza FlareSolverr/Byparr a usare WARP |
| `workers` | `0` | Numero worker Gunicorn (0 = auto, usa n. CPU) |

### Esempio configurazione con WARP

```yaml
api_password: "mypassword"
mpd_mode: "ffmpeg"
enable_warp: true
warp_license_key: "XXXX-XXXX-XXXX-XXXX"
warp_excluded_hosts: "real-debrid.com,*.real-debrid.com,dlhd.dad,*.dlhd.dad"
transport_routes: "{URL=vavoo.to, DISABLE_SSL=true}"
dvr_enabled: true
```

---

## 🔧 Note WARP

- Richiede `/dev/net/tun` (configurato automaticamente in `config.yaml`)
- Se il build o l'avvio fallisce per mancanza del dispositivo TUN, abilita il **Kernel module** `tun` nell'host
- Con `enable_warp: false` (default) il container funziona esattamente come la versione Light, senza overhead

---

## 📁 Struttura del repository

```
ha-easyproxy/
├── repository.json
└── easyproxy/
    ├── config.yaml     ← Manifesto add-on (opzioni, porte, ingress)
    ├── build.yaml      ← Immagine base per HA Supervisor
    ├── Dockerfile      ← Build Full: python:3.12 + FFmpeg + WARP + FlareSolverr + Byparr
    ├── start.py        ← Avvia WARP → FlareSolverr → Byparr → EasyProxy
    └── readme.md       ← Questo file
```

---

## 🔄 Aggiornamento

Incrementa `version` in `config.yaml` (es. `2.0.0` → `2.0.1`) → commit → push.  
In HA comparirà automaticamente il pulsante **AGGIORNA**.

---

## 🙏 Credits

- **EasyProxy** — [realbestia1](https://github.com/realbestia1/EasyProxy)
- **FlareSolverr** — [FlareSolverr/FlareSolverr](https://github.com/FlareSolverr/FlareSolverr)
- **Byparr** — [ThePhaseless/Byparr](https://github.com/ThePhaseless/Byparr)
- **Home Assistant** — [home-assistant.io](https://www.home-assistant.io/)
