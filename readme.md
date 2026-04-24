# EasyProxy HAOS Add-on — Guida Completa

> **EasyProxy (FULL, senza WARP) per Home Assistant OS**
> Compatibile con: amd64, aarch64, armv7

---

## Perché add-on locale e non Portainer?

Su **Home Assistant OS** (HAOS), Portainer è **sconsigliato e non supportato ufficialmente**:

- L'add-on Portainer ufficiale è stato **rimosso** dal repository Community Add-ons
  per problemi di stabilità e supporto.
- Qualsiasi container Docker non-nativo installato tramite Portainer
  **contrassegna il sistema come "unsupported"**, impedendo aggiornamenti.
- L'unica via **supportata e stabile** su HAOS è creare un **add-on locale**.

➡ **Conclusione**: usa il metodo add-on locale descritto di seguito.

---

## Prerequisiti

- Home Assistant OS attivo sul mini PC
- Accesso ai file di HA tramite uno di questi add-on:
  - **SSH & Web Terminal** (Settings → Add-ons → Store)
  - **Studio Code Server** (VS Code nel browser)

---

## Installazione step-by-step

### 1. Copia i file sul mini PC

Tramite SSH o Studio Code Server, crea la cartella:

```bash
mkdir -p /addons/easyproxy
```

Poi copia i file da questa cartella (`easyproxy/`) in `/addons/easyproxy/`:

```
/addons/
  easyproxy/
    config.yaml
    Dockerfile
    run.sh
    build.yaml
    DOCS.md
    CHANGELOG.md
```

Con SSH puoi usare `scp` dal tuo computer:

```bash
scp -r ./easyproxy/* root@<IP_HA>:/addons/easyproxy/
```

Oppure crea/incolla i file uno per uno con Studio Code Server.

---

### 2. Abilita add-on locali in HAOS

1. Vai su **Impostazioni → Add-on**
2. In basso a destra clicca **Store (⋮) → Controlla aggiornamenti**
3. Gli add-on in `/addons/` vengono rilevati automaticamente come **"Local add-ons"**

---

### 3. Installa l'add-on

1. Cerca **EasyProxy** nella sezione **Local add-ons** dello store
2. Clicca **Installa** (la prima build richiede 2-5 minuti)
3. Vai nella scheda **Configurazione** e imposta la tua `api_password`

---

### 4. Avvia e verifica

1. Clicca **Avvia**
2. Controlla i log: dovresti vedere `Avvio EasyProxy (FULL, senza WARP)...`
3. Accedi a `http://<IP_HA>:7860` dal browser

---

## Configurazione Stremio

Nell'add-on Stremio (es. Streamvix):

| Campo | Valore |
|---|---|
| Proxy URL | `http://<IP_HA>:7860` |
| Password | quella impostata in `api_password` |

---

## Struttura file

```
easyproxy/
├── config.yaml     ← Metadati add-on (nome, porte, opzioni)
├── Dockerfile      ← Build del container (scarica EasyProxy da GitHub, rimuove WARP)
├── run.sh          ← Script di avvio (imposta env vars, lancia uvicorn/gunicorn)
├── build.yaml      ← Immagini base per ogni architettura
├── DOCS.md         ← Documentazione utente
└── CHANGELOG.md    ← Storico versioni
```

---

## Variabili d'ambiente WARP disabilitate

Il `run.sh` imposta automaticamente:

```bash
ENABLE_WARP=false
WARP_ENABLED=false
USE_WARP=false
DISABLE_WARP=true
```

Queste variabili coprono tutti i possibili nomi usati da MediaFlow Proxy / EasyProxy
per attivare/disattivare WARP.

---

## Risoluzione problemi

| Problema | Soluzione |
|---|---|
| Add-on non compare nello store | Riavvia HA o clicca "Controlla aggiornamenti" |
| Build fallisce | Controlla i log: potrebbe mancare una dipendenza in `requirements.txt` |
| Porta 7860 non raggiungibile | Verifica che la porta sia aperta nel firewall del mini PC |
| Errore "api_password" | Imposta la password nella scheda Configurazione dell'add-on |
