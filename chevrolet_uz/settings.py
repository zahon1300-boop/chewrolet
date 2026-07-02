"""
Django settings for Chevrolet UZ project.

Ishlab chiqish (Development) va Production uchun mos sozlamalar.
Environment variables orqali maxfiy ma'lumotlar boshqariladi.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# ==============================================================================
# ASOSIY YO'LLAR
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# XAVFSIZLIK
# ==============================================================================
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-insecure-key-change-in-production-!!!"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

DEFAULT_ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]
ENV_ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split()
ALLOWED_HOSTS = (
    DEFAULT_ALLOWED_HOSTS
    + ENV_ALLOWED_HOSTS
    + [
        "chewrolet-3.onrender.com",
        "chewrolet-7.onrender.com",
        "chewrolet-7777.onrender.com",
        "*.onrender.com",
    ]
)

# ==============================================================================
# ILOVALAR
# ==============================================================================
INSTALLED_APPS = [
    # Django standart
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "django.contrib.humanize",

    "main.apps.MainConfig",
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",       # CSRF himoya
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "main.middleware.AdminRedirectMiddleware",
]

ROOT_URLCONF = "chevrolet_uz.urls"

# ==============================================================================
# SHABLONLAR
# ==============================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.csrf",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "chevrolet_uz.wsgi.application"

# ==============================================================================
# MA'LUMOTLAR BAZASI
# SQLite — ishlab chiqish; PostgreSQL — production
# ==============================================================================
if os.environ.get("USE_POSTGRES", "False") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "chevrolet_uz_db"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
            "CONN_MAX_AGE": 60,
            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ==============================================================================
# AUTENTIFIKATSIYA
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/profile/"
LOGOUT_REDIRECT_URL = "/"

# ==============================================================================
# XALQAROLASHTIRISH (I18N / L10N)
# ==============================================================================
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==============================================================================
# STATIK FAYLLAR
# ==============================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"   # collectstatic uchun
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ==============================================================================
# MEDIA FAYLLAR (Rasmlar va yuklamalar)
# ==============================================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Rasm sifati va o'lchami chegaralari
IMAGE_MAX_WIDTH = 1920
IMAGE_MAX_HEIGHT = 1080
IMAGE_QUALITY = 85          # JPEG sifati (0-100)
THUMBNAIL_SIZE = (300, 200) # Admin panel thumbnail o'lchami

# ==============================================================================
# DEFAULT PRIMARY KEY
# ==============================================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# XAVFSIZLIK SOZLAMALARI (Production uchun)
# ==============================================================================
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000          # 1 yil
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    CSRF_TRUSTED_ORIGINS = os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        ""
    ).split() if os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "") else []

# ==============================================================================
# LOGGING
# ==============================================================================

# Logs papkasini avtomatik yaratish (Windows va Linux uchun)
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "django.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 3,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "main": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
