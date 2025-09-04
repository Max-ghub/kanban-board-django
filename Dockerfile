# === builder ===
FROM python:3.12-slim AS builder
RUN pip install poetry==1.8.0
WORKDIR /app
COPY pyproject.toml poetry.lock ./
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then \
      poetry export -f requirements.txt --output /tmp/requirements.txt --without-hashes --with dev; \
    else \
      poetry export -f requirements.txt --output /tmp/requirements.txt --without-hashes; \
    fi

# === runtime ===
FROM python:3.12-slim
RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /tmp/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . .
EXPOSE 8000
