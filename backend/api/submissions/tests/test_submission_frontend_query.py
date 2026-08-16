from pytest import mark

from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DurationFactory,
    TopicFactory,
)
from files_upload.tests.factories import ProposalMaterialFileFactory
from i18n.strings import LazyI18nString
from languages.models import Language
from submissions import models
from submissions.tests.factories import (
    ProposalMaterialFactory,
    SubmissionFactory,
    SubmissionTypeFactory,
)

SUBMISSION_QUERY = """
    query GetSubmission($id: ID!) {
      submission(id: $id) {
        id
        status
        title(language: "en")
        abstract(language: "en")
        elevatorPitch(language: "en")
        shortSocialSummary
        doNotRecord
        multilingualTitle {
          it
          en
        }
        multilingualAbstract {
          it
          en
        }
        multilingualElevatorPitch {
          it
          en
        }
        type {
          id
          name
        }
        notes
        canEdit
        speakerLevel
        previousTalkVideo
        topic {
          id
          name
        }
        duration {
          id
          name
        }
        audienceLevel {
          id
          name
        }
        languages {
          id
          code
          name
        }
        tags {
          id
          name
        }
        materials {
          id
          name
          url
          fileId
          fileUrl
          fileMimeType
        }
      }
    }
"""


@mark.django_db
def test_submission_frontend_query(
    graphql_client,
    user,
    django_assert_num_queries,
):
    conference = ConferenceFactory(active_cfp=True)
    submission_type = SubmissionTypeFactory(name="Talk")
    topic = TopicFactory(name="GraphQL")
    duration = DurationFactory(
        conference=conference,
        duration=45,
        name="45 minutes",
    )
    audience_level = AudienceLevelFactory(name="Intermediate")
    submission = SubmissionFactory(
        abstract=LazyI18nString({"en": "English abstract", "it": "Abstract italiano"}),
        audience_level=audience_level,
        conference=conference,
        do_not_record=True,
        duration=duration,
        elevator_pitch=LazyI18nString({"en": "English pitch", "it": "Pitch italiano"}),
        languages=["en"],
        notes="Private notes",
        previous_talk_video="https://example.com/talk",
        short_social_summary="Short summary",
        speaker=user,
        speaker_level=models.Submission.SPEAKER_LEVELS.intermediate,
        tags=["graphql"],
        title=LazyI18nString({"en": "English title", "it": "Titolo italiano"}),
        topic=topic,
        type=submission_type,
    )
    link_material = ProposalMaterialFactory(
        name="Slides",
        proposal=submission,
        url="https://example.com/slides",
    )
    material_file = ProposalMaterialFileFactory(
        mime_type="application/pdf",
        uploaded_by=user,
    )
    file_material = ProposalMaterialFactory(
        file=material_file,
        name="Handout",
        proposal=submission,
    )
    english = Language.objects.get(code="en")
    tag = submission.tags.get()
    graphql_client.force_login(user)

    with django_assert_num_queries(10):
        response = graphql_client.query(
            SUBMISSION_QUERY,
            variables={"id": submission.hashid},
        )

    assert "errors" not in response
    assert response["data"]["submission"] == {
        "id": submission.hashid,
        "status": "proposed",
        "title": "English title",
        "abstract": "English abstract",
        "elevatorPitch": "English pitch",
        "shortSocialSummary": "Short summary",
        "doNotRecord": True,
        "multilingualTitle": {"it": "Titolo italiano", "en": "English title"},
        "multilingualAbstract": {
            "it": "Abstract italiano",
            "en": "English abstract",
        },
        "multilingualElevatorPitch": {
            "it": "Pitch italiano",
            "en": "English pitch",
        },
        "type": {"id": str(submission_type.id), "name": "Talk"},
        "notes": "Private notes",
        "canEdit": True,
        "speakerLevel": "intermediate",
        "previousTalkVideo": "https://example.com/talk",
        "topic": {"id": str(topic.id), "name": "GraphQL"},
        "duration": {"id": str(duration.id), "name": "45 minutes"},
        "audienceLevel": {
            "id": str(audience_level.id),
            "name": "Intermediate",
        },
        "languages": [{"id": str(english.id), "code": "en", "name": english.name}],
        "tags": [{"id": str(tag.id), "name": "graphql"}],
        "materials": [
            {
                "id": str(link_material.id),
                "name": "Slides",
                "url": "https://example.com/slides",
                "fileId": None,
                "fileUrl": None,
                "fileMimeType": None,
            },
            {
                "id": str(file_material.id),
                "name": "Handout",
                "url": None,
                "fileId": str(material_file.id),
                "fileUrl": material_file.file.url,
                "fileMimeType": "application/pdf",
            },
        ],
    }
