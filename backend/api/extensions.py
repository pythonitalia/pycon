import hashlib
import logfire
from functools import cached_property
from strawberry.extensions.tracing.utils import should_skip_tracing
from typing import Any, Callable, Generator, Iterator
from strawberry.extensions import LifecycleStep, SchemaExtension
import time
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


class LogfireExtension(SchemaExtension):
    def __init__(
        self,
        *,
        execution_context=None,
    ) -> None:
        self.strawberry_logfire = logfire.with_settings(
            custom_scope_suffix="strawberry", tags=["API"]
        )
        self.execution_context = execution_context

    @cached_property
    def _resource_name(self) -> str:
        if self.execution_context.query is None:
            return "query_missing"

        query_hash = self.hash_query(self.execution_context.query)

        if self.execution_context.operation_name:
            return f"{self.execution_context.operation_name}:{query_hash}"

        return query_hash

    def create_span(
        self,
        lifecycle_step: LifecycleStep,
        name: str,
        **kwargs: Any,
    ):
        """Create a span with the given name and kwargs.

        You can  override this if you want to add more tags to the span.

        Example:

        ```python
        class CustomExtension(DatadogTracingExtension):
            def create_span(self, lifecycle_step, name, **kwargs):
                span = super().create_span(lifecycle_step, name, **kwargs)
                if lifecycle_step == LifeCycleStep.OPERATION:
                    span.set_attribute("graphql.query", self.execution_context.query)
                return span
        ```
        """
        return self.strawberry_logfire.span(
            name, lifecycle_step=lifecycle_step.name, **kwargs
        )

    def hash_query(self, query: str) -> str:
        return hashlib.md5(query.encode("utf-8")).hexdigest()

    def on_operation(self) -> Iterator[None]:
        self._operation_name = self.execution_context.operation_name
        span_name = (
            f"{self._operation_name}" if self._operation_name else "Anonymous Query"
        )

        with self.create_span(
            LifecycleStep.OPERATION,
            span_name,
            resource=self._resource_name,
        ) as request_span:
            request_span.set_attribute("graphql.operation_name", self._operation_name)

            query = self.execution_context.query
            query = query.strip()
            operation_type = "query"

            if query.startswith("mutation"):
                operation_type = "mutation"
            elif query.startswith("subscription"):  # pragma: no cover
                operation_type = "subscription"

            request_span.set_attribute("graphql.operation_type", operation_type)

            yield

    def on_validate(self) -> Generator[None, None, None]:
        with self.create_span(
            lifecycle_step=LifecycleStep.VALIDATION,
            name="Validation",
        ):
            yield

    def on_parse(self) -> Generator[None, None, None]:
        with self.create_span(
            lifecycle_step=LifecycleStep.PARSE,
            name="Parsing",
        ):
            yield

    def resolve(
        self,
        _next: Callable,
        root: Any,
        info,
        *args: str,
        **kwargs: Any,
    ) -> Any:
        if should_skip_tracing(_next, info):
            return _next(root, info, *args, **kwargs)

        field_path = f"{info.parent_type}.{info.field_name}"

        with self.create_span(
            lifecycle_step=LifecycleStep.RESOLVE,
            name=f"Resolving: {field_path}",
        ) as span:
            span.set_attribute("graphql.field_name", info.field_name)
            span.set_attribute("graphql.parent_type", info.parent_type.name)
            span.set_attribute("graphql.field_path", field_path)
            span.set_attribute("graphql.path", ".".join(map(str, info.path.as_list())))

            return _next(root, info, *args, **kwargs)
