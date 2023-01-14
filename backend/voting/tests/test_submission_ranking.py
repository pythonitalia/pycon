# import pytest
# import respx
# from django.conf import settings

from voting.models import RankRequest, RankStat, Vote

# pytestmark = pytest.mark.django_db


# @pytest.fixture
# def mock_users():
#     with respx.mock as mock:
#         mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
#             json={
#                 "data": {
#                     "usersByIds": [
#                         {
#                             "id": 1,
#                             "gender": "male",
#                         },
#                         {
#                             "id": 2,
#                             "gender": "male",
#                         },
#                         {
#                             "id": 3,
#                             "gender": "female",
#                         },
#                         {
#                             "id": 4,
#                             "gender": "not_say",
#                         },
#                         {
#                             "id": 5,
#                             "gender": "other",
#                         },
#                     ]
#                 }
#             }
#         )

#         yield


# @pytest.fixture
# def _voting_fixture(
#     conference_factory,
#     user_factory,
#     submission_factory,
#     submission_tag_factory,
#     vote_factory,
# ):
#     conference = conference_factory(
#         submission_types=["Talk", "Workshop"],
#         audience_levels=("adult", "senior"),
#         languages=["en", "it"],
#     )
#     sushi = submission_tag_factory(name="Sushi")
#     pizza = submission_tag_factory(name="Pizza")
#     submissions = []
#     submissions.append(
#         submission_factory(
#             conference=conference,
#             tags=["sushi"],
#             speaker_id=1,
#             languages=["en"],
#             custom_submission_type="Talk",
#             custom_audience_level="senior",
#         )
#     )
#     submissions.append(
#         submission_factory(
#             conference=conference,
#             tags=["sushi"],
#             speaker_id=2,
#             languages=["en", "it"],
#             custom_submission_type="Workshop",
#             custom_audience_level="senior",
#         )
#     )
#     submissions.append(
#         submission_factory(
#             conference=conference,
#             tags=["sushi"],
#             speaker_id=3,
#             languages=["en"],
#             custom_submission_type="Workshop",
#             custom_audience_level="adult",
#         )
#     )
#     submissions.append(
#         submission_factory(
#             conference=conference,
#             tags=["sushi"],
#             speaker_id=4,
#             languages=["it"],
#             custom_submission_type="Talk",
#             custom_audience_level="senior",
#         )
#     )
#     submissions.append(
#         submission_factory(
#             conference=conference,
#             tags=["pizza"],
#             speaker_id=1,
#             languages=["en", "it"],
#             custom_submission_type="Workshop",
#             custom_audience_level="senior",
#         )
#     )
#     submissions.append(
#         submission_factory(
#             conference=conference,
#             tags=["pizza"],
#             speaker_id=2,
#             languages=[
#                 "it",
#             ],
#             custom_submission_type="Talk",
#             custom_audience_level="senior",
#         )
#     )
#     submissions.append(
#         submission_factory(
#             conference=conference,
#             tags=["pizza"],
#             speaker_id=5,
#             languages=[
#                 "en",
#             ],
#             custom_submission_type="Talk",
#             custom_audience_level="senior",
#         )
#     )

#     user1 = user_factory()
#     user2 = user_factory()
#     user3 = user_factory()

#     vote_factory(user_id=user1.id, submission=submissions[0], value=1)
#     vote_factory(user_id=user1.id, submission=submissions[1], value=2)
#     vote_factory(user_id=user1.id, submission=submissions[2], value=3)
#     vote_factory(user_id=user1.id, submission=submissions[3], value=4)

#     vote_factory(user_id=user2.id, submission=submissions[0], value=1)
#     vote_factory(user_id=user2.id, submission=submissions[6], value=1)

#     vote_factory(user_id=user3.id, submission=submissions[5], value=4)

#     users_weights = {
#         (user1.id, sushi.id): 2.0,
#         (user2.id, pizza.id): 1.0,
#         (user2.id, sushi.id): 1.0,
#         (user3.id, pizza.id): 1.0,
#     }
#     votes = Vote.objects.all()

#     ranked_submissions = [
#         {
#             "submission_id": submissions[3].id,
#             "submission__tag_id": submissions[3].topic.id,
#             "score": 4.0,
#         },
#         {
#             "submission_id": submissions[6].id,
#             "submission__tag_id": submissions[6].topic.id,
#             "score": 1.0,
#         },
#         {
#             "submission_id": submissions[2].id,
#             "submission__tag_id": submissions[2].topic.id,
#             "score": 3.0,
#         },
#         {
#             "submission_id": submissions[5].id,
#             "submission__tag_id": submissions[5].topic.id,
#             "score": 4.0,
#         },
#         {
#             "submission_id": submissions[4].id,
#             "submission__tag_id": submissions[4].topic.id,
#             "score": 0,
#         },
#         {
#             "submission_id": submissions[1].id,
#             "submission__tag_id": submissions[1].topic.id,
#             "score": 2.0,
#         },
#         {
#             "submission_id": submissions[0].id,
#             "submission__tag_id": submissions[0].topic.id,
#             "score": 1.0,
#         },
#     ]
#     return conference, votes, users_weights, ranked_submissions


# @pytest.mark.skip
# def test_most_voted_based_algorithm(_voting_fixture, mock_users):
#     conference, _, _, ranked_submissions = _voting_fixture

#     ranking = RankRequest.objects.create(conference=conference, is_public=True)
#     for index, rank in enumerate(ranking.rank_submissions.all().order_by("rank")):
#         assert rank.submission.id == ranked_submissions[index]["submission_id"]
#         assert round(rank.score, 2) == round(ranked_submissions[index]["score"], 2)


# def test_ranking_only_on_proposed_submissions(
#     conference, submission_factory, mock_users
# ):
#     valid_submission = submission_factory(status="proposed", conference=conference)
#     cancelled_submission = submission_factory(status="cancelled", conference=conference)

#     ranking = RankRequest.objects.create(conference=conference, is_public=True)

#     submissions_ids = [rs.submission.pk for rs in ranking.rank_submissions.all()]
#     assert len(submissions_ids) == 1
#     assert valid_submission.pk in submissions_ids
#     assert cancelled_submission.pk not in submissions_ids


# def test_weights(_voting_fixture):
#     _, votes, weights, _ = _voting_fixture
#     assert weights == RankRequest.get_users_weights(votes)


# def test_stats(mock_users, _voting_fixture):
#     conference, _, _, _ = _voting_fixture

#     ranking = RankRequest.objects.create(conference=conference, is_public=True)

#     stats = ranking.stats.all()

#     assert len(stats) == 14
#     assert stats.filter(type=RankStat.Type.SUBMISSIONS).first().value == 7
#     assert stats.filter(type=RankStat.Type.SPEAKERS).first().value == 5
#     assert stats.filter(type=RankStat.Type.LANGUAGE, name="English").first().value == 5
#     assert stats.filter(type=RankStat.Type.LANGUAGE, name="Italian").first().value == 4
#     assert (
#         stats.filter(type=RankStat.Type.SUBMISSION_TYPE, name="Talk").first().value == 4
#     )
#     assert (
#         stats.filter(type=RankStat.Type.SUBMISSION_TYPE, name="Workshop").first().value
#         == 3
#     )
#     assert (
#         stats.filter(type=RankStat.Type.AUDIENCE_LEVEL, name="adult").first().value == 1
#     )
#     assert (
#         stats.filter(type=RankStat.Type.AUDIENCE_LEVEL, name="senior").first().value
#         == 6
#     )

#     assert stats.filter(type=RankStat.Type.TOPIC, name="Sushi").first().value == 4
#     assert stats.filter(type=RankStat.Type.TOPIC, name="Pizza").first().value == 3
#     assert stats.filter(type=RankStat.Type.GENDER, name="Male").first().value == 2
#     assert stats.filter(type=RankStat.Type.GENDER, name="Female").first().value == 1
#     assert (
#         stats.filter(type=RankStat.Type.GENDER, name="Prefer not to say").first().value
#         == 1
#     )
#     assert stats.filter(type=RankStat.Type.GENDER, name="Other").first().value == 1


def test_tag_count_should_remain_the_same(
    conference_factory,
    user_factory,
    submission_factory,
    submission_tag_factory,
    vote_factory,
    conference,
):
    pizza = submission_tag_factory(name="Pizza")
    sushi = submission_tag_factory(name="Sushi")
    polenta = submission_tag_factory(name="Polenta")

    submissions = [
        submission_factory(
            conference=conference,
            tags=["Polenta"],
        ),
        submission_factory(
            conference=conference,
            tags=['Polenta']
,
        ),
        submission_factory(
            conference=conference,
            tags=['Pizza', 'Sushi']
,
        ),
        submission_factory(
            conference=conference,
            tags=['Pizza', 'Sushi']
,
        ),
        submission_factory(
            conference=conference,
            tags=['Pizza', 'Polenta']
,
        ),
        submission_factory(
            conference=conference,
            tags=['Pizza', 'Polenta']
,
        ),
        submission_factory(
            conference=conference,
            tags=['Polenta', 'Sushi', 'Sushi']
,
        ),
        submission_factory(
            conference=conference,
            tags=["Pizza"],
        ),
        submission_factory(
            conference=conference,
            tags=["Pizza"],
        ),
        submission_factory(
            conference=conference,
            tags=["Polenta"],
        ),
    ]

    ranking = RankRequest.objects.create(conference=conference, is_public=True)

    assert ranking.rank_submissions.filter(tag=polenta).count() ==  6
    assert ranking.rank_submissions.filter(tag=sushi).count() ==  3
    assert ranking.rank_submissions.filter(tag=pizza).count() ==  6
