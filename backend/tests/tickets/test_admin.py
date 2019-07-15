from pytest import mark

from django.contrib.admin.sites import AdminSite

from tickets.admin import TicketAdmin
from tickets.models import Ticket


@mark.django_db
def test_ticket_conference_display_label(ticket_factory):
    admin_site = AdminSite()
    model_admin = TicketAdmin(Ticket, admin_site)
    ticket = ticket_factory()

    assert model_admin.ticket_fare_name(ticket) == ticket.ticket_fare.name


@mark.django_db
def test_ticket_assigned_user_display_label(ticket_factory):
    admin_site = AdminSite()
    model_admin = TicketAdmin(Ticket, admin_site)
    ticket = ticket_factory()

    assert model_admin.user_email(ticket) == ticket.user.email
