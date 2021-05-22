from sentry_sdk import add_breadcrumb
from strawberry.extensions import Extension
from strawberry.types.execution import ExecutionContext


class SentryExtension(Extension):
    def on_request_start(self, execution_context: ExecutionContext):
        add_breadcrumb(
            category="graphql",
            message=f"""
{execution_context.operation_name or 'No operation name'}
{execution_context.query}
            """.strip(),
            level="info",
        )
