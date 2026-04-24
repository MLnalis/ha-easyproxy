FROM python:3.12-slim-bookworm

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/easyproxy \
    FLARESOLVERR_URL=http://localhost:8191 \
    BYPARR_URL=http://localhost:8192 \
    BYPARR_PORT=8192 \
    ENABLE_WARP=false \
    WARP_ENABLED=false \
    USE_WARP=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git gnupg gpg jq \
    && curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg \
        | gpg --yes --dearmor \
        --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] \
        https://pkg.cloudflareclient.com/ bookworm main" \
        | tee /etc/apt/sources.list.d/cloudflare-client.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        cloudflare-warp \
        netcat-openbsd \
        ffmpeg \
        chromium \
        chromium-driver \
        libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
        libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
        libxfixes3 libxrandr2 libgbm1 libasound2 \
        libpango-1.0-0 libcairo2 libatspi2.0-0 libxshmfence1 \
        ca-certificates fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_EXE_PATH=/usr/bin/chromium \
    CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER_PATH=/usr/bin/chromedriver

RUN git clone https://github.com/FlareSolverr/FlareSolverr.git /app/flaresolverr \
    && pip install --no-cache-dir -r /app/flaresolverr/requirements.txt

COPY patch_flaresolverr.py /tmp/patch_flaresolverr.py
RUN python /tmp/patch_flaresolverr.py

RUN git clone https://github.com/ThePhaseless/Byparr.git /app/byparr_src \
    && cd /app/byparr_src \
    && sed -i 's/requires-python = .*/requires-python = ">=3.12"/' pyproject.toml \
    && pip install --no-cache-dir . \
    && python -m camoufox fetch

RUN git clone https://github.com/realbestia1/EasyProxy.git /app/easyproxy \
    && pip install --no-cache-dir -r /app/easyproxy/requirements.txt \
    && cd /app/easyproxy && python -m playwright install chromium --with-deps

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 7860 8191 8192
CMD ["/run.sh"]