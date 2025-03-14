import json
import stripe
import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.strawberry import StrawberryIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

root = environ.Path(__file__) - 3

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    FRONTEND_URL=(str, "http://localhost:3000"),
    CLAMAV_PORT=(int, 3310),
)

environ.Env.read_env(root(".env"))

ENVIRONMENT = env("ENV", default="local")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

FRONTEND_URL = env("FRONTEND_URL")

SENTRY_DSN = env("SENTRY_DSN", default="")

GITHASH = env("GITHASH", default="")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            AwsLambdaIntegration(),
            StrawberryIntegration(async_execution=False),
            CeleryIntegration(monitor_beat_tasks=True),
        ],
        traces_sample_rate=0.4,
        profiles_sample_rate=0.4,
        send_default_pii=True,
        environment=ENVIRONMENT,
        release=GITHASH,
    )

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
    "wagtail_headless_preview",
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
    "integrations.apps.IntegrationsConfig",
    "healthchecks.apps.HealthchecksConfig",
    "files_upload.apps.FilesUploadConfig",
    "video_uploads.apps.VideoUploadsConfig",
    "organizers.apps.OrganizersConfig",
    "billing.apps.BillingConfig",
    "privacy_policy.apps.PrivacyPolicyConfig",
    "visa.apps.VisaConfig",
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

# Django Debug Toolbar

ENABLE_DJANGO_DEBUG_TOOLBAR: bool = env.bool(
    "ENABLE_DJANGO_DEBUG_TOOLBAR", default=False
)


if ENABLE_DJANGO_DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")

    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda _: DEBUG,
        "SHOW_COLLAPSED": True,
    }

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

ROOT_URLCONF = "pycon.urls"

FORM_RENDERER = "custom_admin.template_backends.FormRenderer"

TEMPLATES = [
    {
        "BACKEND": "custom_admin.template_backends.CustomAdminDjangoTemplate",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "custom_admin.context_processors.admin_settings",
            ],
            "builtins": [
                "custom_admin.templatetags.to_json_for_prop",
                "custom_admin.templatetags.empty_string_if_none",
            ],
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
    "users.backends.PermissionsBackend",
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
            "MEDIA_FILES_STORAGE_BACKEND",
            default="pycon.storages.CustomFileSystemStorage",
        )
    },
    "private": {
        "BACKEND": env(
            "MEDIA_FILES_PRIVATE_STORAGE_BACKEND",
            default="pycon.storages.CustomFileSystemStorage",
        )
    },
    "localstorage": {
        "BACKEND": "pycon.storages.CustomFileSystemStorage",
        "LOCATION": "/tmp/",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
IMAGEKIT_DEFAULT_FILE_STORAGE = env(
    "MEDIA_FILES_STORAGE_BACKEND", default="pycon.storages.CustomFileSystemStorage"
)

if PRETIX_API:
    PRETIX_API_TOKEN = env("PRETIX_API_TOKEN")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "pycon.api": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
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
        "celery.app.trace": {
            "handlers": ["console"],
            "level": "INFO",
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

MAILCHIMP_SECRET_KEY = env("MAILCHIMP_SECRET_KEY", default="")
MAILCHIMP_DC = env("MAILCHIMP_DC", default="us3")
MAILCHIMP_LIST_ID = env("MAILCHIMP_LIST_ID", default="")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SPEAKERS_EMAIL_ADDRESS = env("SPEAKERS_EMAIL_ADDRESS", default="")

VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN = env(
    "VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN", default=""
).strip()
VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN = env(
    "VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN", default=""
).strip()

USER_ID_HASH_SALT = env("USER_ID_HASH_SALT", default="")

PLAIN_API = env("PLAIN_API", default="")
PLAIN_API_TOKEN = env("PLAIN_API_TOKEN", default="")
PLAIN_INTEGRATION_TOKEN = env("PLAIN_INTEGRATION_TOKEN", default="")

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"

REDIS_URL = env("CACHE_URL", default="")

CACHES = {
    "default": env.cache(default="locmemcache://snowflake"),
}

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

OPENAI_API_KEY = env("OPENAI_API_KEY", default="")

if OPENAI_API_KEY:
    WAGTAILLOCALIZE_MACHINE_TRANSLATOR = {
        "CLASS": "cms.translator.OpenAITranslator",
        "OPTIONS": {},
    }

FLODESK_API_KEY = env("FLODESK_API_KEY", default="")
FLODESK_SEGMENT_ID = env("FLODESK_SEGMENT_ID", default="")

WAGTAIL_HEADLESS_PREVIEW = {
    "CLIENT_URLS": {"default": "{SITE_ROOT_URL}/api/page-preview"},
    "SERVE_BASE_URL": None,
    "REDIRECT_ON_PREVIEW": False,
    "ENFORCE_TRAILING_SLASH": False,
}

X_FRAME_OPTIONS = "SAMEORIGIN"

CELERY_TASK_IGNORE_RESULT = True

AWS_STORAGE_BUCKET_NAME = env("AWS_MEDIA_BUCKET", default=None)
AWS_REGION_NAME = AWS_SES_REGION_NAME = AWS_S3_REGION_NAME = env(
    "AWS_REGION_NAME", default="eu-central-1"
)
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default=None)
AWS_SESSION_TOKEN = env("AWS_SESSION_TOKEN", default=None)

CLAMAV_HOST = env("CLAMAV_HOST", default=None)
CLAMAV_PORT = env("CLAMAV_PORT", default=3310)

IS_RUNNING_TESTS = False

try:
    ECS_NETWORK_CONFIG = json.loads(env("ECS_NETWORK_CONFIG", default=""))
except json.decoder.JSONDecodeError:
    ECS_NETWORK_CONFIG = {}

ECS_SERVICE_ROLE = env("ECS_SERVICE_ROLE", default="")

SNS_WEBHOOK_SECRET = env("SNS_WEBHOOK_SECRET", default="")

USE_SES_V2 = True

AWS_SES_CONFIGURATION_SET = env("AWS_SES_CONFIGURATION_SET", default="")
DEFAULT_FROM_EMAIL = "noreply@pycon.it"
