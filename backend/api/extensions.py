import time
from typing import Any, Callable
import strawberry
from graphql import GraphQLError
from strawberry.extensions import FieldExtension
from django.core.cache import cache


# TODO Reimplement with a schema extension
class RateLimit(FieldExtension):
    def __init__(self, rate: str | None):
        super().__init__()
        self.rate = rate
        self.reqs, self.period = self.parse_rate(rate)

    def resolve(
        self, next: Callable[..., Any], source: Any, info: strawberry.Info, **kwargs
    ):
        self.allow_request(info)
        result = next(source, info, **kwargs)
        return result

    def allow_request(self, info: strawberry.Info):
        if not self.rate:
            return

        cache_key = self.get_cache_key(info)
        now = time.time()
        history = cache.get(cache_key, [])

        while history and history[-1] < now - self.period:
            history.pop()

        if len(history) >= self.reqs:
            raise GraphQLError("Rate limit exceeded.")

        history.insert(0, now)
        cache.set(cache_key, history, self.period)

    def get_cache_key(self, info: strawberry.Info) -> str:
        return f"ratelimit:{info.context.request.user.id}:{info.field_name}"

    def parse_rate(self, rate: str) -> tuple[int, int]:
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split("/")
        num_requests = int(num)
        duration = {"s": 1, "m": 60, "h": 3600, "d": 86400}[period[0]]
        return (num_requests, duration)
