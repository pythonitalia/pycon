import random

from pytest import mark

from tests.voting.factories.vote_range import VoteRangeFactory
from voting.models import Vote


def _submit_vote(client, submission, user, **kwargs):
    range = VoteRangeFactory()

    defaults = {
        'value': random.uniform(range.first, range.last),
        'range': range.id,
        'submission': submission.id,
        'user': user.id
    }

    variables = {**defaults, **kwargs}

    return client.query(
        """
        mutation($submission: ID!, $user: ID!, $value: Float!) {
            sendVote(input: {
                submission: $submission,
                user: $user,
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
        }
        """,
        variables=variables,
    ), variables


@mark.django_db
def test_submit_vote(graphql_client, user, conference_factory,
                     submission_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        active_voting=True,
    )

    submission = submission_factory(
        conference=conference,
        id=1
    )

    resp, variables = _submit_vote(
        graphql_client,
        submission,
        user,
        value=10
    )

    assert resp['data']['sendVote']['vote'] is not None, resp
    assert resp['data']['sendVote']['errors'] == []

    vote = Vote.objects.get(id=resp['data']['sendVote']['vote']['id'])
    assert vote.value == variables['value']
    assert vote.submission.id == variables['submission']
    assert vote.user.id == variables['user']


def test_reject_vote_when_voting_is_not_open(graphql_client, user,
                                             conference_factory,
                                             submission_factory):
    graphql_client.force_login(user)

    conference = conference_factory()

    submission = submission_factory(
        conference=conference,
    )

    resp, variables = _submit_vote(
        graphql_client,
        submission,
        user
    )

    assert resp['data']['sendVote']['errors']
    assert (
        resp['data']['sendVote']['errors'][0]['messages']
        ==
        ['The voting session is not open!']
    )
    assert resp['data']['sendVote']['errors'][0]['field'] == '__all__'


def test_user_can_votes_differents_submissons(graphql_client, user,
                                              conference_factory,
                                              submission_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        active_voting=True,
    )

    submission1 = submission_factory(
        conference=conference,
        id=1
    )
    resp1, variables1 = _submit_vote(
        graphql_client,
        submission1,
        user
    )
    assert resp1['data']['sendVote']['vote'] is not None, resp1
    assert resp1['data']['sendVote']['errors'] == []

    vote1 = Vote.objects.get(user=user, submission=submission1)
    assert vote1.value == variables1['value']

    submission2 = submission_factory(
        conference=conference,
    )

    resp2, variables2 = _submit_vote(
        graphql_client,
        submission2,
        user
    )
    assert resp2['data']['sendVote']['vote'] is not None, resp1
    assert resp2['data']['sendVote']['errors'] == []

    vote2 = Vote.objects.get(user=user, submission=submission2)
    assert vote2.value == variables2['value']

    assert Vote.objects.all().__len__() == 2


def test_updating_vote_when_user_votes_the_same_submission(graphql_client,
                                                           user,
                                                           conference_factory,
                                                           submission_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        active_voting=True,
    )

    submission = submission_factory(
        conference=conference,
        id=1
    )
    resp, variables = _submit_vote(
        graphql_client,
        submission,
        user
    )
    assert resp['data']['sendVote']['vote'] is not None, resp
    assert resp['data']['sendVote']['errors'] == []

    vote1 = Vote.objects.get(user=user, submission=submission)
    assert vote1.value == variables['value']

    resp, variables = _submit_vote(
        graphql_client,
        submission,
        user,
    )
    assert resp['data']['sendVote']['vote'] is not None, resp
    assert resp['data']['sendVote']['errors'] == []

    vote1 = Vote.objects.get(user=user, submission=submission)
    assert vote1.value == variables['value']
