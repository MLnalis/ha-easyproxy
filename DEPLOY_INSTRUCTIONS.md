# 📤 Pubblicare su GitHub

## 1. Crea Repository

https://github.com/new → Name: `ha-easyproxy`

## 2. Push

```bash
cd ha-easyproxy
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/MLnalis/ha-easyproxy.git
git push -u origin main
```

## 3. Aggiungi a HA

Utenti aggiungono:
```
https://github.com/MLnalis/ha-easyproxy
```

**Nota:** Usa immagine `ghcr.io/realbestia1/easyproxy:latest`
