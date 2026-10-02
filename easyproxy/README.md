# Home Assistant Add-on: EasyProxy

Universal HLS/M3U8/DASH (MPD) proxy, stream extractor and DVR, packaged as a Home Assistant add-on.

Based on the upstream project: https://github.com/realbestia1/EasyProxy (MIT License).

## Features

- Proxy for HLS, M3U8, MPD (DASH) and static video files
- ClearKey DRM support
- Specialized extractors (Vavoo, DaddyliveHD, Sportsonline, VixSrc, DoodStream, EmbedSports, ...)
- Integrated DVR and Playlist Builder
- Cloudflare WARP, NordVPN, custom WireGuard and Tor SOCKS5 routes (no privileged mode required)

## Installation

1. Copy this folder to `/addons/easyproxy/` (Samba or SSH add-on), or add it through a custom repository.
2. Go to **Settings -> Add-ons -> Add-on Store -> ⋮ -> Check for updates**.
3. Open **EasyProxy** under *Local add-ons*, then **Install**.
4. Set a strong `api_password`, then **Start**.
5. Open `http://<HA_IP>:7860/admin`.

## Supported architectures

- amd64
- aarch64

See `DOCS.md` for configuration and usage details.
