import math
import random

from api.voting.types import VoteValues
from pytest import mark
from voting.models import Vote


def _submit_vote(client, submission, **kwargs):
    value_index = kwargs.get(
        "value_index",
        math.floor(random.uniform(Vote.VALUES.not_interested, Vote.VALUES.must_see)),
    )

    defaults = {
        "value": VoteValues.from_int(value_index).name,
        "submission": submission.id,
    }

    variables = {**defaults, **kwargs}

    return (
        client.query(
            """mutation($submission: ID!, $value: VoteValues!) {
                sendVote(input: {
                    submission: $submission,
                    value: $value
                }) {
                    __typename

                    ... on VoteType {
                        id
                        value
                    }

                    ... on SendVoteErrors {
                        validationSubmission: submission
                        validationValue: value
                        nonFieldErrors
                    }
                }
            }""",
            variables=variables,
        ),
        {**variables, "value_index": value_index},
    )


@mark.django_db
@mark.parametrize("score_index", [0, 1, 2])
def test_submit_vote(
    graphql_client, user, conference_factory, submission_factory, score_index
):
    graphql_client.force_login(user)

    conference = conference_factory(active_voting=True)

    submission = submission_factory(conference=conference)

    resp, variables = _submit_vote(graphql_client, submission, value_index=score_index)

    assert resp["data"]["sendVote"]["__typename"] == "VoteType"

    vote = Vote.objects.get(id=resp["data"]["sendVote"]["id"])

    assert vote.value == score_index
    assert vote.submission.id == variables["submission"]
    assert vote.user == user


def test_reject_vote_when_voting_is_not_open(
    graphql_client, user, conference_factory, submission_factory
):
    graphql_client.force_login(user)

    conference = conference_factory()

    submission = submission_factory(conference=conference)

    resp, variables = _submit_vote(graphql_client, submission)

    assert resp["data"]["sendVote"]["__typename"] == "SendVoteErrors"
    assert resp["data"]["sendVote"]["nonFieldErrors"] == [
        "The voting session is not open!"
    ]


def test_user_can_vote_different_submissions(
    graphql_client, user, conference_factory, submission_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(active_voting=True)

    submission1 = submission_factory(conference=conference, id=1)
    resp1, variables1 = _submit_vote(graphql_client, submission1)

    assert resp1["data"]["sendVote"]["__typename"] == "VoteType"

    vote1 = Vote.objects.get(user=user, submission=submission1)
    assert vote1.value == variables1["value_index"]

    submission2 = submission_factory(conference=conference)

    resp2, variables2 = _submit_vote(graphql_client, submission2)

    assert resp2["data"]["sendVote"]["__typename"] == "VoteType"

    vote2 = Vote.objects.get(user=user, submission=submission2)
    assert vote2.value == variables2["value_index"]

    assert Vote.objects.all().count() == 2


def test_updating_vote_when_user_votes_the_same_submission(
    graphql_client, user, conference_factory, submission_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(active_voting=True)

    submission = submission_factory(conference=conference, id=1)
    resp, variables = _submit_vote(graphql_client, submission, value_index=1)

    assert resp["data"]["sendVote"]["__typename"] == "VoteType"

    vote1 = Vote.objects.get(user=user, submission=submission)
    assert vote1.value == variables["value_index"]

    resp, variables = _submit_vote(graphql_client, submission, value_index=3)

    assert resp["data"]["sendVote"]["__typename"] == "VoteType"

    vote1 = Vote.objects.get(user=user, submission=submission)

    assert vote1.value == variables["value_index"]
