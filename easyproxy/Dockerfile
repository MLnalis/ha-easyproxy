# EasyProxy Full — Home Assistant OS Add-on
# Versione ottimizzata per Home Assistant OS / Supervised
#
# Stack avviato all'interno del container:
#   :8191  FlareSolverr v3  (bypass Cloudflare, usa Chrome + Xvfb)
#   :8192  Byparr           (DoodStream / token IP-sticky, usa Camoufox)
#   :7860  EasyProxy        (proxy HLS/M3U8/IPTV, Gunicorn + aiohttp)

ARG BUILD_FROM="python:3.12-slim-bookworm"
FROM ${BUILD_FROM}

ARG BUILD_VERSION
ARG BUILD_ARCH

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0
ENV PYTHONPATH=/app
ENV FLARESOLVERR_URL=http://localhost:8191
ENV BYPARR_URL=http://localhost:8192
ENV BYPARR_PORT=8192
ENV HEADLESS=false
ENV DISPLAY=:99

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
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxext6 \
    fonts-liberation \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --break-system-packages --upgrade pip

RUN git clone https://github.com/FlareSolverr/FlareSolverr.git /app/flaresolverr \
 && cd /app/flaresolverr \
 && python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt \
 && python3 -m pip install --no-cache-dir --break-system-packages xvfbwrapper

RUN git clone https://github.com/ThePhaseless/Byparr.git /app/byparr_src \
 && cd /app/byparr_src \
 && sed -i 's/requires-python = .*/requires-python = ">=3.11"/' pyproject.toml \
 && python3 -m pip install --no-cache-dir --break-system-packages . \
 && python3 -m camoufox fetch

RUN git clone https://github.com/realbestia1/EasyProxy.git /app/easyproxy \
 && cd /app/easyproxy \
 && python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt \
 && python3 -m playwright install chromium \
 && python3 -m playwright install-deps chromium

COPY start.py /start.py

EXPOSE 7860

CMD ["python3", "/start.py"]