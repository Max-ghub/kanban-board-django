# Kanban Board Backend

Бэкенд для системы управления проектами и задачами по принципам Kanban, реализованный на **Django** и **Django REST Framework**.
Приложение покрывает полный цикл работы: от регистрации пользователя и авторизации через JWT до управления проектами, досками, задачами, уведомлениями и аналитикой.

---

## ⚙️ Возможности

* **Аутентификация и авторизация**
  Кастомная модель пользователя, вход по телефону, выдача JWT токенов (access/refresh) через SimpleJWT.
  Поддержка ограничения частоты запросов (rate limiting, throttling).

* **Управление проектами и участниками**
  CRUD API для проектов, добавление и удаление участников с разграничением ролей (владелец/участник).
  Оптимизация запросов и кеширование списков проектов.

* **Доски и колонки**
  Поддержка сортировки и изменения порядка колонок, кэширование и транзакционная обработка операций.

* **Задачи и подзадачи**
  Статусы Kanban (Backlog → Done), приоритеты, исполнители и иерархия задач.
  Поддержка перемещения задач, назначения исполнителя и создания подзадач с проверкой прав доступа.

* **Уведомления и настройки доставки**
  Поддержка различных каналов (email/SMS, Redis backend), хранение прочитанности и пользовательских предпочтений.

* **Наблюдаемость и мониторинг**
  Интеграция Prometheus и Grafana, профилирование через `django-cprofile-middleware`, логирование и Sentry SDK.

---

## 🧱 Архитектура и стек

| Компонент     | Технологии                                 |
| ------------- | ------------------------------------------ |
| Backend       | Python 3.12, Django 5, DRF                 |
| База данных   | PostgreSQL                                 |
| Очереди / кеш | Redis + Celery                             |
| Документация  | drf-yasg (Swagger/OpenAPI)                 |
| Мониторинг    | Prometheus, Grafana, Sentry                |
| DevTools      | Poetry, Docker Compose, pre-commit, pytest |

---

## 📂 Структура проекта

| Путь                        | Назначение                              |
| --------------------------- | --------------------------------------- |
| `kanban_board/`             | Основные настройки Django и Celery      |
| `management/`               | Домены: проекты, доски, колонки, задачи |
| `users/`                    | Пользователи, JWT, SMS-подтверждение    |
| `notification/`             | Модель уведомлений и API                |
| `notification_preferences/` | Настройки уведомлений                   |
| `phone/`                    | Генерация и проверка SMS-кодов          |
| `api/v1/`                   | Сборка REST API v1 и маршрутизация      |

---

## 🚀 Быстрый старт (локально)

```bash
git clone https://github.com/Max-ghub/kanban-board-django.git
cd kanban-board-django
poetry install
cp .env.example .env
poetry run python manage.py migrate
poetry run python manage.py runserver
poetry run celery -A kanban_board worker -l info
```

Минимальный `.env`:

```dotenv
SECRET_KEY=dev-secret
DEBUG=1
DB_NAME=kanban
DB_USER=kanban
DB_PASSWORD=kanban
DB_HOST=localhost
REDIS_HOST=localhost
```

---

## 🐳 Запуск в Docker

```bash
make run-dev
# или фоновый запуск:
make run-dev-d
```

Окружение поднимет:

* **Django API** → [http://localhost:8000](http://localhost:8000)
* **Swagger UI** → [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* **Prometheus** → [http://localhost:9090](http://localhost:9090)
* **Grafana** → [http://localhost:3000](http://localhost:3000)

Для продакшн:

```bash
make run-prod
```

---

## 🧪 Тестирование и стиль кода

```bash
poetry run pytest
poetry run pre-commit install
poetry run pre-commit run --all-files
```

Инструменты:

* `pytest` — тесты и фикстуры
* `black`, `flake8`, `isort` — автоформат и линтер
* `mypy` (можно добавить для строгой типизации)

---

## 🧠 Архитектурные решения

* **Feature Flags** через `django-extra-settings`
* **Фоновая обработка SMS и уведомлений** на Celery
* **Кеширование ответов API** и `cache_response` decorator
* **Гибкая пагинация DRF** с `PageNumberPagination`
* **ORM-оптимизация** (`select_related`, `prefetch_related`)
* **Role-based permissions** (`IsProjectOwner`, `IsProjectMemberOrOwner`)

---

## 📊 Мониторинг и профилирование

* **Prometheus** собирает метрики Django и Celery.
* **Grafana** визуализирует метрики по API latency, ошибкам, нагрузке.
* **Sentry SDK** отслеживает исключения и перформанс.
* **ApacheBench** и `django-cprofile` помогают измерять производительность.

---

## 📘 Документация API

* **Swagger UI** — `/swagger/`
* **Redoc** — `/redoc/`
* Генерация OpenAPI-схемы автоматически через `drf-yasg`.

---