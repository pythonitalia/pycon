from datetime import datetime, timedelta

import pytest
from asgiref.sync import async_to_sync
from django.utils import timezone
from resonate.resonate import Resonate
from resonate.retry import Never

from cms.models import FAQ, GenericCopy, Menu
from cms.tests.factories import (
    FAQFactory,
    GenericCopyFactory,
    MenuFactory,
    MenuLinkFactory,
)
from conferences.models import Conference, Deadline, Duration
from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DeadlineFactory,
    DurationFactory,
    TopicFactory,
)
from conferences.workflows import CLONE_CONFERENCE, clone_conference
from generic_forms.models import Form, FormQuestion
from generic_forms.tests.factories import FormFactory, FormQuestionFactory
from pycon.constants import UTC
from notifications.models import EmailTemplate, EmailTemplateIdentifier
from notifications.tests.factories import EmailTemplateFactory
from sponsors.models import (
    SponsorBenefit,
    SponsorLevel,
    SponsorLevelBenefit,
    SponsorSpecialOption,
)
from sponsors.tests.factories import (
    SponsorBenefitFactory,
    SponsorFactory,
    SponsorLevelBenefitFactory,
    SponsorLevelFactory,
    SponsorSpecialOptionFactory,
)
from submissions.tests.factories import SubmissionTypeFactory
from voting.models import IncludedEvent
from voting.tests.factories.included_event import IncludedEventFactory

pytestmark = pytest.mark.django_db

NEW_START = datetime(2027, 5, 26, 9, 0, tzinfo=UTC)
NEW_END = datetime(2027, 5, 30, 18, 0, tzinfo=UTC)


def run_clone(source_code, new_code="pycon2027", workflow_id=None, **kwargs):
    """Run the workflow in-process, on Resonate's local (in-memory) connection.

    ``async_to_sync`` (rather than ``asyncio.run``) so the steps' thread
    sensitive database work runs back in this thread -- the one holding the
    test transaction.
    """

    async def go():
        resonate = Resonate(autostart=False, retry_policy=Never())
        resonate.register(clone_conference, name=CLONE_CONFERENCE)
        resonate.start()

        try:
            handle = resonate.run(
                workflow_id or f"clone-{new_code}",
                clone_conference,
                source_code=source_code,
                new_code=new_code,
                new_name=kwargs.get("new_name", "PyCon Italia 2027"),
                new_start=kwargs.get("new_start", NEW_START).isoformat(),
                new_end=kwargs.get("new_end", NEW_END).isoformat(),
                new_hostname=kwargs.get("new_hostname", "pycon2027.example.com"),
            )
            return await handle.result()
        finally:
            await resonate.stop()

    return async_to_sync(go)()


@pytest.fixture
def source_conference():
    return ConferenceFactory(
        code="pycon2026",
        start=datetime(2026, 5, 27, 9, 0, tzinfo=UTC),
        end=datetime(2026, 5, 31, 18, 0, tzinfo=UTC),
        hostname="pycon2026.example.com",
        location="Bologna",
        slack_new_proposal_channel_id="C123",
        max_proposals_per_user=3,
    )


def test_creates_the_new_conference_from_the_source(source_conference):
    source_conference.topics.add(TopicFactory(name="Web"))
    source_conference.audience_levels.add(AudienceLevelFactory(name="Beginner"))
    source_conference.submission_types.add(SubmissionTypeFactory(name="Talk"))

    result = run_clone(source_conference.code)

    conference = Conference.objects.get(code="pycon2027")

    assert result["conference_id"] == conference.id
    assert str(conference.name) == "PyCon Italia 2027"
    assert conference.hostname == "pycon2027.example.com"
    assert conference.start == NEW_START
    assert conference.end == NEW_END
    assert conference.organizer_id == source_conference.organizer_id
    assert conference.location == "Bologna"
    assert conference.slack_new_proposal_channel_id == "C123"
    assert conference.max_proposals_per_user == 3
    assert list(conference.topics.all()) == list(source_conference.topics.all())
    assert list(conference.audience_levels.all()) == list(
        source_conference.audience_levels.all()
    )
    assert list(conference.submission_types.all()) == list(
        source_conference.submission_types.all()
    )


def test_does_not_copy_edition_specific_data(source_conference):
    run_clone(source_conference.code)

    conference = Conference.objects.get(code="pycon2027")

    assert conference.pretix_organizer_id == ""
    assert conference.pretix_event_id == ""
    assert conference.pretix_event_url == ""
    assert conference.pretix_conference_voucher_quota_id is None


def test_copies_deadlines_shifted_by_the_new_start_date(source_conference):
    DeadlineFactory(
        conference=source_conference,
        type=Deadline.TYPES.cfp,
        start=datetime(2026, 1, 10, 10, 0, tzinfo=UTC),
        end=datetime(2026, 2, 10, 10, 0, tzinfo=UTC),
    )

    result = run_clone(source_conference.code)

    shift = NEW_START - source_conference.start
    deadline = Deadline.objects.get(
        conference__code="pycon2027", type=Deadline.TYPES.cfp
    )

    assert result["copied"]["deadlines"] == 1
    assert deadline.start == datetime(2026, 1, 10, 10, 0, tzinfo=UTC) + shift
    assert deadline.end == datetime(2026, 2, 10, 10, 0, tzinfo=UTC) + shift


def test_copies_durations_with_their_submission_types(source_conference):
    submission_type = SubmissionTypeFactory(name="Talk")
    duration = DurationFactory(
        conference=source_conference, name="Standard", duration=45, notes="Notes"
    )
    duration.allowed_submission_types.add(submission_type)

    result = run_clone(source_conference.code)

    new_duration = Duration.objects.get(conference__code="pycon2027", name="Standard")

    assert result["copied"]["durations"] == 1
    assert new_duration.duration == 45
    assert new_duration.notes == "Notes"
    assert list(new_duration.allowed_submission_types.all()) == [submission_type]


def test_copies_sponsor_configuration_without_the_sponsors(source_conference):
    benefit = SponsorBenefitFactory(
        conference=source_conference, name="Booth", category="booth"
    )
    level = SponsorLevelFactory(
        conference=source_conference, name="Gold", price=1000, slots=3
    )
    level.sponsors.add(SponsorFactory())
    SponsorLevelBenefitFactory(sponsor_level=level, benefit=benefit, value="2")
    SponsorSpecialOptionFactory(
        conference=source_conference, name="Job board", price=100
    )

    run_clone(source_conference.code)

    conference = Conference.objects.get(code="pycon2027")
    new_level = SponsorLevel.objects.get(conference=conference, name="Gold")
    new_benefit = SponsorBenefit.objects.get(conference=conference)

    assert new_level.price == 1000
    assert new_level.slots == 3
    assert new_level.sponsors.count() == 0
    assert str(new_benefit.name) == "Booth"
    assert SponsorLevelBenefit.objects.filter(
        sponsor_level=new_level, benefit=new_benefit
    ).exists()
    assert SponsorSpecialOption.objects.filter(
        conference=conference, name="Job board"
    ).exists()


def test_copies_email_templates(source_conference):
    EmailTemplateFactory(
        conference=source_conference,
        identifier=EmailTemplateIdentifier.proposal_accepted,
        subject="Congrats",
        body="Body",
    )
    EmailTemplateFactory(
        conference=source_conference,
        identifier=EmailTemplateIdentifier.custom,
        name="Sponsors update",
        subject="Update",
    )

    result = run_clone(source_conference.code)

    conference = Conference.objects.get(code="pycon2027")
    accepted = EmailTemplate.objects.get(
        conference=conference, identifier=EmailTemplateIdentifier.proposal_accepted
    )

    assert result["copied"]["email_templates"] == 2
    assert accepted.subject == "Congrats"
    assert EmailTemplate.objects.filter(
        conference=conference,
        identifier=EmailTemplateIdentifier.custom,
        name="Sponsors update",
    ).exists()


def test_copies_cms_content(source_conference):
    GenericCopyFactory(conference=source_conference, key="homepage-intro")
    FAQFactory(conference=source_conference)
    menu = MenuFactory(conference=source_conference, identifier="main")
    MenuLinkFactory(menu=menu)

    run_clone(source_conference.code)

    conference = Conference.objects.get(code="pycon2027")
    new_menu = Menu.objects.get(conference=conference, identifier="main")

    assert GenericCopy.objects.filter(
        conference=conference, key="homepage-intro"
    ).exists()
    assert FAQ.objects.filter(conference=conference).count() == 1
    assert new_menu.links.count() == 1


def test_copies_forms_and_questions_but_no_answers(source_conference):
    form = FormFactory(
        conference=source_conference, purpose=Form.Purpose.GRANT, name="Grant form"
    )
    FormQuestionFactory(form=form, label="Why do you need a grant?", required=True)

    run_clone(source_conference.code)

    conference = Conference.objects.get(code="pycon2027")
    new_form = Form.objects.get(conference=conference, purpose=Form.Purpose.GRANT)
    question = FormQuestion.objects.get(form=new_form)

    assert new_form.name == "Grant form"
    assert question.label == "Why do you need a grant?"
    assert question.required is True
    assert new_form.answers.count() == 0


def test_copies_voting_included_events(source_conference):
    IncludedEventFactory(
        conference=source_conference,
        pretix_organizer_id="python-italia",
        pretix_event_id="pycon2025",
    )

    run_clone(source_conference.code)

    assert IncludedEvent.objects.filter(
        conference__code="pycon2027",
        pretix_organizer_id="python-italia",
        pretix_event_id="pycon2025",
    ).exists()


def test_running_the_workflow_again_does_not_duplicate_anything(source_conference):
    DeadlineFactory(conference=source_conference, type=Deadline.TYPES.cfp)
    DurationFactory(conference=source_conference, name="Standard")
    SponsorLevelFactory(conference=source_conference, name="Gold")
    GenericCopyFactory(conference=source_conference, key="homepage-intro")

    first = run_clone(source_conference.code, workflow_id="clone-first-run")
    second = run_clone(source_conference.code, workflow_id="clone-second-run")

    assert second["conference_id"] == first["conference_id"]
    assert Conference.objects.filter(code="pycon2027").count() == 1
    assert Deadline.objects.filter(conference__code="pycon2027").count() == 1
    assert Duration.objects.filter(conference__code="pycon2027").count() == 1
    assert SponsorLevel.objects.filter(conference__code="pycon2027").count() == 1
    assert GenericCopy.objects.filter(conference__code="pycon2027").count() == 1
    assert all(count == 0 for count in second["copied"].values())


def test_deadlines_are_not_shifted_when_the_source_has_no_dates(source_conference):
    source_conference.start = None
    source_conference.end = None
    source_conference.save()

    start = timezone.now()
    DeadlineFactory(
        conference=source_conference,
        type=Deadline.TYPES.cfp,
        start=start,
        end=start + timedelta(days=30),
    )

    run_clone(source_conference.code)

    deadline = Deadline.objects.get(
        conference__code="pycon2027", type=Deadline.TYPES.cfp
    )

    assert deadline.start == start
