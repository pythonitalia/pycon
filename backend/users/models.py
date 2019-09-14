from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from pycountry import countries

from .managers import UserManager

COUNTRIES = [{"code": country.alpha_2, "name": country.name} for country in countries]
EU_COUNTRIES = (
    "AT",
    "BE",
    "BG",
    "CY",
    "CZ",
    "DK",
    "EE",
    "FI",
    "FR",
    "DE",
    "GR",
    "HU",
    "HR",
    "IE",
    "IT",
    "LV",
    "LT",
    "LU",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SK",
    "SI",
    "ES",
    "SE",
    "GB",
)


def get_countries(code=""):
    if code:
        country = [country for country in COUNTRIES if country["code"] == code]
        if country:
            return country[0]
        raise exceptions.ObjectDoesNotExist(f"'{code}' is not a valid country.")
    return COUNTRIES


class User(AbstractBaseUser, PermissionsMixin):
    image = models.ImageField(_("image"), upload_to="user_image", null=True, blank=True)
    username = models.CharField(_("username"), max_length=100, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=300, blank=True)
    name = models.CharField(_("name"), max_length=300, blank=True)

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    GENDERS = Choices(("male", _("Male")), ("female", _("Female")))
    gender = models.CharField(_("gender"), choices=GENDERS, max_length=10, blank=True)
    date_birth = models.DateField(_("date of birth"), null=True)
    open_to_recruiting = models.BooleanField(_("open to recruiting"), default=False)
    open_to_newsletter = models.BooleanField(_("open to newsletter"), default=False)

    country = models.CharField(
        choices=COUNTRIES, max_length=50, verbose_name=_("country"), blank=True
    )

    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("is staff"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_short_name(self):
        return self.email

    def clean(self):
        # TODO check required field here i.e. company-required-fileds?
        pass

    def is_eu(self):
        if self.country in EU_COUNTRIES:
            return True
        return False

    def is_italian(self):
        if self.country == "IT":
            return True
        return False
