from pytest import mark

from participants.tests.factories import ParticipantFactory
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory


PARTICIPANT_PUBLIC_PROFILE_QUERY = """
    query ParticipantPublicProfile(
        $id: ID!
        $conference: String!
        $language: String!
    ) {
        participant(id: $id, conference: $conference) {
            id
            fullname
            publicProfile
            bio
            website
            photo
            twitterHandle
            instagramHandle
            linkedinUrl
            facebookUrl
            mastodonHandle
            proposals {
                id
                title(language: $language)
                type {
                    id
                    name
                }
                audienceLevel {
                    id
                    name
                }
                duration {
                    id
                    duration
                }
                scheduleItems {
                    ...ScheduleItemFragment
                }
            }
        }
    }

    fragment ScheduleItemFragment on ScheduleItem {
        id
        title
        slug
        type
        duration
        hasLimitedCapacity
        userHasSpot
        hasSpacesLeft
        spacesLeft
        linkTo
        audienceLevel {
            id
            name
        }
        language {
            id
            name
            code
        }
        submission {
            ...SubmissionFragment
        }
        keynote {
            ...KeynoteFragment
        }
        speakers {
            id
            fullname
            participant {
                id
                photo
            }
        }
        rooms {
            id
            name
            type
        }
    }

    fragment SubmissionFragment on Submission {
        id
        title(language: $language)
        duration {
            id
            duration
        }
        audienceLevel {
            id
            name
        }
        speaker {
            id
            fullName
        }
        type {
            id
            name
        }
        tags {
            id
            name
        }
    }

    fragment KeynoteFragment on Keynote {
        id
        title(language: "en")
        slug(language: "en")
        speakers {
            id
            fullName
        }
    }
"""


MY_EDIT_PROFILE_QUERY = """
    query MyEditProfile($conference: String!) {
        me {
            id
            hashid
            email
            name
            fullName
            gender
            openToRecruiting
            openToNewsletter
            dateBirth
            country
            participant(conference: $conference) {
                id
                publicProfile
                photo
                photoId
                bio
                website
                speakerLevel
                previousTalkVideo
                twitterHandle
                instagramHandle
                linkedinUrl
                facebookUrl
                mastodonHandle
            }
        }
    }
"""


@mark.parametrize("proposal_count", [1, 4])
@mark.django_db
def test_frontend_public_participant_query(
    graphql_client, django_assert_num_queries, proposal_count
):
    participant = ParticipantFactory(public_profile=True)
    proposals = SubmissionFactory.create_batch(
        proposal_count,
        conference=participant.conference,
        speaker=participant.user,
        status=Submission.STATUS.accepted,
    )

    expected_queries = 3 + proposal_count
    with django_assert_num_queries(expected_queries):
        response = graphql_client.query(
            PARTICIPANT_PUBLIC_PROFILE_QUERY,
            variables={
                "id": participant.hashid,
                "conference": participant.conference.code,
                "language": "en",
            },
        )

    assert "errors" not in response
    participant_data = response["data"]["participant"]
    assert participant_data["id"] == participant.hashid
    assert {proposal["id"] for proposal in participant_data["proposals"]} == {
        proposal.hashid for proposal in proposals
    }


@mark.django_db
def test_frontend_edit_profile_participant_query(
    graphql_client, django_assert_num_queries
):
    participant = ParticipantFactory(public_profile=True)
    graphql_client.force_login(participant.user)

    with django_assert_num_queries(4):
        response = graphql_client.query(
            MY_EDIT_PROFILE_QUERY,
            variables={"conference": participant.conference.code},
        )

    assert "errors" not in response
    participant_data = response["data"]["me"]["participant"]
    assert participant_data["id"] == participant.hashid
    assert participant_data["speakerLevel"] == participant.speaker_level
