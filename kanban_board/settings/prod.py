from .base import *

DEBUG = False

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1,backend")
CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS", "https://localhost,https://backend"
)

# Безопасность prod
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", True)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", True)
SECURE_HSTS_SECONDS = env_int("SECURE_HSTS_SECONDS", 31536000)  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", True)

# nginx/ingress
if env_bool("USE_X_FORWARDED_PROTO", True):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Prometheus в prod включаем только осознанно
if env_bool("ENABLE_PROMETHEUS", False):
    MIDDLEWARE.insert(0, "django_prometheus.middleware.PrometheusBeforeMiddleware")
    MIDDLEWARE.append("django_prometheus.middleware.PrometheusAfterMiddleware")

# Логи
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
for logger in (LOGGING.get("loggers") or {}).values():
    logger["level"] = LOG_LEVEL
LOGGING["root"]["level"] = LOG_LEVEL
