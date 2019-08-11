from django.contrib.admin.sites import AdminSite
from pytest import mark
from tickets.admin import TicketAdmin, UserAnswersInline
from tickets.models import Ticket, UserAnswer


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


@mark.django_db
def test_cannot_manually_add_answers_to_a_ticket_in_the_admin(user_answer_factory):
    admin_site = AdminSite()

    has_permission = UserAnswersInline(
        parent_model=UserAnswer, admin_site=admin_site
    ).has_add_permission(user_answer_factory())

    assert not has_permission
