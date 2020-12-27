import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


class GraphQLClient:
    def __init__(self, client):
        self._client = client

    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        body = {"query": query}
        headers = headers or {}

        if variables:
            body["variables"] = variables

        resp = self._client.post(
            "/graphql", json.dumps(body), content_type="application/json", **headers
        )

        data = json.loads(resp.content.decode())
        return data

    def force_login(self, user):
        self._client.force_login(user)
