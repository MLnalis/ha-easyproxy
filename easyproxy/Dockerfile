# ─────────────────────────────────────────────────────────────────────────────
# EasyProxy Full — Home Assistant OS Add-on  v2.1.3
#
# Porte interne:
#   8191  FlareSolverr v3  (bypass Cloudflare — Chrome + Xvfb)
#   8192  Byparr           (DoodStream IP-sticky — Camoufox)
#   7860  EasyProxy        (proxy HLS/M3U8/IPTV — Gunicorn + aiohttp)
# ─────────────────────────────────────────────────────────────────────────────

ARG BUILD_FROM="python:3.12-slim-bookworm"
FROM ${BUILD_FROM}

ARG BUILD_VERSION
ARG BUILD_ARCH

LABEL io.hass.version="${BUILD_VERSION}" \
      io.hass.type="addon" \
      io.hass.arch="amd64"

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0 \
    PYTHONPATH=/app \
    FLARESOLVERR_URL=http://localhost:8191 \
    BYPARR_URL=http://localhost:8192 \
    BYPARR_PORT=8192 \
    HEADLESS=false \
    DISPLAY=:99 \
    # Chrome flags sicuri in container (equivalente a shm_size: 1gb del docker-compose originale)
    CHROME_FLAGS="--no-sandbox --disable-dev-shm-usage --disable-gpu --window-size=1280,720"

# ── 1. Pacchetti di sistema ───────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    ffmpeg \
    curl \
    wget \
    unzip \
    xvfb \
    # Dipendenze runtime Chrome
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libxshmfence1 \
    libglu1-mesa \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxext6 \
    libglib2.0-0 \
    libgtk-3-0 \
    libdbus-1-3 \
    fonts-liberation \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# ── 2. Google Chrome Stable da .deb ufficiale Google ─────────────────────────
# MOTIVO: undetected_chromedriver (usato da FlareSolverr) cerca "google-chrome"
# nel PATH. Chromium da apt NON è compatibile con undetected_chromedriver.
# Il docker-compose originale usa shm_size: 1gb — noi usiamo --disable-dev-shm-usage.
RUN wget -q -O /tmp/google-chrome.deb \
      "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
 && apt-get update \
 && apt-get install -y --no-install-recommends /tmp/google-chrome.deb \
 && rm /tmp/google-chrome.deb \
 && rm -rf /var/lib/apt/lists/* \
 # Esporta il path esatto per undetected_chromedriver
 && ln -sf /usr/bin/google-chrome /usr/local/bin/chrome \
 && google-chrome --version

ENV CHROME_PATH=/usr/bin/google-chrome

# ── 3. pip upgrade ────────────────────────────────────────────────────────────
RUN python3 -m pip install --no-cache-dir --upgrade pip

# ── 4. FlareSolverr v3 ────────────────────────────────────────────────────────
# FlareSolverr cerca Chrome in PATH e tramite undetected_chromedriver.
# xvfbwrapper è una lib Python — NON esiste come pacchetto apt.
RUN git clone https://github.com/FlareSolverr/FlareSolverr.git /app/flaresolverr \
 && cd /app/flaresolverr \
 && python3 -m pip install --no-cache-dir -r requirements.txt \
 && python3 -m pip install --no-cache-dir xvfbwrapper

# ── 5. Byparr ─────────────────────────────────────────────────────────────────
# Byparr usa Camoufox (fork Firefox stealth), indipendente da Chrome.
# pyproject.toml patchato: requires-python >=3.11 (era >=3.12 ma funziona su 3.11+)
RUN git clone https://github.com/ThePhaseless/Byparr.git /app/byparr_src \
 && cd /app/byparr_src \
 && sed -i 's/requires-python = .*/requires-python = ">=3.11"/' pyproject.toml \
 && python3 -m pip install --no-cache-dir . \
 && python3 -m camoufox fetch

# ── 6. EasyProxy (originale realbestia1/EasyProxy) ────────────────────────────
# L'originale viene avviato con:
#   gunicorn --bind 0.0.0.0:$PORT --workers N --worker-class aiohttp.worker.GunicornWebWorker app:app
# Le variabili d'ambiente sono le stesse del docker-compose originale:
#   API_PASSWORD, PORT, MPD_MODE, GLOBAL_PROXY, TRANSPORT_ROUTES
RUN git clone https://github.com/realbestia1/EasyProxy.git /app/easyproxy \
 && cd /app/easyproxy \
 && python3 -m pip install --no-cache-dir -r requirements.txt \
 && python3 -m playwright install chromium \
 && python3 -m playwright install-deps chromium

COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 7860

CMD ["/run.sh"]