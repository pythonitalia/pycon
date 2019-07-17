import math
import random

from pytest import mark

from voting.models import Vote
from voting.types import VoteValues


def _submit_vote(client, submission, **kwargs):
    vote_index = math.floor(random.uniform(Vote.VALUES.not_interested, Vote.VALUES.must_see))
    defaults = {
        "value": VoteValues.get(vote_index).name,
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
                    vote {
                        id
                        value
                    }
                    errors {
                        messages
                        field
                    }
                }
            }""",
            variables=variables,
        ),
        {
            **variables,
            'vote_index': vote_index
        },
    )


@mark.django_db
def test_submit_vote(graphql_client, user, conference_factory, submission_factory):
    graphql_client.force_login(user)

    conference = conference_factory(active_voting=True)

    submission = submission_factory(conference=conference)

    resp, variables = _submit_vote(graphql_client, submission, value=VoteValues.get(0).name)

    assert resp["data"]["sendVote"]["vote"] is not None, resp
    assert resp["data"]["sendVote"]["errors"] == []

    vote = Vote.objects.get(id=resp["data"]["sendVote"]["vote"]["id"])
    assert vote.value == 0
    assert vote.submission.id == variables["submission"]
    assert vote.user == user


def test_reject_vote_when_voting_is_not_open(
    graphql_client, user, conference_factory, submission_factory
):
    graphql_client.force_login(user)

    conference = conference_factory()

    submission = submission_factory(conference=conference)

    resp, variables = _submit_vote(graphql_client, submission)

    assert resp["data"]["sendVote"]["errors"]
    assert resp["data"]["sendVote"]["errors"][0]["messages"] == [
        "The voting session is not open!"
    ]
    assert resp["data"]["sendVote"]["errors"][0]["field"] == "__all__"


def test_user_can_vote_different_submissions(
    graphql_client, user, conference_factory, submission_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(active_voting=True)

    submission1 = submission_factory(conference=conference, id=1)
    resp1, variables1 = _submit_vote(graphql_client, submission1)
    assert resp1["data"]["sendVote"]["vote"] is not None, resp1
    assert resp1["data"]["sendVote"]["errors"] == []

    vote1 = Vote.objects.get(user=user, submission=submission1)
    assert vote1.value == variables1["vote_index"]

    submission2 = submission_factory(conference=conference)

    resp2, variables2 = _submit_vote(graphql_client, submission2)
    assert resp2["data"]["sendVote"]["vote"] is not None, resp1
    assert resp2["data"]["sendVote"]["errors"] == []

    vote2 = Vote.objects.get(user=user, submission=submission2)
    assert vote2.value == variables2["vote_index"]

    assert Vote.objects.all().__len__() == 2


def test_updating_vote_when_user_votes_the_same_submission(
    graphql_client, user, conference_factory, submission_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(active_voting=True)

    submission = submission_factory(conference=conference, id=1)
    resp, variables = _submit_vote(graphql_client, submission)

    assert resp["data"]["sendVote"]["vote"] is not None, resp
    assert resp["data"]["sendVote"]["errors"] == []

    vote1 = Vote.objects.get(user=user, submission=submission)
    assert vote1.value == variables["vote_index"]

    resp, variables = _submit_vote(graphql_client, submission)

    assert resp["data"]["sendVote"]["vote"] is not None, resp
    assert resp["data"]["sendVote"]["errors"] == []

    vote1 = Vote.objects.get(user=user, submission=submission)

    assert vote1.value == variables["vote_index"]
