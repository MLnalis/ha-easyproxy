FROM python:3.12-slim-bookworm

# ── Impostazioni base ────────────────────────────────────────────────────────
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    FLARESOLVERR_URL=http://localhost:8191 \
    BYPARR_URL=http://localhost:8192 \
    BYPARR_PORT=8192 \
    CHROME_EXE_PATH=/usr/bin/chromium \
    CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER_PATH=/usr/bin/chromedriver \
    ENABLE_WARP=false \
    WARP_ENABLED=false \
    USE_WARP=false

# ── Dipendenze sistema + WARP (installato ma mai avviato) ────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    gnupg \
    gpg \
    jq \
    && curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --yes --dearmor \
        --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] \
        https://pkg.cloudflareclient.com/ bookworm main" \
        | tee /etc/apt/sources.list.d/cloudflare-client.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        cloudflare-warp \
        netcat-openbsd \
        ffmpeg \
        chromium \
        libnss3 \
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
        ca-certificates \
        fonts-liberation \
        chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# ── Variabili Chromium ───────────────────────────────────────────────────────
ENV CHROME_EXE_PATH=/usr/bin/chromium \
    CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER_PATH=/usr/bin/chromedriver

# ── FlareSolverr v3 (Python) ─────────────────────────────────────────────────
RUN git clone https://github.com/FlareSolverr/FlareSolverr.git /app/flaresolverr \
    && cd /app/flaresolverr \
    && sed -i 's/driver_executable_path=driver_exe_path/driver_executable_path="\/usr\/bin\/chromedriver"/' src/utils.py \
    && sed -i "s|options.add_argument('--no-sandbox')|options.add_argument('--no-sandbox'); options.add_argument('--disable-dev-shm-usage'); options.add_argument('--disable-gpu'); options.add_argument('--headless=new')|" src/utils.py \
    && sed -i "s|^\([[:space:]]*\)start_xvfb_display()|\1pass|g" src/utils.py \
    && pip install --no-cache-dir -r requirements.txt

# ── Byparr (patch Python >= 3.14 → >= 3.12) ──────────────────────────────────
RUN git clone https://github.com/ThePhaseless/Byparr.git /app/byparr_src \
    && cd /app/byparr_src \
    && sed -i 's/requires-python = .*/requires-python = ">=3.12"/' pyproject.toml \
    && pip install --no-cache-dir . \
    && python -m camoufox fetch

# ── EasyProxy ────────────────────────────────────────────────────────────────
RUN git clone https://github.com/realbestia1/EasyProxy.git /app/easyproxy \
    && pip install --no-cache-dir -r /app/easyproxy/requirements.txt \
    && cd /app/easyproxy && python -m playwright install chromium \
    && chmod +x /app/easyproxy/entrypoint.sh

# ── Script di avvio per HAOS ─────────────────────────────────────────────────
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 7860 8191 8192

CMD ["/run.sh"]
