from .main import *  # noqa

DEBUG = False

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    send_default_pii=True,
    debug=True,
)
