# EasyProxy - Documentation

## Configuration

| Option | Description | Default |
| :--- | :--- | :--- |
| `api_password` | Password protecting the proxy API and the admin panel. **Change it.** | `cambiami` |
| `warp_license_key` | Optional Cloudflare WARP+ license key, used when the WARP profile is first registered. | empty |

The server port is fixed at `7860` inside the container. To change the external port, edit it in the add-on **Network** tab.

All other settings (WARP routing, DVR, proxies, NordVPN, WireGuard, Tor) are managed from the admin panel:
`http://<HA_IP>:7860/admin`.

## Persistent data

The add-on `/data` directory holds EasyProxy configuration and the WARP profile (`/data/warp.conf`). It survives restarts and updates. It is included in Home Assistant backups.

To store DVR recordings on shared storage, the add-on maps `/media` and `/share` read/write. Select one of these paths in the admin panel DVR settings.

## Usage

- Dashboard / admin: `http://<HA_IP>:7860/admin`
- API docs: `http://<HA_IP>:7860/docs`
- Playlist builder: `http://<HA_IP>:7860/builder`
- Server info: `http://<HA_IP>:7860/info`

Proxy a stream:

```
http://<HA_IP>:7860/proxy/manifest.m3u8?url=<URL>
```

Extract a stream:

```
http://<HA_IP>:7860/extractor/video?d=<URL>&redirect_stream=true
```

If the API password is enabled, add it as required by the upstream API (see `/docs`).

## Internal SOCKS5 endpoints

These listen on the add-on's loopback and are meant to be referenced from the admin panel:

| Service | Endpoint |
| :--- | :--- |
| WARP | `socks5h://127.0.0.1:1080` |
| NordVPN | `socks5h://127.0.0.1:1081` |
| Custom WireGuard | `socks5h://127.0.0.1:1082` |
| Tor | `socks5h://127.0.0.1:9050` |

## Notes

- The first start registers a WARP profile. If it fails, EasyProxy keeps running without WARP.
- The image includes Chromium, Tor and ffmpeg: allow at least 1 GB of free RAM.
- Port 7860 is exposed on your LAN. Do not forward it to the internet without protection.
- Use this software only with content you are legally entitled to access.

## Support

Upstream issues: https://github.com/realbestia1/EasyProxy/issues
