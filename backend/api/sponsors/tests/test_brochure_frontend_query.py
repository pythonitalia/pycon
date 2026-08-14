import datetime
from decimal import Decimal

import pytest

from conferences.tests.factories import ConferenceFactory
from i18n.strings import LazyI18nString
from sponsors import models
from sponsors.tests.factories import (
    SponsorBenefitFactory,
    SponsorLevelBenefitFactory,
    SponsorLevelFactory,
    SponsorSpecialOptionFactory,
)

pytestmark = pytest.mark.django_db


BROCHURE_QUERY = """\
query GetBrochureData($conferenceCode: String!) {
  conference(code: $conferenceCode) {
    id
    name
    start
    end
    introduction
    sponsorBenefits {
      name
      category
      description
    }
    sponsorLevels {
      name
      price
      slots
      benefits {
        name
        value
      }
    }
    sponsorSpecialOptions {
      name
      price
      description
    }
  }
}
"""


def test_brochure_frontend_query(graphql_client, django_assert_num_queries):
    start = datetime.datetime(2026, 5, 27, 9, 0, tzinfo=datetime.UTC)
    end = datetime.datetime(2026, 5, 30, 18, 0, tzinfo=datetime.UTC)
    conference = ConferenceFactory(
        name=LazyI18nString({"en": "PyCon Italia"}),
        introduction=LazyI18nString({"en": "Welcome to Florence"}),
        start=start,
        end=end,
    )

    levels = []
    benefits = []
    level_benefits = []
    for index in range(4):
        benefit = SponsorBenefitFactory(
            conference=conference,
            name=LazyI18nString({"en": f"Benefit {index}"}),
            category=models.SponsorBenefit.Category.CONTENT,
            description=LazyI18nString({"en": f"Description {index}"}),
            order=index,
        )
        level = SponsorLevelFactory(
            conference=conference,
            name=f"Level {index}",
            price=Decimal(f"{index + 1}000.00"),
            slots=index + 1,
            order=index,
        )
        level_benefit = SponsorLevelBenefitFactory(
            sponsor_level=level,
            benefit=benefit,
            value=LazyI18nString({"en": f"Value {index}"}),
        )
        benefits.append(benefit)
        levels.append(level)
        level_benefits.append(level_benefit)

    options = [
        SponsorSpecialOptionFactory(
            conference=conference,
            name=f"Option {index}",
            price=Decimal(f"{index + 1}00.00"),
            description=f"Option description {index}",
            order=index,
        )
        for index in range(2)
    ]

    with django_assert_num_queries(5):
        response = graphql_client.query(
            BROCHURE_QUERY,
            variables={"conferenceCode": conference.code},
        )

    assert response == {
        "data": {
            "conference": {
                "id": str(conference.id),
                "name": "PyCon Italia",
                "start": start.isoformat(),
                "end": end.isoformat(),
                "introduction": "Welcome to Florence",
                "sponsorBenefits": [
                    {
                        "name": str(benefit.name),
                        "category": benefit.category,
                        "description": str(benefit.description),
                    }
                    for benefit in benefits
                ],
                "sponsorLevels": [
                    {
                        "name": level.name,
                        "price": str(level.price),
                        "slots": level.slots,
                        "benefits": [
                            {
                                "name": str(level_benefit.benefit.name),
                                "value": str(level_benefit.value),
                            }
                        ],
                    }
                    for level, level_benefit in zip(levels, level_benefits, strict=True)
                ],
                "sponsorSpecialOptions": [
                    {
                        "name": option.name,
                        "price": str(option.price),
                        "description": option.description,
                    }
                    for option in options
                ],
            }
        }
    }
