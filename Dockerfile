# 1) builder
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install poetry==1.8.0
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-root

# 2) final
FROM python:3.12-slim
WORKDIR /app

# убираем компиляторы, оставляем только runtime зависимости
RUN apt-get update && apt-get install -y libpq-dev

# из билдера копируем ВСЁ из /usr/local: и библиотеки, и скрипты
COPY --from=builder /usr/local /usr/local

# копируем код
COPY . .
