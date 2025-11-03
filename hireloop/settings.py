"""
Django settings for hireloop project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# CRITICAL: Use environment variable in production, fallback for collectstatic
SECRET_KEY = os.getenv(
    "SECRET_KEY", 
    "django-insecure-@))4gro63qr1xtk@a5_ic+u!p04#_w21i$l*wh*-t871@akw3o"
)

# DEBUG should be False in production
DEBUG = True

# Allowed hosts from environment
ALLOWED_HOSTS_ENV = os.getenv(
    "ALLOWED_HOSTS",
    "hireloop.software,www.hireloop.software,localhost,127.0.0.1"
)
ALLOWED_HOSTS = ALLOWED_HOSTS_ENV.split(",")

# Configuración para aceptar health checks de Kubernetes
# Permitir cualquier host interno de Kubernetes (10.x.x.x)
if not DEBUG:
    # En producción, permite IPs internas de pods
    ALLOWED_HOSTS.append('.cluster.local')
    ALLOWED_HOSTS.append('*')  # Temporal para debugging
else:
    ALLOWED_HOSTS.append('*')

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://hireloop.software,https://www.hireloop.software"
).split(",")

# Auth redirects
LOGIN_URL = '/core/login/'
LOGIN_REDIRECT_URL = '/core/profile/'
LOGOUT_REDIRECT_URL = '/'

# Security settings (only in production)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # NO forzar SSL redirect - el Load Balancer maneja HTTPS
    SECURE_SSL_REDIRECT = False  # Cambiado a False
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SAMESITE = "Lax"  # Changed from "None" for better security
CSRF_COOKIE_SAMESITE = "Lax"

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ==============================================================================
# STRIPE
# ==============================================================================

STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

# ==============================================================================
# LOGGING
# ==============================================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# ==============================================================================
# APPLICATIONS
# ==============================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "taggit",
    "core",
    "microservices",
    "projects",
    "mentorship_session",
    "cart",
    "payments",
    "django_plotly_dash.apps.DjangoPlotlyDashConfig",
    "channels",
    "analytics",
    "rest_framework",
    'storages',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}

MIDDLEWARE = [
    "core.middleware.HealthCheckMiddleware",  # PRIMERO - permite health checks
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_plotly_dash.middleware.BaseMiddleware",
    "django_plotly_dash.middleware.ExternalRedirectionMiddleware",
]


WHITENOISE_AUTOREFRESH = True 
WHITENOISE_USE_FINDERS = True

ROOT_URLCONF = "hireloop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.user_profile_type",
                "core.context_processors.cart_and_wishlist_counts",
            ],
        },
    },
]

WSGI_APPLICATION = "hireloop.wsgi.application"

# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "hireloop"),
        "USER": os.getenv("DB_USER", "webuser"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
        "CONN_MAX_AGE": 600,  # Connection pooling
        "OPTIONS": {
            "connect_timeout": 10,
        }
    }
}

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise configuration for efficient static file serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================================================================
# GOOGLE CLOUD STORAGE (GCS) for MEDIA FILES
# ==============================================================================
# Set credentials BEFORE importing storages
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/creds/credentials.json"

# Modern Django 5.x STORAGES setting
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# GCS Configuration
GS_BUCKET_NAME = 'hireloop-media'
GS_DEFAULT_ACL = None
GS_QUERYSTRING_AUTH = False  # URLs públicas sin firma
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

PROFILE_STORAGE_TYPE = "gcs"

# ==============================================================================
# DJANGO PLOTLY DASH
# ==============================================================================

PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_bootstrap_components',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

# ==============================================================================
# OTHER SETTINGS
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "core.User"
X_FRAME_OPTIONS = "SAMEORIGIN"
