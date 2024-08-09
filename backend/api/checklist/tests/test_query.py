from checklist.tests.factories import ChecklistItemFactory
import pytest

pytestmark = pytest.mark.django_db


def test_fetch_checklist_items(graphql_client):
    item_1 = ChecklistItemFactory(text="Abbracciare Ernesto", order=2)
    item_2 = ChecklistItemFactory(text="Abbracciare Patrick", order=1)
    item_3 = ChecklistItemFactory(
        text="Assicurarsi ci sia abbastanza sushi in sala", order=0
    )

    response = graphql_client.query(
        """{
        checklist {
            id
            text
        }
    }"""
    )

    assert not response.get("errors")
    assert len(response["data"]["checklist"]) == 3
    assert response["data"]["checklist"] == [
        {
            "id": str(item_3.id),
            "text": str(item_3.text),
        },
        {
            "id": str(item_2.id),
            "text": str(item_2.text),
        },
        {
            "id": str(item_1.id),
            "text": str(item_1.text),
        },
    ]


def test_fetch_with_empty_checklist_items(graphql_client):
    response = graphql_client.query(
        """{
        checklist {
            id
            text
        }
    }"""
    )

    assert not response.get("errors")
    assert len(response["data"]["checklist"]) == 0
    assert response["data"]["checklist"] == []
