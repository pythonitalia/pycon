import pytest
from django.test.utils import override_settings

from integrations.mailchimp import subscribe


@override_settings(MAILCHIMP_SECRET_KEY="")
def test_mailchimp_not_configure():
    with pytest.raises(ValueError, match="Mailchimp integration is not configured"):
        subscribe("me@pycon.it")


@pytest.mark.xfail(reason="TODO")
def test_call_mailchimp():
    assert False
