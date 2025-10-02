import os
import socket
from datetime import timedelta
from pathlib import Path

# Если в dev хочешь грузить .env через python-dotenv — можно раскомментировать:
# from dotenv import load_dotenv
# load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ---------- helpers ----------
def env_bool(env_name: str, default_value: bool = False) -> bool:
    env_value = os.getenv(env_name)
    if env_value is None:
        return default_value
    return env_value.lower() in {"1", "true", "yes", "on"}


def env_int(env_name: str, default_value: int) -> int:
    try:
        return int(os.getenv(env_name, default_value))
    except (TypeError, ValueError):
        return default_value


def env_list(env_name: str, default_value: str = "") -> list[str]:
    return [
        item.strip()
        for item in os.getenv(env_name, default_value).split(",")
        if item.strip()
    ]


# ---------- core ----------
SECRET_KEY = os.getenv("SECRET_KEY", "Specify the SECRET_KEY")
DEBUG = env_bool("DEBUG", False)

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1,backend")

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/login/"

INSTALLED_APPS = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd-party
    "rest_framework",
    "drf_yasg",
    # prometheus — включаем middleware по флагу ниже
    "django_prometheus",
    # project apps
    "core",
    "api",
    "users",
    "phone",
    "management",
    "notification",
    "notification_preferences",
    "extra_settings",
]

MIDDLEWARE = [
    # Prometheus вокруг request/response добавляем только если включили флаг (см. ниже)
    # "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.MaintenanceModeMiddleware",
    # "django_prometheus.middleware.PrometheusAfterMiddleware",
    # Профайлер — подключаем только в dev через флаг (см. dev.py)
]

ROOT_URLCONF = "kanban_board.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kanban_board.wsgi.application"

# ---------- database ----------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "Specify the DB_NAME"),
        "USER": os.getenv("DB_USER", "Specify the DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD", "Specify the DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "Specify the DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# ---------- redis / cache / celery ----------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# Разводим базы: кэш/брокер/результаты/троттлинг
REDIS_DB_CACHE = os.getenv("REDIS_DB_CACHE", "0")
REDIS_DB_BROKER = os.getenv("REDIS_DB_BROKER", "1")
REDIS_DB_BACKEND = os.getenv("REDIS_DB_BACKEND", "2")
REDIS_DB_THROTTLE = os.getenv("REDIS_DB_THROTTLE", "3")

REDIS_URL = os.getenv(
    "REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_CACHE}"
)
CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BROKER}"
)
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BACKEND}"
)

CACHE_KEY_PREFIX = os.getenv("CACHE_KEY_PREFIX", "kanban_default")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "KEY_PREFIX": CACHE_KEY_PREFIX,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": False,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
    }
}

# DRF throttle хранит ключи в кэше — ключи отделяем префиксом
THROTTLE_CACHE_PREFIX = os.getenv("THROTTLE_CACHE_PREFIX", "throttle")

# ---------- DRF ----------
REST_FRAMEWORK = {
    # Auth
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # Throttling
    "DEFAULT_THROTTLE_CLASSES": [
        "core.throttling.SlowUserRateThrottle",
        "core.throttling.SlowAnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": os.getenv("THROTTLE_RATE_USER", "30/min"),
        "anon": os.getenv("THROTTLE_RATE_ANON", "15/min"),
        "auth": os.getenv("THROTTLE_RATE_AUTH", "5/15m"),
        "authRefresh": os.getenv("THROTTLE_RATE_AUTH_REFRESH", "30/hour"),
        "register": os.getenv("THROTTLE_RATE_REGISTER", "3/10m"),
        "registerVerify": os.getenv("THROTTLE_RATE_REGISTER_VERIFY", "5/15m"),
    },
    # Pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": env_int("PAGE_SIZE", 5),
}

# ---------- JWT ----------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}

# ---------- Password policy ----------
STRICT_PASSWORDS = env_bool("STRICT_PASSWORDS", True)
PASSWORD_MIN_LENGTH = env_int("PASSWORD_MIN_LENGTH", 8)

STRICT_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": PASSWORD_MIN_LENGTH},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
RELAXED_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": min(6, PASSWORD_MIN_LENGTH)},
    },
]
AUTH_PASSWORD_VALIDATORS = (
    STRICT_PASSWORD_VALIDATORS if STRICT_PASSWORDS else RELAXED_PASSWORD_VALIDATORS
)

# ---------- Celery ----------
CELERY_BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = env_int("CELERY_TASK_TIME_LIMIT", 30)
CELERY_TASK_SOFT_TIME_LIMIT = env_int("CELERY_TASK_SOFT_TIME_LIMIT", 25)

# ---------- Swagger ----------
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": (
                "JWT авторизация. Передавайте токен в заголовке: "
                "**Authorization: Bearer <токен>**"
            ),
        },
    },
    "PERSIST_AUTH": DEBUG,
    "OPERATIONS_SORTER": "alpha",
    "TAGS_SORTER": "alpha",
    "DOC_EXPANSION": "list",
}

# ---------- i18n ----------
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "ru-ru")
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")
USE_I18N = True
USE_TZ = True

# ---------- static ----------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- logging ----------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}
