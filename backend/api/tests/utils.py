import json


class GraphQLClient:
    def __init__(self, client):
        self._client = client

    def query(self, query, op_name=None, variables=None, headers=None):
        """
        Args:
            query (string) - GraphQL query to run
            op_name (string) - If the query is a mutation or named query, you
                               must supply the op_name. For annon queries
                               ("{ ... }"), should be None (default).
            variables (dict) - If provided, the variables in GraphQL will be
                               set to this value
        Returns:
            dict, response from graphql endpoint.
                  The response has the "data" key.
                  It will have the "error" key if any error happened.
        """
        body = {"query": query}
        if op_name:
            body["operation_name"] = op_name
        if variables:
            body["variables"] = variables

        headers = headers or {}

        resp = self._client.post(
            "/graphql", json.dumps(body), content_type="application/json", **headers
        )

        return json.loads(resp.content.decode())

    def force_login(self, user):
        self._client.force_login(user)
