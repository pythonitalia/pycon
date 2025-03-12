from countries import countries
from model_utils.models import TimeStampedModel
from django.db import models
from django.conf import settings
from billing.managers import BillingAddressQuerySet
from django.utils.translation import gettext_lazy as _


class BillingAddress(TimeStampedModel):
    conference_reference = "organizer__conferences"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="billing_addresses",
        verbose_name=_("user"),
    )
    organizer = models.ForeignKey(
        "organizers.Organizer",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("organizer"),
    )
    is_business = models.BooleanField(_("is business"))
    company_name = models.TextField(_("company name"), blank=True)
    user_name = models.TextField(_("user name"))
    zip_code = models.TextField(_("zip code"))
    city = models.TextField(_("city"))
    address = models.TextField(_("address"))
    country = models.CharField(
        _("country"),
        choices=[(country.code, country.name) for country in countries],
        max_length=10,
    )
    vat_id = models.TextField(_("vat id"), blank=True)
    fiscal_code = models.TextField(_("fiscal code"), blank=True)
    sdi = models.TextField(_("sdi"), blank=True)
    pec = models.EmailField(_("pec"), blank=True)

    objects = BillingAddressQuerySet().as_manager()
