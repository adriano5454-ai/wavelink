# Candidate Linux container for a FICTIONAL, private client demonstration.
# Image build and actual Render TLS/disk behaviour require platform acceptance.
FROM python:3.13-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends nginx ca-certificates libjpeg62-turbo zlib1g \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 wavelink \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin wavelink
WORKDIR /opt/wavelink
COPY requirements.lock ./requirements.lock
RUN python -m pip install --no-cache-dir -r requirements.lock
COPY vendor/source.part* vendor/source_parts.json ./vendor/
COPY deploy/extract_source.py ./extract_source.py
RUN python extract_source.py vendor/source_parts.json /opt/wavelink/app \
    && rm vendor/source.part* vendor/source_parts.json extract_source.py
COPY vendor/FICTIONAL_DEMO.ajproject ./vendor/FICTIONAL_DEMO.ajproject
COPY deploy ./deploy
COPY ops ./ops
# Runtime starts with mount ownership setup and immediately drops to UID 10001.
# Never install/open the Windows Admin or run its launcher in the container.
EXPOSE 10000
CMD ["python", "-m", "deploy.entrypoint"]
