FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev \
 && pip install poetry==1.8.0 && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
