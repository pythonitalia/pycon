import environ
from django.utils.translation import gettext_lazy as _

root = environ.Path(__file__) - 3  # three folder back (/a/b/c/ - 3 = /)

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    FRONTEND_URL=(str, "http://localhost:4000"),
)

environ.Env.read_env(root(".env"))

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

FRONTEND_URL = env("FRONTEND_URL")

# Application definition

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    "dal_admin_filters",
    "whitenoise.runserver_nostatic",
    "admin_views",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.ApiConfig",
    "timezone_field",
    "social_django",
    "users",
    "strawberry.django",
    "conferences.apps.ConferencesConfig",
    "languages.apps.LanguagesConfig",
    "submissions.apps.SubmissionsConfig",
    "schedule.apps.ScheduleConfig",
    "voting.apps.VotingConfig",
    "blog.apps.BlogConfig",
    "pages.apps.PagesConfig",
    "sponsors.apps.SponsorsConfig",
    "cms.apps.CMSConfig",
    "events.apps.EventsConfig",
    "grants.apps.GrantsConfig",
    "i18n",
    "importer",
    "storages",
    "notifications.apps.NotificationsConfig",
    "hotels.apps.HotelsConfig",
    "newsletters.apps.NewslettersConfig",
    "ordered_model",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "qinspect.middleware.QueryInspectMiddleware",
]

ROOT_URLCONF = "pycon.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [root("frontend")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "pycon.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {"default": env.db(default="sqlite:///{}".format(root("db.sqlite3")))}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

PASSWORD_VALIDATORS = [
    "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "django.contrib.auth.password_validation.MinimumLengthValidator",
    "django.contrib.auth.password_validation.CommonPasswordValidator",
    "django.contrib.auth.password_validation.NumericPasswordValidator",
]

AUTH_PASSWORD_VALIDATORS = [{"NAME": validator} for validator in PASSWORD_VALIDATORS]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [("en", _("English")), ("it", _("Italian"))]

LOCALE_PATHS = [root("locale")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_DIRS = [root("assets")]

STATIC_URL = "/django-static/"
STATIC_ROOT = root("static")

MEDIA_URL = "/media/"
MEDIA_ROOT = root("media")

AUTH_USER_MODEL = "users.User"
SOCIAL_AUTH_USER_MODEL = "users.User"

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default="")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", default="")

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_LOGIN_REDIRECT_URL = f"{FRONTEND_URL}/en/login/success/"
# SOCIAL_AUTH_LOGIN_ERROR_URL = f"{FRONTEND_URL}/login/"

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET", default="")

CELERY_BROKER_URL = ""
SLACK_INCOMING_WEBHOOK_URl = ""
USE_SCHEDULER = False

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MAPBOX_PUBLIC_API_KEY = env("MAPBOX_PUBLIC_API_KEY", default="")

SERIALIZATION_MODULES = {"json": "i18n.serializers"}
USE_X_FORWARDED_HOST = False

PRETIX_API = env("PRETIX_API", default="")
PRETIX_API_TOKEN = None

if PRETIX_API:
    PRETIX_API_TOKEN = env("PRETIX_API_TOKEN")

SIMULATE_PRETIX_DB = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "app_api": {"handlers": ["console"], "level": "WARNING"},
        "qinspect": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
    },
}

QUERY_INSPECT_ENABLED = DEBUG
QUERY_INSPECT_LOG_QUERIES = True
QUERY_INSPECT_LOG_TRACEBACKS = True
QUERY_INSPECT_TRACEBACK_ROOTS = [root(".")]

PINPOINT_APPLICATION_ID = env("PINPOINT_APPLICATION_ID", default="")
