from . import base

DEBUG = True

INSTALLED_APPS = base.INSTALLED_APPS + [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + base.MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

DATABASES = base.DATABASES
ALLOWED_HOSTS = base.ALLOWED_HOSTS
STATIC_URL = base.STATIC_URL
