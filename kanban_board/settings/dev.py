from .base import *

DEBUG = True

try:
    import debug_toolbar  # noqa

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
except Exception:
    pass

try:
    import django_cprofile_middleware  # noqa

    MIDDLEWARE.append("django_cprofile_middleware.middleware.ProfilerMiddleware")
except Exception:
    pass

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

import socket

INTERNAL_IPS = ["127.0.0.1"]
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
