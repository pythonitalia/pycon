from strawberry.tools import create_type

import strawberry


@strawberry.type
def cms_empty_query():
    return "cms"


Query = create_type("Query", fields=[cms_empty_query])
schema = strawberry.federation.Schema(query=Query)
