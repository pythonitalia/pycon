from api.builder import create_query_type

from .me import me

Query = create_query_type("Query", [me])
