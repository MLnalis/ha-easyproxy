ARG BUILD_FROM
FROM ${BUILD_FROM}

# ── Variabili d'ambiente ─────────────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    ENABLE_WARP=false \
    WARP_ENABLED=false \
    USE_WARP=false \
    CHROME_EXE_PATH=/usr/bin/chromium \
    CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER_PATH=/usr/bin/chromedriver \
    FLARESOLVERR_URL=http://localhost:8191 \
    BYPARR_URL=http://localhost:8192 \
    BYPARR_PORT=8192

# ── Dipendenze di sistema (Debian — immagine base HAOS python:3.12) ──────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ffmpeg \
    chromium \
    chromium-driver \
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
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── EasyProxy ────────────────────────────────────────────────────────────────
RUN git clone https://github.com/realbestia1/EasyProxy.git . \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install chromium --with-deps

# ── FlareSolverr v3 (Python) ─────────────────────────────────────────────────
RUN git clone https://github.com/FlareSolverr/FlareSolverr.git /app/flaresolverr \
    && cd /app/flaresolverr \
    && sed -i 's/driver_executable_path=driver_exe_path/driver_executable_path="\/usr\/bin\/chromedriver"/' src/utils.py \
    && sed -i "s|options.add_argument('--no-sandbox')|options.add_argument('--no-sandbox'); options.add_argument('--disable-dev-shm-usage'); options.add_argument('--disable-gpu'); options.add_argument('--headless=new')|" src/utils.py \
    && sed -i "s|^\([[:space:]]*\)start_xvfb_display()|\1pass|g" src/utils.py \
    && pip install --no-cache-dir -r requirements.txt

# ── Byparr (bypass Python 3.14 requirement) ───────────────────────────────────
RUN git clone https://github.com/ThePhaseless/Byparr.git /app/byparr_src \
    && cd /app/byparr_src \
    && sed -i 's/requires-python = .*/requires-python = ">=3.11"/' pyproject.toml \
    && pip install --no-cache-dir . \
    && python -m camoufox fetch

# ── Script di avvio ──────────────────────────────────────────────────────────
COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 7860 8191 8192

CMD ["/run.sh"]
