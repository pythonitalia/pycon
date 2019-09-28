from i18n.strings import LazyI18nString
from pytest import mark


@mark.django_db
def test_get_conference_faqs(conference_factory, faq_factory, graphql_client):
    conference = conference_factory()
    conference_b = conference_factory()

    faq_factory(
        conference=conference,
        question=LazyI18nString({"en": "Do you love this conference?"}),
        answer=LazyI18nString({"en": "Yes!"}),
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                faqs {
                    question
                    answer
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["faqs"] == [
        {"question": "Do you love this conference?", "answer": "Yes!"}
    ]

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                faqs {
                    question
                    answer
                }
            }
        }
        """,
        variables={"code": conference_b.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["faqs"] == []
