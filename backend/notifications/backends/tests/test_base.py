import pytest
from notifications.backends.base import EmailBackend


def test_base_backend():
    base = EmailBackend()
    with pytest.raises(NotImplementedError):
        base.send_email(
            template="template",
            subject="subject",
            from_="from",
            to="to",
            variables={"key": "value"},
            reply_to=["reply"],
        )
