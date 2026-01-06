FROM node:22 AS tailwind

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY tailwind.config.js postcss.config.js ./

COPY templates ./templates
COPY static ./static

RUN npm run build


FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


FROM python:3.13-slim AS prod

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -m -r -s /bin/bash falaai && \
    mkdir /app && \
    chown -R falaai:falaai /app

WORKDIR /app


COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY scripts/entrypoint.sh /scripts/entrypoint.sh
RUN chmod +x /scripts/entrypoint.sh \
    && sed -i 's/\r$//' /scripts/entrypoint.sh

COPY --chown=falaai:falaai . .

RUN mkdir -p /app/staticfiles /app/media && \
    chown -R falaai:falaai /app/staticfiles /app/media

COPY --from=tailwind --chown=falaai:falaai /app/static/ ./static/

USER falaai

ENTRYPOINT ["/scripts/entrypoint.sh"]