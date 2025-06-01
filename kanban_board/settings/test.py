from .main import *  # noqa

DEBUG = True
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]
MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = ["127.0.0.1"]
