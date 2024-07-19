from graphql import GraphQLError
import time
import time_machine
from unittest.mock import Mock
from api.context import Info
import pytest
from api.extensions import RateLimit
from django.test import override_settings
from django.core.cache import cache


def test_rate_limit_with_no_rate():
    rate_limit = RateLimit(rate=None)
    assert rate_limit.allow_request(None) is None


@pytest.mark.parametrize(
    "value,expected_output",
    [
        (None, (None, None)),
        ("10/m", (10, 60)),
        ("10/s", (10, 1)),
        ("10/h", (10, 3600)),
        ("10/d", (10, 86400)),
    ],
)
def test_parsing_rate_limit(value, expected_output):
    rate_limit = RateLimit(rate=None)
    assert rate_limit.parse_rate(value) == expected_output


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique",
        }
    }
)
def test_removes_obsolete_history_records():
    info = Info(context=Mock())
    info.field_name = "field_name"
    info.context.request = Mock()
    info.context.request.user = Mock()
    info.context.request.user.id = 1

    rate_limit = RateLimit(rate="10/m")

    with time_machine.travel("2021-01-01 00:01:00", tick=False):
        cache_key = rate_limit.get_cache_key(info)
        cache.set(cache_key, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 60)

        current_time = time.time()
        rate_limit.allow_request(info)

        assert cache.get(cache_key) == [current_time]


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique",
        }
    }
)
def test_blocks_too_many_requests():
    info = Info(context=Mock())
    info.field_name = "field_name"
    info.context.request = Mock()
    info.context.request.user = Mock()
    info.context.request.user.id = 1

    rate_limit = RateLimit(rate="10/m")

    with time_machine.travel("2021-01-01 00:01:00", tick=False), pytest.raises(
        GraphQLError
    ):
        current_time = time.time()

        cache_key = rate_limit.get_cache_key(info)
        cache.set(cache_key, [current_time] * 100, 60)

        rate_limit.allow_request(info)
