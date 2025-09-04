import os

import sentry_sdk

from .base import *


def getenv_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


DEBUG = False

ALLOWED_HOSTS = [
    h for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,backend").split(",") if h
]
CSRF_TRUSTED_ORIGINS = [
    o
    for o in os.getenv(
        "CSRF_TRUSTED_ORIGINS", "http://localhost,http://backend:8000"
    ).split(",")
    if o
]

STATIC_ROOT = os.getenv("STATIC_ROOT", "/app/staticfiles")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = getenv_bool("SECURE_SSL_REDIRECT", False)

SESSION_COOKIE_SECURE = getenv_bool("SESSION_COOKIE_SECURE", SECURE_SSL_REDIRECT)
CSRF_COOKIE_SECURE = getenv_bool("CSRF_COOKIE_SECURE", SECURE_SSL_REDIRECT)

SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = getenv_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = getenv_bool("SECURE_HSTS_PRELOAD", False)

dsn = os.getenv("SENTRY_DSN", "")
if dsn:
    sentry_sdk.init(dsn=dsn, send_default_pii=True)
