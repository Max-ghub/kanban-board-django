from .base import *

DEBUG = env_bool("DEBUG", True)

# debug-toolbar — если установлен, включаем
try:
    import debug_toolbar  # noqa

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
except Exception:
    pass

# профайлер — включаем по флагу, чтобы случайно не держать всегда включенным
if env_bool("ENABLE_PROFILER", False):
    try:
        import django_cprofile_middleware  # noqa

        MIDDLEWARE.append("django_cprofile_middleware.middleware.ProfilerMiddleware")
    except Exception:
        pass

# prometheus — включаем только по флагу
if env_bool("ENABLE_PROMETHEUS", False):
    MIDDLEWARE.insert(0, "django_prometheus.middleware.PrometheusBeforeMiddleware")
    MIDDLEWARE.append("django_prometheus.middleware.PrometheusAfterMiddleware")

# Browsable API в dev
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# INTERNAL_IPS для docker + toolbar
INTERNAL_IPS = ["127.0.0.1"]
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
