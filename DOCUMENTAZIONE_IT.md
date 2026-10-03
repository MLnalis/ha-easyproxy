# 📚 Documentazione

## Installazione

1. HA → Impostazioni → Componenti aggiuntivi
2. ⋮ → Repository → `https://github.com/MLnalis/ha-easyproxy`
3. Installa EasyProxy

## Configurazione

```yaml
port: 7860
api_password: "password"
enable_warp: false
```

## Utilizzo

- Dashboard: `http://[IP-HA]:7860`
- Admin: `http://[IP-HA]:7860/admin`
- API: `http://[IP-HA]:7860/docs`

### Proxy

```
http://[IP-HA]:7860/proxy/manifest.m3u8?url=<URL>
```

### DVR

```
http://[IP-HA]:7860/record?url=<URL>&name=<NOME>
```

## Supporto

- Issue: https://github.com/MLnalis/ha-easyproxy/issues
