from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.constants import GENDERS

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=100, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=300, blank=True)
    name = models.CharField(_("name"), max_length=300, blank=True)

    gender = models.CharField(_("gender"), choices=GENDERS, max_length=10, blank=True)
    country = models.CharField(_("country"), max_length=50, blank=True)
    date_birth = models.DateField(_("date of birth"), null=True)
    open_to_recruiting = models.BooleanField(_("open to recruiting"), default=False)
    open_to_newsletter = models.BooleanField(_("open to newsletter"), default=False)

    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("is staff"), default=False)

    jwt_auth_id = models.IntegerField(_("jwt auth id"), default=1)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.name or 'No name set'})"

    def get_short_name(self):
        return self.email

    @property
    def fullname(self):
        return self.full_name

    @property
    def display_name(self):
        return self.full_name or self.name
