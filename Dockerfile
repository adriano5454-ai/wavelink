# Candidate Linux container for a FICTIONAL, private client demonstration.
# Image build and actual Render TLS/disk behaviour require platform acceptance.
FROM python:3.13-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends nginx ca-certificates libjpeg62-turbo zlib1g tk8.6 poppler-utils tesseract-ocr tesseract-ocr-por \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 wavelink \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin wavelink
WORKDIR /opt/wavelink
COPY requirements.lock ./requirements.lock
RUN python -m pip install --no-cache-dir -r requirements.lock
COPY vendor/source.part* vendor/source_parts.json ./vendor/
COPY deploy/extract_source.py deploy/apply_ui93.py deploy/apply_ui94.py deploy/apply_ui95.py deploy/apply_ui96.py deploy/apply_ui97.py deploy/apply_ui99.py deploy/apply_ui100.py deploy/apply_ui101.py deploy/apply_ui102.py deploy/apply_ui103.py deploy/apply_ui104.py deploy/apply_ui105.py deploy/apply_ui106.py ./
RUN python extract_source.py vendor/source_parts.json /opt/wavelink/app \
    && python apply_ui93.py /opt/wavelink/app \
    && python apply_ui94.py /opt/wavelink/app \
    && python apply_ui95.py /opt/wavelink/app \
    && python apply_ui96.py /opt/wavelink/app \
    && python apply_ui97.py /opt/wavelink/app \
    && python apply_ui99.py /opt/wavelink/app \
    && python apply_ui100.py /opt/wavelink/app \
    && python apply_ui101.py /opt/wavelink/app \
    && python apply_ui102.py /opt/wavelink/app \
    && python apply_ui103.py /opt/wavelink/app \
    && python apply_ui104.py /opt/wavelink/app \
    && python apply_ui105.py /opt/wavelink/app \
    && python apply_ui106.py /opt/wavelink/app \
    && rm vendor/source.part* vendor/source_parts.json extract_source.py apply_ui93.py apply_ui94.py apply_ui95.py apply_ui96.py apply_ui97.py apply_ui99.py apply_ui100.py apply_ui101.py apply_ui102.py apply_ui103.py apply_ui104.py apply_ui105.py apply_ui106.py
COPY vendor/FICTIONAL_DEMO.ajproject ./vendor/FICTIONAL_DEMO.ajproject
COPY deploy ./deploy
COPY ops ./ops
# Runtime starts with mount ownership setup and immediately drops to UID 10001.
# Never install/open the Windows Admin or run its launcher in the container.
EXPOSE 10000
CMD ["python", "-m", "deploy.entrypoint"]
