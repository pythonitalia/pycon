from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=100, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=300, blank=True)
    name = models.CharField(_("name"), max_length=300, blank=True)

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    GENDERS = Choices(("male", _("Male")), ("female", _("Female")))
    gender = models.CharField(_("gender"), choices=GENDERS, max_length=10, blank=True)
    date_birth = models.DateField(_("date of birth"), null=True)

    business_name = models.CharField(_("business name"), max_length=150, blank=True)
    fiscal_code = models.CharField(_("fiscal code"), max_length=16, blank=True)
    vat_number = models.CharField(_("VAT number"), max_length=22, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=20, blank=True)

    # electronic invoicing ita
    recipient_code = models.CharField(_("recipient code"), max_length=7, blank=True)
    pec_address = models.EmailField(_("PEC"), blank=True)

    address = models.TextField(_("address"), blank=True)
    country = models.ForeignKey(
        "countries.Country",
        verbose_name=_("country"),
        on_delete=models.PROTECT,
        null=True,
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
