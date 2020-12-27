import random

from conferences.tests.factories import ConferenceFactory
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory
from voting.tests.factories import VoteFactory
from voting.tests.fixtures import get_random_vote


def fakeit():
    conference = ConferenceFactory()

    USERS_NUMBER = random.randint(10, 50)
    SUBMISSION_NUMBER = int(USERS_NUMBER * 0.4)
    users = UserFactory.create_batch(USERS_NUMBER)

    submissions = SubmissionFactory.create_batch(
        SUBMISSION_NUMBER, conference=conference
    )

    counts_votes = {}
    for submission in submissions:
        counts_votes[submission.pk] = 0
    for user in users:
        i_vote_only = random.randint(0, len(submissions))
        submission_to_vote = random.sample(submissions, k=i_vote_only)
        for submission in submission_to_vote:
            # make more realistic: skip some voting...
            if bool(random.getrandbits(1)):
                continue

            value = get_random_vote()
            VoteFactory(user=user, value=value, submission=submission)
            counts_votes[submission.pk] += value

    return conference, counts_votes
