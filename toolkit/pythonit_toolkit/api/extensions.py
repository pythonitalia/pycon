from sentry_sdk import add_breadcrumb
from strawberry.extensions import Extension


class SentryExtension(Extension):
    def on_request_start(self):
        add_breadcrumb(
            category="graphql",
            message=f"""
{self.execution_context.operation_name or 'No operation name'}
{self.execution_context.query}
            """.strip(),
            level="info",
        )
