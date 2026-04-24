ARG BUILD_FROM
FROM ${BUILD_FROM}

# Installa dipendenze di sistema
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-virtualenv \
    git \
    curl \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev

# Clona EasyProxy
WORKDIR /app
RUN git clone https://github.com/realbestia1/EasyProxy.git .

# Installa dipendenze Python (NO warp, NO cloudflared)
# Rimuove eventuali pacchetti warp dai requirements
RUN if [ -f requirements.txt ]; then \
      sed -i '/warp/Id' requirements.txt && \
      sed -i '/cloudflare/Id' requirements.txt; \
    fi

RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copia script di avvio
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 7860

CMD ["/run.sh"]
