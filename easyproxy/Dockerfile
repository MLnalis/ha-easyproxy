# EasyProxy Full — Home Assistant Add-on
# Include: FlareSolverr v3, Byparr, Cloudflare WARP, Chromium, FFmpeg

FROM python:3.12-slim-bookworm

# ---------- Environment ----------
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0
ENV PYTHONPATH=/app
ENV CHROME_EXE_PATH=/usr/bin/chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver
ENV FLARESOLVERR_URL=http://localhost:8191
ENV BYPARR_URL=http://localhost:8192
ENV BYPARR_PORT=8192

# ---------- System deps + Cloudflare WARP repo ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    gnupg \
    gpg \
    netcat-openbsd \
    xvfb \
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
    libglu1-mesa \
    ca-certificates \
    fonts-liberation \
 && curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg \
      | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg \
 && echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ bookworm main" \
      | tee /etc/apt/sources.list.d/cloudflare-client.list \
 && apt-get update && apt-get install -y --no-install-recommends cloudflare-warp \
 && rm -rf /var/lib/apt/lists/*

# ---------- FlareSolverr v3 (Python) ----------
RUN git clone https://github.com/FlareSolverr/FlareSolverr.git /app/flaresolverr \
 && cd /app/flaresolverr \
 && sed -i 's/driver_executable_path=driver_exe_path/driver_executable_path="\/usr\/bin\/chromedriver"/' src/utils.py \
 && sed -i "s|options.add_argument('--no-sandbox')|options.add_argument('--no-sandbox'); options.add_argument('--disable-dev-shm-usage'); options.add_argument('--disable-gpu'); options.add_argument('--headless=new')|" src/utils.py \
 && sed -i "s|^\([[:space:]]*\)start_xvfb_display()|\1pass|g" src/utils.py \
 && pip install --no-cache-dir -r requirements.txt

# ---------- Byparr (patch: rimuove vincolo Python >=3.14) ----------
RUN git clone https://github.com/ThePhaseless/Byparr.git /app/byparr_src \
 && cd /app/byparr_src \
 && sed -i 's/requires-python = .*/requires-python = ">=3.11"/' pyproject.toml \
 && pip install --no-cache-dir . \
 && python -m camoufox fetch

# ---------- EasyProxy ----------
RUN git clone https://github.com/realbestia1/EasyProxy.git /app/easyproxy

WORKDIR /app/easyproxy

RUN pip install --no-cache-dir -r requirements.txt \
 && python -m playwright install chromium

# ---------- HA start script ----------
COPY start.py /start.py

EXPOSE 7860

CMD ["python3", "/start.py"]
