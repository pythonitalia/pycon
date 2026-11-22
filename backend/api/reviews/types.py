import re
from urllib.parse import urljoin

import strawberry
from django.conf import settings
from django.db.models import Prefetch
from django.template.defaultfilters import linebreaksbr
from django.urls import reverse

from countries import countries
from grants import models as grants_models
from markdownify.templatetags.markdownify import markdownify
from participants import models as participants_models
from reviews import models
from submissions import models as submissions_models


@strawberry.type
class ScoreOption:
    id: strawberry.ID
    label: str
    numeric_value: int


@strawberry.type
class ReviewTag:
    id: strawberry.ID
    name: str


@strawberry.type
class ReviewSession:
    id: strawberry.ID
    score_options: list[ScoreOption]
    tags: list[ReviewTag]

    @classmethod
    def from_model(cls, review_session: models.ReviewSession):
        score_options = review_session.availablescoreoption_set.order_by(
            "-numeric_value"
        )
        used_tag_ids = (
            submissions_models.Submission.objects.for_conference(
                review_session.conference_id
            )
            .values_list("tags__id", flat=True)
            .distinct()
        )
        tags = submissions_models.SubmissionTag.objects.filter(
            id__in=used_tag_ids
        ).order_by("name")

        return cls(
            id=review_session.id,
            score_options=[
                ScoreOption(
                    id=option.id,
                    label=option.label,
                    numeric_value=option.numeric_value,
                )
                for option in score_options
            ],
            tags=[ReviewTag(id=tag.id, name=tag.name) for tag in tags],
        )


@strawberry.type
class TextInLanguages:
    en: str | None
    it: str | None


@strawberry.type
class Ranking:
    tag: str
    rank: int
    total: int


@strawberry.type
class ReviewVote:
    id: strawberry.ID
    reviewer_name: str
    is_mine: bool
    score_label: str | None
    score_value: int | None
    comment: str


@strawberry.type
class MyVote:
    score_option_id: strawberry.ID | None
    comment: str


@strawberry.type
class SpeakerGrant:
    status: str
    admin_url: str


@strawberry.type
class OtherProposal:
    id: strawberry.ID
    title: str


@strawberry.type
class ReviewSpeaker:
    id: strawberry.ID
    full_name: str
    gender: str | None
    country: str | None
    photo_url: str | None
    bio: str | None
    website: str | None
    twitter_handle: str | None
    instagram_handle: str | None
    mastodon_handle: str | None
    linkedin_url: str | None
    facebook_url: str | None
    speaker_level: str | None
    previous_talk_video: str | None
    participant_admin_url: str | None
    grant: SpeakerGrant | None
    proposals_count: int
    max_proposals: int | None
    other_proposals: list[OtherProposal]


@strawberry.type
class ReviewProposal:
    id: strawberry.ID
    title: TextInLanguages
    elevator_pitch_html: TextInLanguages
    abstract_html: TextInLanguages
    notes: str
    tags: list[ReviewTag]
    type: str
    audience_level: str
    duration: int
    languages: list[str]
    rankings: list[Ranking]
    website_url: str
    admin_url: str
    is_mine: bool
    speaker: ReviewSpeaker
    votes: list[ReviewVote]
    my_vote: MyVote | None

    @classmethod
    def from_model(
        cls,
        proposal: submissions_models.Submission,
        review_session: models.ReviewSession,
        user,
    ):
        languages = [language.code for language in proposal.languages.all()]
        votes = list(
            models.UserReview.objects.filter(
                review_session=review_session, proposal=proposal
            )
            .select_related("user", "score")
            .order_by("created")
        )
        my_vote = next((vote for vote in votes if vote.user_id == user.id), None)

        return cls(
            id=proposal.id,
            title=_in_languages(proposal.title, languages),
            elevator_pitch_html=_in_languages(
                proposal.elevator_pitch, languages, _markdown_to_html
            ),
            abstract_html=_in_languages(
                proposal.abstract, languages, _markdown_to_html
            ),
            notes=proposal.notes,
            tags=[ReviewTag(id=tag.id, name=tag.name) for tag in proposal.tags.all()],
            type=proposal.type.name,
            audience_level=proposal.audience_level.name,
            duration=proposal.duration.duration,
            languages=languages,
            rankings=[
                Ranking(
                    tag=ranking.tag.name if ranking.tag else "",
                    rank=ranking.rank,
                    total=ranking.total_submissions_per_tag,
                )
                for ranking in proposal.rankings.select_related("tag").order_by(
                    "tag__name"
                )
            ],
            website_url=urljoin(
                settings.FRONTEND_URL, f"/submission/{proposal.hashid}"
            ),
            admin_url=reverse(
                "admin:submissions_submission_change", args=(proposal.id,)
            ),
            is_mine=proposal.speaker_id == user.id,
            speaker=_build_speaker(proposal),
            votes=[
                ReviewVote(
                    id=vote.id,
                    reviewer_name=vote.user.display_name,
                    is_mine=vote.user_id == user.id,
                    score_label=vote.score.label if vote.score else None,
                    score_value=vote.score.numeric_value if vote.score else None,
                    comment=vote.comment,
                )
                for vote in votes
            ],
            my_vote=MyVote(score_option_id=my_vote.score_id, comment=my_vote.comment)
            if my_vote
            else None,
        )


def _in_languages(
    text, language_codes: list[str], render=lambda value: value
) -> TextInLanguages:
    return TextInLanguages(
        en=render(text.localize("en")) if "en" in language_codes else None,
        it=render(text.localize("it")) if "it" in language_codes else None,
    )


LIST_TAG_WHITESPACE = re.compile(r"\s*(</?(?:ul|ol|li)>)\s*")


def _markdown_to_html(text: str) -> str:
    # Without this, linebreaksbr adds a <br> next to every list tag.
    html = LIST_TAG_WHITESPACE.sub(r"\1", markdownify(text))
    return linebreaksbr(html, autoescape=False)


def _build_speaker(proposal: submissions_models.Submission) -> ReviewSpeaker:
    speaker = proposal.speaker
    conference = proposal.conference
    participant = participants_models.Participant.objects.filter(
        user_id=speaker.id, conference_id=conference.id
    ).first()
    grant = (
        grants_models.Grant.objects.of_user(speaker.id)
        .for_conference(conference.id)
        .first()
    )
    speaker_proposals = list(
        submissions_models.Submission.objects.non_cancelled()
        .for_conference(conference.id)
        .of_user(speaker.id)
        .order_by("created")
    )
    country = countries.get(code=speaker.country) if speaker.country else None

    return ReviewSpeaker(
        id=speaker.id,
        full_name=speaker.full_name,
        gender=speaker.get_gender_display()
        if speaker.gender and speaker.gender != "not_say"
        else None,
        country=country.name if country else None,
        photo_url=participant.photo_url if participant else None,
        bio=participant.bio if participant else None,
        website=participant.website if participant else None,
        twitter_handle=participant.twitter_handle if participant else None,
        instagram_handle=participant.instagram_handle if participant else None,
        mastodon_handle=participant.mastodon_handle if participant else None,
        linkedin_url=participant.linkedin_url if participant else None,
        facebook_url=participant.facebook_url if participant else None,
        speaker_level=participant.get_speaker_level_display()
        if participant and participant.speaker_level
        else None,
        previous_talk_video=participant.previous_talk_video if participant else None,
        participant_admin_url=reverse(
            "admin:participants_participant_change", args=(participant.id,)
        )
        if participant
        else None,
        grant=SpeakerGrant(
            status=grant.get_status_display(),
            admin_url=reverse("admin:grants_grant_change", args=(grant.id,)),
        )
        if grant
        else None,
        proposals_count=len(speaker_proposals),
        max_proposals=conference.max_proposals_per_user,
        other_proposals=[
            OtherProposal(id=other.id, title=other.title.localize("en"))
            for other in speaker_proposals
            if other.id != proposal.id
        ],
    )


def review_proposals_queryset(review_session: models.ReviewSession):
    return (
        submissions_models.Submission.objects.non_cancelled()
        .for_conference(review_session.conference_id)
        .select_related("speaker", "conference", "type", "audience_level", "duration")
        .prefetch_related(
            "languages",
            Prefetch(
                "tags",
                queryset=submissions_models.SubmissionTag.objects.order_by("name"),
            ),
        )
    )
