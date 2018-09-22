from .settings import LIMIT_MAX_VALUE, LIMIT_MIN_VALUE


def get_pagination(queryset, offset, limit, graphql_type):
    limit = max(min(limit, LIMIT_MAX_VALUE), LIMIT_MIN_VALUE)
    offset = max(0, offset)

    return graphql_type(
        total_count=queryset.count(),
        objects=queryset[offset:offset + limit],
    )
