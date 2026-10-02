FROM ghcr.io/realbestia1/easyproxy:latest

COPY run.sh /run-ha.sh
RUN sed -i 's/
$//' /run-ha.sh && chmod +x /run-ha.sh

ENTRYPOINT []
CMD ["/bin/bash", "/run-ha.sh"]
