import environ

root = environ.Path(__file__) - 3  # three folder back (/a/b/c/ - 3 = /)

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    FRONTEND_URL=(str, "http://testfrontend.it/"),
)

environ.Env.read_env(root(".env"))

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

FRONTEND_URL = env("FRONTEND_URL")

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
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
    "conferences.apps.ConferencesConfig",
    "languages.apps.LanguagesConfig",
    "submissions.apps.SubmissionsConfig",
    "schedule.apps.ScheduleConfig",
    "orders.apps.OrdersConfig",
    "payments.apps.PaymentsConfig",
    "tickets.apps.TicketsConfig",
    "voting.apps.VotingConfig",
    "blog.apps.BlogConfig",
    "pages.apps.PagesConfig",
    "importer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

LANGUAGE_CODE = "en-us"

LOCALE_PATHS = [root("locale")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_DIRS = [root("assets")]

STATIC_URL = "/static/"
STATIC_ROOT = root("static")

MEDIA_URL = "/media/"
MEDIA_ROOT = root("media")

AUTH_USER_MODEL = "users.User"
SOCIAL_AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default="")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", default="")

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_LOGIN_REDIRECT_URL = f"{FRONTEND_URL}/login/success/"
SOCIAL_AUTH_LOGIN_ERROR_URL = f"{FRONTEND_URL}/login/error/"

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET", default="")

CELERY_BROKER_URL = ""
SLACK_INCOMING_WEBHOOK_URl = ""
USE_SCHEDULER = False

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MAPBOX_PUBLIC_API_KEY = env("MAPBOX_PUBLIC_API_KEY", default="")
