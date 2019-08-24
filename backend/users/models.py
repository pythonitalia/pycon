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

[
    {"code": country.alpha_2, "name": country.name}
    for country in countries
    if country.alpha_2 in EU_COUNTRIES
]


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

    business_name = models.CharField(_("business name"), max_length=150, blank=True)
    fiscal_code = models.CharField(_("fiscal code"), max_length=16, blank=True)
    vat_number = models.CharField(_("VAT number"), max_length=22, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=20, blank=True)

    # electronic invoicing ita
    recipient_code = models.CharField(_("recipient code"), max_length=7, blank=True)
    pec_address = models.EmailField(_("PEC"), blank=True)

    address = models.TextField(_("address"), blank=True)
    country = models.CharField(
        choices=COUNTRIES, max_length=50, verbose_name=_("country"), null=True
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

    def clean_business_fields(self):

        if not self.business_name:
            raise exceptions.ValidationError(
                {"business_name": _("Missing Business Name in your user profile.")}
            )

        if not self.phone_number:
            raise exceptions.ValidationError(
                {"phone_number": _("Missing Phone Number in your user profile.")}
            )

        if not self.country:
            raise exceptions.ValidationError(
                {"country": _("Missing Country in your user profile.")}
            )

        if not self.is_eu():
            return

        if self.is_italian():

            # TODO check fiscal code with italian roles...
            #  but first you have to split the address for get CAP!

            if not self.fiscal_code and not self.vat_number:
                raise exceptions.ValidationError(
                    _("Please specify Fiscal Code or VAT number in your user profile.")
                )

            if self.fiscal_code:
                self.clean_fiscal_code()

            if not self.recipient_code and not self.pec_address:
                raise exceptions.ValidationError(
                    _(
                        "For Italian companies for electronic invoicing it is "
                        "mandatory to specify the recipient's code or the pec address."
                    )
                )
            return

        if not self.vat_number:
            raise exceptions.ValidationError(
                {"vat_number": _("Missing VAT Number in your user profile.")}
            )

    def clean_fiscal_code(self):
        msg = _("Fiscal Code is invalid")
        if not len(self.fiscal_code) == 16:
            raise exceptions.ValidationError(
                {"fiscal_code": _("Fiscal Code is invalid: length != 16")}
            )

        if not self.fiscal_code[:6].isalpha():
            raise exceptions.ValidationError({"fiscal_code": msg})

        # year of birth
        if not self.fiscal_code[6:8].isdigit():
            raise exceptions.ValidationError({"fiscal_code": msg})

        # month of birth
        if self.fiscal_code[8:9] not in (
            "A",
            "B",
            "C",
            "D",
            "E",
            "H",
            "L",
            "M",
            "P",
            "R",
            "S",
            "T",
        ):
            raise exceptions.ValidationError({"fiscal_code": msg})

        # date of birth
        if not self.fiscal_code[9:11].isdigit():
            raise exceptions.ValidationError({"fiscal_code": msg})

        # city code
        if not self.fiscal_code[11:15]:
            pass

        if not self.fiscal_code[15:16].isalpha():
            raise exceptions.ValidationError({"fiscal_code": msg})

    def is_eu(self):
        if self.country in EU_COUNTRIES:
            return True
        return False

    def is_italian(self):
        if self.country == "IT":
            return True
        return False
