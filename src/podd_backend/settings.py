import os
from pathlib import Path

from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def env_boolean(key: str, default: bool = False):
    if key in os.environ:
        return os.environ[key].lower() not in ("false", "no", "0")
    return default


SRC_DIR = Path(__file__).resolve().parent
BASE_DIR = SRC_DIR.parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = env_boolean("DEBUG")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]").split(",")
INTERNAL_IPS = os.environ.get("INTERNAL_IPS", "127.0.0.1").split(",")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
DJANGO_DB = os.environ.get("DJANGO_DB", ENVIRONMENT)
ADMINS = [(os.environ.get("ADMIN_NAME", "Admin"), os.environ.get("ADMIN_EMAIL", "root@localhost"))]


# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions", # needed for admin
    "django.contrib.messages", # needed for admin
    "django.contrib.staticfiles", # needed for admin and REST browsable API
    "cachalot",
    "django_extensions",
    "rest_framework", # needed for REST browsable API
    "rest_framework_json_api", # needed for REST browsable API
    "corsheaders",
    "django_filters", # needed for REST browsable API
    "martor", # needed for Episode, Podcast & Post admin
    "spodcat",
    "spodcat.logs",
    "spodcat.contrib.admin",
    "podd_backend",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "podd_backend.middleware.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

try:
    # pylint: disable=unused-import
    import debug_toolbar

    # INSTALLED_APPS.append("debug_toolbar")
    # MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
except ImportError:
    pass

ROOT_URLCONF = "podd_backend.urls"

X_FRAME_OPTIONS = "SAMEORIGIN"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [SRC_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = f"{SRC_DIR.name}.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES: dict[str, dict] = {
    "local": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "production": {
        "ENGINE": os.environ.get("PROD_SQL_ENGINE"),
        "NAME": os.environ.get("PROD_SQL_DB"),
        "PASSWORD": os.environ.get("PROD_SQL_PASSWORD"),
        "HOST": os.environ.get("PROD_SQL_HOST"),
        "USER": os.environ.get("PROD_SQL_USER"),
    },
}
DATABASES["default"] = DATABASES[DJANGO_DB].copy()


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "podd_backend.User"


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "sv"
TIME_ZONE = "Europe/Stockholm"
USE_I18N = True
USE_TZ = True
FORMAT_MODULE_PATH = ["formats"]
LOCALE_PATHS = [SRC_DIR / "locale"]
LANGUAGES = [
    ("en", _("English")),
    ("sv", _("Swedish")),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = []
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", BASE_DIR / "media")

AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME", "musikensmakt")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_FILES_KEY")
AZURE_CONTAINER = os.environ.get("AZURE_CONTAINER", "spodcat-backend")
AZURE_LOCATION = ENVIRONMENT
AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")
AZURE_RESOURCE_GROUP = os.environ.get("AZURE_RESOURCE_GROUP")
AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")

STORAGES = {
    "default": {"BACKEND": "storages.backends.azure_storage.AzureStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    "local": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
}
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "root@localhost")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "root@localhost")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 25)
EMAIL_USE_TLS = env_boolean("EMAIL_USE_TLS")


# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "spodcat.logging.AdminEmailHandler",
            "include_html": True,
            "filters": ["require_debug_false"],
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "spodcat": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "pydub.converter": {
            "handlers": ["console"],
            "level": "DEBUG",
        }
    },
}


# django-cors-headers
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://backend.musikensmakt.huseli.us",
    "https://musikensmakt.huseli.us",
    "https://backend.podd.huseli.us",
    "https://podd.huseli.us",
]


# django-debug-toolbar
def show_toolbar(request: HttpRequest):
    from django.conf import settings

    remote_addr = str(request.META.get("REMOTE_ADDR", ""))
    return settings.DEBUG and (remote_addr in settings.INTERNAL_IPS or remote_addr.startswith("192.168"))


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.alerts.AlertsPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "cachalot.panels.CachalotPanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


# martor
MARTOR_ENABLE_LABEL = True


# Caching
redis_db = os.environ.get("REDIS_DB", "0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://127.0.0.1:6379/{redis_db}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}
CACHALOT_DATABASES = ["default"]


# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}


SPODCAT = {
    "FRONTEND_ROOT_URL": os.environ.get("FRONTEND_ROOT_URL"),
    "ROOT_URL": os.environ.get("ROOT_URL"),
    "FILEFIELDS": {
        "FONTFACE_FILE": {"STORAGE": "local"},
    },
}
