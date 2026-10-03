FROM ghcr.io/realbestia1/easyproxy:latest

LABEL io.hass.version="1.0.0"
LABEL io.hass.type="addon"
LABEL maintainer="MLnalis"

WORKDIR /data
RUN mkdir -p /data/config /data/recordings /data/logs
EXPOSE 7860

COPY run.sh /run.sh
RUN chmod a+x /run.sh

ENTRYPOINT ["/run.sh"]
