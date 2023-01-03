from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from i18n.fields import I18nCharField, I18nTextField


class BedLayout(models.Model):
    name = I18nCharField(_("name"), max_length=200)

    def __str__(self) -> str:
        if isinstance(self.name, str):
            return self.name

        return self.name.localize("en")


class HotelRoom(models.Model):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="hotel_rooms",
    )

    name = I18nCharField(_("name"), max_length=200)
    description = I18nTextField(_("description"), blank=True)

    total_capacity = models.PositiveIntegerField(_("total capacity"))
    price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)

    available_bed_layouts = models.ManyToManyField(
        BedLayout,
    )

    @cached_property
    def capacity_left(self):
        return (
            self.total_capacity
            - HotelRoomReservation.objects.filter(room_id=self.pk).count()
        )

    @property
    def is_sold_out(self):
        # TODO: run the check in the query instead of python
        return (
            HotelRoomReservation.objects.filter(room_id=self.pk).count()
            >= self.total_capacity
        )

    def __str__(self):
        return f"{self.name} ({self.conference.code})"

    class Meta:
        verbose_name = _("hotel room")
        verbose_name_plural = _("hotel rooms")


class HotelRoomReservation(models.Model):
    order_code = models.CharField(_("pretix's order code"), max_length=200)

    room = models.ForeignKey(
        HotelRoom,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("room"),
    )

    user_id = models.IntegerField(verbose_name=_("user"))

    checkin = models.DateField(_("checkin"))
    checkout = models.DateField(_("checkout"))
    bed_layout = models.ForeignKey(
        BedLayout,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.order_code} ({self.checkin} -> {self.checkout})"

    class Meta:
        verbose_name = _("hotel room reservation")
        verbose_name_plural = _("hotel room reservations")
