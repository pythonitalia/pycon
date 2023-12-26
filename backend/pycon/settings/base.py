import stripe
import environ
from django.utils.translation import gettext_lazy as _

root = environ.Path(__file__) - 3

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    FRONTEND_URL=(str, "http://localhost:3000"),
)

environ.Env.read_env(root(".env"))

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

FRONTEND_URL = env("FRONTEND_URL")

# Application definition

INSTALLED_APPS = [
    "users",
    # CMS parts
    "cms.components.base",
    "cms.components.home",
    "cms.components.news",
    "cms.components.page",
    "cms.components.sites",
    # CMS
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    # --
    "schedule.apps.ScheduleConfig",
    "custom_admin",
    "dal",
    "dal_select2",
    "dal_admin_filters",
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.ApiConfig",
    "timezone_field",
    "strawberry.django",
    "conferences.apps.ConferencesConfig",
    "languages.apps.LanguagesConfig",
    "submissions.apps.SubmissionsConfig",
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
    "invoices",
    "job_board",
    "import_export",
    "volunteers_notifications.apps.VolunteersNotificationsConfig",
    "checklist.apps.ChecklistConfig",
    "participants.apps.ParticipantsConfig",
    "reviews.apps.ReviewsConfig",
    "markdownify.apps.MarkdownifyConfig",
    "imagekit",
    "badge_scanner",
    "badges.apps.BadgesConfig",
    "google_api.apps.GoogleApiConfig",
    "association_membership.apps.AssociationMembershipConfig",
    "rest_framework",
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
    # "qinspect.middleware.QueryInspectMiddleware",
]

ROOT_URLCONF = "pycon.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "custom_admin.context_processors.admin_settings",
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


USE_TZ = True

STATICFILES_DIRS = [root("assets")]

STATIC_URL = "/django-static/"
STATIC_ROOT = root("static")

MEDIA_URL = "/media/"
MEDIA_ROOT = root("media")

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    # "custom_auth.backend.UsersAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
)

MAPBOX_PUBLIC_API_KEY = env("MAPBOX_PUBLIC_API_KEY", default="")

SERIALIZATION_MODULES = {"json": "i18n.serializers"}
USE_X_FORWARDED_HOST = False

PRETIX_API = env("PRETIX_API", default="")
PRETIX_API_TOKEN = None

STORAGES = {
    "default": {
        "BACKEND": env(
            "MEDIA_FILES_STORAGE_BACKEND", default="pycon.storages.CustomS3Boto3Storage"
        )
    },
    "conferencevideos": {
        "BACKEND": "pycon.storages.ConferenceVideosStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
IMAGEKIT_DEFAULT_FILE_STORAGE = env(
    "MEDIA_FILES_STORAGE_BACKEND", default="pycon.storages.CustomS3Boto3Storage"
)

if PRETIX_API:
    PRETIX_API_TOKEN = env("PRETIX_API_TOKEN")

SIMULATE_PRETIX_DB = True

ENVIRONMENT = env("ENV", default="local")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "pycon.api": {"handlers": ["console"], "level": "WARNING", "propagate": True},
        "pycon.integrations": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "celery": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "qinspect": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
    },
}

QUERY_INSPECT_ENABLED = DEBUG
QUERY_INSPECT_LOG_QUERIES = True
QUERY_INSPECT_LOG_TRACEBACKS = True
QUERY_INSPECT_TRACEBACK_ROOTS = [root(".")]

PINPOINT_APPLICATION_ID = env("PINPOINT_APPLICATION_ID", default="")

SQS_QUEUE_URL = env("SQS_QUEUE_URL", default="")

MAILCHIMP_SECRET_KEY = env("MAILCHIMP_SECRET_KEY", default="")
MAILCHIMP_DC = env("MAILCHIMP_DC", default="us3")
MAILCHIMP_LIST_ID = env("MAILCHIMP_LIST_ID", default="")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

PYTHONIT_EMAIL_BACKEND = env(
    "PYTHONIT_EMAIL_BACKEND",
    default="pythonit_toolkit.emails.backends.local.LocalEmailBackend",
)
DEFAULT_EMAIL_FROM = env("DEFAULT_EMAIL_FROM", default="noreply@pycon.it")

SPEAKERS_EMAIL_ADDRESS = env("SPEAKERS_EMAIL_ADDRESS", default="")

VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN = env(
    "VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN", default=""
).strip()
VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN = env(
    "VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN", default=""
).strip()

AZURE_ACCOUNT_NAME = AZURE_STORAGE_ACCOUNT_NAME = env(
    "AZURE_STORAGE_ACCOUNT_NAME", default=""
)
AZURE_ACCOUNT_KEY = AZURE_STORAGE_ACCOUNT_KEY = env(
    "AZURE_STORAGE_ACCOUNT_KEY", default=""
)

USER_ID_HASH_SALT = env("USER_ID_HASH_SALT", default="")

PLAIN_API = env("PLAIN_API", default="")
PLAIN_API_TOKEN = env("PLAIN_API_TOKEN", default="")

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"

CACHES = {
    "default": env.cache(default="locmemcache://snowflake"),
}

TEMPORAL_ADDRESS = env("TEMPORAL_ADDRESS", default="")

SESSION_COOKIE_NAME = "pythonitalia_sessionid"
CSRF_USE_SESSIONS = True
CSRF_COOKIE_SECURE = DEBUG is False

# Stripe
STRIPE_SECRET_API_KEY = env("STRIPE_SECRET_API_KEY")
STRIPE_SUBSCRIPTION_PRICE_ID = env("STRIPE_SUBSCRIPTION_PRICE_ID")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SIGNATURE_SECRET")

stripe.api_key = STRIPE_SECRET_API_KEY

PRETIX_WEBHOOK_SECRET = env("PRETIX_WEBHOOK_SECRET", default="")

ASSOCIATION_FRONTEND_URL = env("ASSOCIATION_FRONTEND_URL", default="")

# Wagtail CMS
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", "English"),
    ("it", "Italian"),
]

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://cms.python.it"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAIL_SITE_NAME = "cms"
WAGTAIL_I18N_ENABLED = True

DEEPL_AUTH_KEY = env("DEEPL_AUTH_KEY", default="")

if DEEPL_AUTH_KEY:
    WAGTAILLOCALIZE_MACHINE_TRANSLATOR = {
        "CLASS": "wagtail_localize.machine_translators.deepl.DeepLTranslator",
        "OPTIONS": {
            "AUTH_KEY": DEEPL_AUTH_KEY,
        },
    }

FLODESK_API_KEY = env("FLODESK_API_KEY", default="")
FLODESK_SEGMENT_ID = env("FLODESK_SEGMENT_ID", default="")
