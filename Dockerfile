# Existing Wavelink container. UI137 prepared locally; no live deployment performed.
# Company data remains on the existing persistent disk; no reset is performed.
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
COPY deploy/extract_source.py deploy/apply_ui93.py deploy/apply_ui94.py deploy/apply_ui95.py deploy/apply_ui96.py deploy/apply_ui97.py deploy/apply_ui99.py deploy/apply_ui100.py deploy/apply_ui101.py deploy/apply_ui102.py deploy/apply_ui103.py deploy/apply_ui104.py deploy/apply_ui105.py deploy/apply_ui106.py deploy/apply_ui107.py deploy/apply_ui108.py deploy/apply_ui109.py deploy/apply_ui110.py deploy/apply_ui111.py deploy/apply_ui112.py deploy/apply_ui113.py deploy/apply_ui114.py deploy/apply_ui115.py deploy/apply_ui116.py deploy/apply_ui117.py deploy/apply_ui118.py deploy/apply_ui119.py deploy/apply_ui120.py deploy/apply_ui121.py deploy/apply_ui122.py deploy/apply_ui123.py deploy/apply_ui124.py deploy/apply_ui125.py deploy/apply_ui126.py deploy/apply_ui127.py deploy/apply_ui128.py deploy/apply_ui129.py deploy/apply_ui130.py deploy/apply_ui131.py deploy/apply_ui132.py deploy/apply_ui133.py deploy/apply_ui134.py deploy/apply_ui135.py deploy/apply_ui136.py deploy/apply_ui137.py ./
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
    && python apply_ui107.py /opt/wavelink/app \
    && python apply_ui108.py /opt/wavelink/app \
    && python apply_ui109.py /opt/wavelink/app \
    && python apply_ui110.py /opt/wavelink/app \
    && python apply_ui111.py /opt/wavelink/app \
    && python apply_ui112.py /opt/wavelink/app \
    && python apply_ui113.py /opt/wavelink/app \
    && python apply_ui114.py /opt/wavelink/app \
    && python apply_ui115.py /opt/wavelink/app \
    && python apply_ui116.py /opt/wavelink/app \
    && python apply_ui117.py /opt/wavelink/app \
    && python apply_ui118.py /opt/wavelink/app \
    && python apply_ui119.py /opt/wavelink/app \
    && python apply_ui120.py /opt/wavelink/app \
    && python apply_ui121.py /opt/wavelink/app \
    && python apply_ui122.py /opt/wavelink/app \
    && python apply_ui123.py /opt/wavelink/app \
    && python apply_ui124.py /opt/wavelink/app \
    && python apply_ui125.py /opt/wavelink/app \
    && python apply_ui126.py /opt/wavelink/app \
    && python apply_ui127.py /opt/wavelink/app \
    && python apply_ui128.py /opt/wavelink/app \
    && python apply_ui129.py /opt/wavelink/app \
    && python apply_ui130.py /opt/wavelink/app \
    && python apply_ui131.py /opt/wavelink/app \
    && python apply_ui132.py /opt/wavelink/app \
    && python apply_ui133.py /opt/wavelink/app \
    && python apply_ui134.py /opt/wavelink/app \
    && python apply_ui135.py /opt/wavelink/app \
    && python apply_ui136.py /opt/wavelink/app \
    && python apply_ui137.py /opt/wavelink/app \
    && rm vendor/source.part* vendor/source_parts.json extract_source.py apply_ui93.py apply_ui94.py apply_ui95.py apply_ui96.py apply_ui97.py apply_ui99.py apply_ui100.py apply_ui101.py apply_ui102.py apply_ui103.py apply_ui104.py apply_ui105.py apply_ui106.py apply_ui107.py apply_ui108.py apply_ui109.py apply_ui110.py apply_ui111.py apply_ui112.py apply_ui113.py apply_ui114.py apply_ui115.py apply_ui116.py apply_ui117.py apply_ui118.py apply_ui119.py apply_ui120.py apply_ui121.py apply_ui122.py apply_ui123.py apply_ui124.py apply_ui125.py apply_ui126.py apply_ui127.py apply_ui128.py apply_ui129.py apply_ui130.py apply_ui131.py apply_ui132.py apply_ui133.py apply_ui134.py apply_ui135.py apply_ui136.py apply_ui137.py
COPY vendor/FICTIONAL_DEMO.ajproject ./vendor/FICTIONAL_DEMO.ajproject
COPY deploy ./deploy
COPY ops ./ops
# Runtime starts with mount ownership setup and immediately drops to UID 10001.
# Never install/open the Windows Admin or run its launcher in the container.
EXPOSE 10000
CMD ["python", "-m", "deploy.entrypoint"]
