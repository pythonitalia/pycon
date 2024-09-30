from datetime import datetime

from conferences.tests.factories import ConferenceFactory
from sponsors.tests.factories import (
    SponsorLevelFactory,
    SponsorBenefitFactory,
    SponsorSpecialOptionFactory,
    SponsorLevelBenefitFactory,
)
from pycon.constants import UTC
from pytest import mark


@mark.django_db
def test_sponsor_information(graphql_client):
    conference = ConferenceFactory(
        start=datetime(2020, 4, 2, tzinfo=UTC),
        end=datetime(2020, 4, 2, tzinfo=UTC),
    )

    sponsor_level = SponsorLevelFactory(conference=conference)
    sponsor_benefit = SponsorBenefitFactory(conference=conference)
    sponsor_special_option = SponsorSpecialOptionFactory(conference=conference)
    sponsor_level_benefit = SponsorLevelBenefitFactory(
        sponsor_level=sponsor_level, benefit=sponsor_benefit
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                sponsorLevels {
                    name
                    slots
                    benefits {
                        name
                        category
                        description
                        value
                    }
                }
                sponsorBenefits {
                    name
                    category
                    description
                }
                sponsorSpecialOptions {
                    name
                    description
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp

    assert resp["data"]["conference"] == {
        "sponsorLevels": [
            {
                "name": sponsor_level.name,
                "slots": sponsor_level.slots,
                "benefits": [
                    {
                        "name": sponsor_benefit.name,
                        "category": sponsor_benefit.category,
                        "description": sponsor_benefit.description,
                        "value": sponsor_level_benefit.value,
                    }
                ],
            }
        ],
        "sponsorBenefits": [
            {
                "name": sponsor_benefit.name,
                "category": sponsor_benefit.category,
                "description": sponsor_benefit.description,
            }
        ],
        "sponsorSpecialOptions": [
            {
                "name": sponsor_special_option.name,
                "description": sponsor_special_option.description,
            }
        ],
    }
