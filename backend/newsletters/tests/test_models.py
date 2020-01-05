import pytest


@pytest.mark.django_db
def test_set_recipients(subscription_factory, email_factory):

    sub1 = subscription_factory()
    sub2 = subscription_factory()

    email = email_factory(recipients=[])
    email.set_recipients()

    assert email.recipients == [sub1.email, sub2.email]


@pytest.mark.django_db
def test_send_newsletter(subscription_factory, email_factory):
    subscription_factory.create_batch(5)
    email = email_factory()
    resp = email.send_email()
    assert resp == 1
