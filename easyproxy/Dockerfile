ARG BUILD_FROM
FROM ghcr.io/realbestia1/easyproxy:latest

LABEL \
    io.hass.version="1.0.0" \
    io.hass.type="addon" \
    io.hass.arch="aarch64|amd64|armv7"

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
