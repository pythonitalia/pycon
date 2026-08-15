from datetime import date, time

from schedule.tests.factories import (
    DayFactory,
    ScheduleItemAdditionalSpeakerFactory,
    ScheduleItemFactory,
    SlotFactory,
)
from submissions.tests.factories import SubmissionFactory
from conferences.tests.factories import (
    ConferenceFactory,
    KeynoteFactory,
    KeynoteSpeakerFactory,
    ConferenceVoucherFactory,
)
from users.tests.factories import UserFactory
from unittest.mock import call
import time_machine
from django.core import exceptions
from django.forms.fields import BooleanField
from pytest import fixture, mark, raises
from django.contrib.admin.sites import AdminSite

from conferences.admin import (
    ConferenceAdmin,
)
from conferences.admin.actions import (
    create_conference_vouchers_on_pretix,
    send_voucher_via_email,
)
from conferences.admin.conference import (
    validate_deadlines_form,
    walk_conference_videos_folder,
    DeadlineForm,
)
from conferences.models import ConferenceVoucher
from schedule.models import ScheduleItem

pytestmark = mark.django_db


@fixture(autouse=False)
def add_delete_field_to_form():
    DeadlineForm.base_fields["DELETE"] = BooleanField(required=False)
    yield
    del DeadlineForm.base_fields["DELETE"]


def test_can_have_multiple_deadlines_only_if_the_other_are_deleted(
    add_delete_field_to_form,
):
    conference = ConferenceFactory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2022-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "cfp",
            "conference": conference.id,
            "DELETE": False,
        }
    )
    form_2 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2023-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "cfp",
            "conference": conference.id,
            "DELETE": True,
        }
    )

    form_1.is_valid()
    form_2.is_valid()

    forms = [form_1, form_2]

    validate_deadlines_form(forms)


@mark.parametrize("type", ["cfp", "voting", "refund"])
def test_cannot_have_duplicate_deadlines(type, add_delete_field_to_form):
    conference = ConferenceFactory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2022-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": type,
            "conference": conference.id,
            "DELETE": False,
        }
    )
    form_2 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2023-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": type,
            "conference": conference.id,
            "DELETE": False,
        }
    )

    form_1.is_valid()
    form_2.is_valid()

    forms = [form_1, form_2]

    with raises(
        exceptions.ValidationError,
        match=f"You can only have one deadline of type {type}",
    ):
        validate_deadlines_form(forms)


def test_start_date_comes_before_end(add_delete_field_to_form):
    conference = ConferenceFactory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2020-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "cfp",
            "conference": conference.id,
            "DELETE": False,
        }
    )

    form_1.is_valid()

    forms = [form_1]

    with raises(exceptions.ValidationError, match="Start date cannot be after end"):
        validate_deadlines_form(forms)


def test_can_have_as_many_custom_deadlines_as_we_want(add_delete_field_to_form):
    conference = ConferenceFactory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2022-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "custom",
            "conference": conference.id,
            "DELETE": False,
        }
    )
    form_2 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2023-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "custom",
            "conference": conference.id,
            "DELETE": False,
        }
    )

    form_1.is_valid()
    form_2.is_valid()

    forms = [form_1, form_2]

    validate_deadlines_form(forms)


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_send_voucher_via_email(
    rf,
    mocker,
):
    mocker.patch("conferences.admin.actions.messages")
    mocker.patch("custom_admin.admin.messages")

    mock_send_email = mocker.patch(
        "conferences.admin.actions.send_conference_voucher_email"
    )

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )

    conference_voucher_1 = ConferenceVoucherFactory(
        conference=conference,
        user_id=schedule_item_1.submission.speaker_id,
        pretix_voucher_id=1,
    )
    conference_voucher_2 = ConferenceVoucherFactory(
        conference=conference,
        user_id=schedule_item_2.submission.speaker_id,
        pretix_voucher_id=2,
    )

    send_voucher_via_email(
        None,
        rf.get("/"),
        queryset=ConferenceVoucher.objects.filter(conference=conference),
    )

    mock_send_email.delay.assert_has_calls(
        [
            call(conference_voucher_id=conference_voucher_1.id),
            call(conference_voucher_id=conference_voucher_2.id),
        ],
        any_order=True,
    )


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_send_voucher_via_email_requires_filtering_by_conference(
    rf,
    mocker,
):
    mock_messages = mocker.patch("custom_admin.admin.messages")
    mock_send_email = mocker.patch(
        "conferences.admin.actions.send_conference_voucher_email"
    )

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    conference_2 = ConferenceFactory(pretix_conference_voucher_quota_id=123)

    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference_2,
        submission=SubmissionFactory(conference=conference_2),
    )

    ConferenceVoucherFactory(
        conference=conference,
        user_id=schedule_item_1.submission.speaker_id,
        pretix_voucher_id=1,
    )
    ConferenceVoucherFactory(
        conference=conference_2,
        user_id=schedule_item_2.submission.speaker_id,
        pretix_voucher_id=2,
    )

    request = rf.get("/")
    send_voucher_via_email(
        None,
        request,
        queryset=ConferenceVoucher.objects.filter(
            conference__in=[conference, conference_2]
        ),
    )

    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )
    mock_send_email.delay.assert_not_called()


def test_create_conference_vouchers_on_pretix(rf, mocker):
    mock_create_voucher = mocker.patch(
        "conferences.admin.actions.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
            {"id": 3},
            {"id": 4},
        ],
    )
    mocker.patch("custom_admin.admin.messages")
    mocker.patch("conferences.admin.actions.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)

    voucher_1 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-123",
        pretix_voucher_id=None,
    )

    voucher_2 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-456",
        pretix_voucher_id=None,
    )

    voucher_3 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-999",
        pretix_voucher_id=None,
        voucher_type=ConferenceVoucher.VoucherType.CO_SPEAKER,
    )

    voucher_4 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-888",
        pretix_voucher_id=None,
        voucher_type=ConferenceVoucher.VoucherType.GRANT,
    )

    create_conference_vouchers_on_pretix(
        None,
        request=rf.get("/"),
        queryset=ConferenceVoucher.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_has_calls(
        [
            call(
                conference=conference,
                code="SPEAKER-123",
                comment=f"Voucher for user_id={voucher_1.user_id}",
                tag="speaker",
                quota_id=123,
                price_mode="set",
                value="0.00",
            ),
            call(
                conference=conference,
                code="SPEAKER-456",
                comment=f"Voucher for user_id={voucher_2.user_id}",
                tag="speaker",
                quota_id=123,
                price_mode="set",
                value="0.00",
            ),
            call(
                conference=conference,
                code="SPEAKER-999",
                comment=f"Voucher for user_id={voucher_3.user_id}",
                tag="co_speaker",
                quota_id=123,
                price_mode="percent",
                value="25.00",
            ),
            call(
                conference=conference,
                code="SPEAKER-888",
                comment=f"Voucher for user_id={voucher_4.user_id}",
                tag="grant",
                quota_id=123,
                price_mode="set",
                value="0.00",
            ),
        ],
        any_order=True,
    )

    voucher_1.refresh_from_db()
    voucher_2.refresh_from_db()
    voucher_3.refresh_from_db()

    assert voucher_1.pretix_voucher_id == 1
    assert voucher_2.pretix_voucher_id == 2
    assert voucher_3.pretix_voucher_id == 3


def test_create_conference_vouchers_on_pretix_only_for_missing_ones(rf, mocker):
    mock_create_voucher = mocker.patch(
        "conferences.admin.actions.create_voucher",
        side_effect=[
            {"id": 1},
        ],
    )
    mocker.patch("conferences.admin.actions.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)

    voucher_1 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-123",
        pretix_voucher_id=None,
    )

    voucher_2 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-456",
        pretix_voucher_id=1155,
    )

    create_conference_vouchers_on_pretix(
        None,
        request=rf.get("/"),
        queryset=ConferenceVoucher.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_called_once_with(
        conference=conference,
        code="SPEAKER-123",
        comment=f"Voucher for user_id={voucher_1.user_id}",
        tag="speaker",
        quota_id=123,
        price_mode="set",
        value="0.00",
    )

    voucher_1.refresh_from_db()
    voucher_2.refresh_from_db()

    assert voucher_1.pretix_voucher_id == 1
    assert voucher_2.pretix_voucher_id == 1155


def test_create_conference_vouchers_on_pretix_doesnt_work_with_multiple_conferences(
    rf, mocker
):
    mock_create_voucher = mocker.patch(
        "conferences.admin.actions.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mock_messages = mocker.patch("custom_admin.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    conference_2 = ConferenceFactory(pretix_conference_voucher_quota_id=123)

    voucher_1 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-123",
        pretix_voucher_id=None,
    )

    voucher_2 = ConferenceVoucherFactory(
        conference=conference_2,
        voucher_code="SPEAKER-456",
        pretix_voucher_id=None,
    )

    request = rf.get("/")

    create_conference_vouchers_on_pretix(
        None,
        request=request,
        queryset=ConferenceVoucher.objects.filter(
            conference__in=[conference, conference_2]
        ),
    )

    mock_create_voucher.assert_not_called()
    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )

    voucher_1.refresh_from_db()
    voucher_2.refresh_from_db()

    assert voucher_1.pretix_voucher_id is None
    assert voucher_2.pretix_voucher_id is None


def test_create_conference_vouchers_on_pretix_doesnt_work_without_pretix_config(
    rf, mocker
):
    mock_create_voucher = mocker.patch(
        "conferences.admin.actions.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mock_messages = mocker.patch("conferences.admin.actions.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=None)

    voucher_1 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-123",
        pretix_voucher_id=None,
    )

    voucher_2 = ConferenceVoucherFactory(
        conference=conference,
        voucher_code="SPEAKER-456",
        pretix_voucher_id=None,
    )

    request = rf.get("/")

    create_conference_vouchers_on_pretix(
        None,
        request=request,
        queryset=ConferenceVoucher.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_not_called()
    mock_messages.error.assert_called_once_with(
        request,
        "Please configure the conference voucher quota ID in the conference settings",
    )

    voucher_1.refresh_from_db()
    voucher_2.refresh_from_db()

    assert voucher_1.pretix_voucher_id is None
    assert voucher_2.pretix_voucher_id is None


def test_video_uploaded_path_matcher(
    rf,
    mocker,
):
    conference = ConferenceFactory(code="conf")

    kim = UserFactory(id=5, name="Kim", full_name="Kim Kitsuragi")
    klaasje = UserFactory(id=10, name="Klaasje", full_name="")
    harrier = UserFactory(id=20, name="Harrier", full_name="Harrier Du Bois")
    anwesha = UserFactory(id=23, name="", full_name="Anwesha Das")
    marcsed = UserFactory(id=99, name="Marcsed", full_name="Marcsed Cazzęfa")

    mocker.patch(
        "conferences.admin.conference.walk_conference_videos_folder",
        return_value=[
            "conf/video-1/1-Kim-Kitsuragi.mp4",
            "conf/video-2/2-Opening.mp4",
            "conf/video-2/5-Klaasje, Harrier Du Bois.mp4",
            "conf/video-2/2-Harrier Du Bois, Klaasje.mp4",
            "conf/video-2/5-Testing Name.mp4",
            "conf/video-2/12-Klaasje.mp4",
            "conf/9-Anwesha Das.mp4",
            "conf/video-2/5-Marcsed Cazzęfa.mp4",
        ],
    )

    request = rf.post("/", data={"run_matcher": "1"})
    event_1 = ScheduleItemFactory(
        conference=conference,
        title="Opening",
        type=ScheduleItem.TYPES.custom,
        submission=None,
    )
    event_2 = ScheduleItemFactory(
        conference=conference,
        title="Talk about something",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=kim,
    )

    event_klaasje_alone = ScheduleItemFactory(
        conference=conference,
        title="Klaasje smokes",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=klaasje,
    )

    event_3 = ScheduleItemFactory(
        conference=conference,
        title="Event 3 Talk about something",
        type=ScheduleItem.TYPES.talk,
        submission=None,
    )
    ScheduleItemAdditionalSpeakerFactory(scheduleitem=event_3, user=klaasje)
    ScheduleItemAdditionalSpeakerFactory(scheduleitem=event_3, user=harrier)

    event_ord_speakers = ScheduleItemFactory(
        conference=conference,
        title="Ordered",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=harrier,
    )
    ScheduleItemAdditionalSpeakerFactory(scheduleitem=event_ord_speakers, user=klaasje)

    keynote_object = KeynoteFactory()
    KeynoteSpeakerFactory(
        keynote=keynote_object,
        user=anwesha,
    )
    keynote_schedule = ScheduleItemFactory(
        conference=conference,
        title="Keynote",
        type=ScheduleItem.TYPES.keynote,
        submission=None,
        keynote=keynote_object,
    )

    special_char_speaker = ScheduleItemFactory(
        conference=conference,
        title="Special char",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=marcsed,
    )

    admin = ConferenceAdmin(
        model=conference.__class__,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    ret = admin.map_videos(request, conference.id)

    assert ret.status_code == 302

    event_1.refresh_from_db()
    event_2.refresh_from_db()
    event_3.refresh_from_db()
    event_klaasje_alone.refresh_from_db()
    keynote_schedule.refresh_from_db()
    special_char_speaker.refresh_from_db()
    event_ord_speakers.refresh_from_db()

    assert event_1.video_uploaded_path == "conf/video-2/2-Opening.mp4"
    assert event_2.video_uploaded_path == "conf/video-1/1-Kim-Kitsuragi.mp4"
    assert event_3.video_uploaded_path == "conf/video-2/5-Klaasje, Harrier Du Bois.mp4"
    assert event_klaasje_alone.video_uploaded_path == "conf/video-2/12-Klaasje.mp4"
    assert keynote_schedule.video_uploaded_path == "conf/9-Anwesha Das.mp4"
    assert (
        event_ord_speakers.video_uploaded_path
        == "conf/video-2/2-Harrier Du Bois, Klaasje.mp4"
    )
    assert (
        special_char_speaker.video_uploaded_path == "conf/video-2/5-Marcsed Cazzęfa.mp4"
    )

    assert (
        "Some files were not used: conf/video-2/5-Testing Name.mp4"
        == admin.message_user.mock_calls[1].args[1]
    )


def test_video_uploaded_path_matcher_with_day_signal(rf, mocker):
    conference = ConferenceFactory(code="pycon2026")
    # workshops only on the first day: videos are numbered by talk day,
    # so D1 in the uploaded files is the second conference day
    workshops_day = DayFactory(conference=conference, day=date(2026, 5, 27))
    day_1 = DayFactory(conference=conference, day=date(2026, 5, 28))
    day_2 = DayFactory(conference=conference, day=date(2026, 5, 29))
    day_3 = DayFactory(conference=conference, day=date(2026, 5, 30))

    marco = UserFactory(name="Marco", full_name="Marco Santoni")
    igor = UserFactory(name="Igor", full_name="Igor Saggese")
    marc_andre = UserFactory(name="Marc-André", full_name="Marc-André Lemburg")
    trainer = UserFactory(name="Trainer", full_name="Some Trainer")

    mocker.patch(
        "conferences.admin.conference.walk_conference_videos_folder",
        return_value=[
            "conference-videos/pycon2026/SPAGHETTI/D1/02 - igor-saggese.mp4",
            "conference-videos/pycon2026/SPAGHETTI/D2/03 - igor-saggese.mp4",
            "conference-videos/pycon2026/TORTELLINI/D1/05 - lightning_talks_day_1.mp4",
            "conference-videos/pycon2026/TORTELLINI/D2/04 - lightning_talks_day_2.mp4",
            "conference-videos/pycon2026/TORTELLINI/D3/05 - lightning_talks_day_3.mp4",
            "conference-videos/pycon2026/TORTELLINI/D3/01 - marc-andre-lemburg.mp4",
        ],
    )

    def slot_for(day):
        return SlotFactory(day=day, hour=time(10, 0), duration=45)

    workshop_event = ScheduleItemFactory(
        conference=conference,
        title="Workshop",
        type=ScheduleItem.TYPES.training,
        submission__speaker=trainer,
        slot=slot_for(workshops_day),
    )

    multi_speaker_event = ScheduleItemFactory(
        conference=conference,
        title="Talk with two speakers",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=marco,
        slot=slot_for(day_1),
    )
    ScheduleItemAdditionalSpeakerFactory(scheduleitem=multi_speaker_event, user=igor)

    igor_solo_event = ScheduleItemFactory(
        conference=conference,
        title="Igor solo talk",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=igor,
        slot=slot_for(day_2),
    )

    lightning_talks_events = [
        ScheduleItemFactory(
            conference=conference,
            title="Lightning Talks",
            type=ScheduleItem.TYPES.custom,
            submission=None,
            slot=slot_for(day),
        )
        for day in (day_1, day_2, day_3)
    ]

    marc_andre_event = ScheduleItemFactory(
        conference=conference,
        title="Accented speaker talk",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=marc_andre,
        slot=slot_for(day_3),
    )

    admin = ConferenceAdmin(
        model=conference.__class__,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post("/", data={"run_matcher": "1"})
    ret = admin.map_videos(request, conference.id)

    assert ret.status_code == 302

    workshop_event.refresh_from_db()
    multi_speaker_event.refresh_from_db()
    igor_solo_event.refresh_from_db()
    marc_andre_event.refresh_from_db()
    for event in lightning_talks_events:
        event.refresh_from_db()

    assert workshop_event.video_uploaded_path == ""
    # the file is named after only one of the two speakers,
    # the day disambiguates it from igor's solo talk
    assert (
        multi_speaker_event.video_uploaded_path
        == "conference-videos/pycon2026/SPAGHETTI/D1/02 - igor-saggese.mp4"
    )
    assert (
        igor_solo_event.video_uploaded_path
        == "conference-videos/pycon2026/SPAGHETTI/D2/03 - igor-saggese.mp4"
    )
    assert (
        lightning_talks_events[0].video_uploaded_path
        == "conference-videos/pycon2026/TORTELLINI/D1/05 - lightning_talks_day_1.mp4"
    )
    assert (
        lightning_talks_events[1].video_uploaded_path
        == "conference-videos/pycon2026/TORTELLINI/D2/04 - lightning_talks_day_2.mp4"
    )
    assert (
        lightning_talks_events[2].video_uploaded_path
        == "conference-videos/pycon2026/TORTELLINI/D3/05 - lightning_talks_day_3.mp4"
    )
    assert (
        marc_andre_event.video_uploaded_path
        == "conference-videos/pycon2026/TORTELLINI/D3/01 - marc-andre-lemburg.mp4"
    )

    assert admin.message_user.mock_calls[0].args[1] == "Matched 6 videos to events."
    # every file was matched exactly once: no reuse or unused warnings
    assert admin.message_user.call_count == 1


def test_video_uploaded_path_matcher_same_speaker_twice_in_a_day(rf, mocker):
    conference = ConferenceFactory(code="pycon2026")
    day_1 = DayFactory(conference=conference, day=date(2026, 5, 28))

    ozge = UserFactory(name="Özge", full_name="Özge Çinko")

    # "4-" listed before "2-" on purpose: assignment must follow the
    # position number in the file name, not the storage listing order
    mocker.patch(
        "conferences.admin.conference.walk_conference_videos_folder",
        return_value=[
            "conference-videos/pycon2026/LASAGNA/D1/4-Ozge Cinko.mp4",
            "conference-videos/pycon2026/LASAGNA/D1/2-Ozge Cinko.mp4",
        ],
    )

    afternoon_event = ScheduleItemFactory(
        conference=conference,
        title="Afternoon talk",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=ozge,
        slot=SlotFactory(day=day_1, hour=time(14, 50), duration=45),
    )
    morning_event = ScheduleItemFactory(
        conference=conference,
        title="Morning talk",
        type=ScheduleItem.TYPES.talk,
        submission__speaker=ozge,
        slot=SlotFactory(day=day_1, hour=time(11, 40), duration=45),
    )

    admin = ConferenceAdmin(
        model=conference.__class__,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post("/", data={"run_matcher": "1"})
    ret = admin.map_videos(request, conference.id)

    assert ret.status_code == 302

    morning_event.refresh_from_db()
    afternoon_event.refresh_from_db()

    assert (
        morning_event.video_uploaded_path
        == "conference-videos/pycon2026/LASAGNA/D1/2-Ozge Cinko.mp4"
    )
    assert (
        afternoon_event.video_uploaded_path
        == "conference-videos/pycon2026/LASAGNA/D1/4-Ozge Cinko.mp4"
    )
    assert admin.message_user.mock_calls[0].args[1] == "Matched 2 videos to events."
    assert admin.message_user.call_count == 1


def test_map_videos_page_hides_events_without_videos(rf, admin_user, mocker):
    render = mocker.patch("conferences.admin.conference.render")
    conference = ConferenceFactory()

    visible_titles = ["A nice talk", "A keynote", "A panel", "Lightning Talks"]
    hidden_titles = ["A training", "Registration", "Coffee break", "Recruiting Room"]

    for title, type in zip(
        visible_titles + hidden_titles,
        [
            ScheduleItem.TYPES.talk,
            ScheduleItem.TYPES.keynote,
            ScheduleItem.TYPES.panel,
            ScheduleItem.TYPES.custom,
            ScheduleItem.TYPES.training,
            ScheduleItem.TYPES.registration,
            "break",
            ScheduleItem.TYPES.recruiting,
        ],
    ):
        ScheduleItemFactory(
            conference=conference,
            title=title,
            type=type,
            submission=None,
        )

    admin = ConferenceAdmin(
        model=conference.__class__,
        admin_site=AdminSite(),
    )

    request = rf.get("/")
    request.user = admin_user
    admin.map_videos(request, conference.id)

    context = render.call_args.args[2]
    shown_titles = [event.title for event in context["events"]]
    assert sorted(shown_titles) == sorted(visible_titles)


def test_storage_walk_conference_videos_folder(mocker):
    mock_storage = mocker.Mock()
    mock_storage.listdir.side_effect = [
        (["test"], ["file1.txt", "file2.txt"]),
        ([""], ["file3.txt", "file4.txt"]),
    ]

    output = walk_conference_videos_folder(mock_storage, "")

    assert output == [
        "file1.txt",
        "file2.txt",
        "test/file3.txt",
        "test/file4.txt",
    ]


def test_save_manual_changes(
    rf,
    mocker,
):
    conference = ConferenceFactory(code="conf")

    event_1 = ScheduleItemFactory(
        conference=conference,
        title="Opening",
        type=ScheduleItem.TYPES.custom,
        submission=None,
    )
    event_2 = ScheduleItemFactory(
        conference=conference,
        title="Talk about something",
        type=ScheduleItem.TYPES.talk,
    )

    event_3 = ScheduleItemFactory(
        conference=conference,
        title="Talk about something",
        type=ScheduleItem.TYPES.talk,
        submission=None,
    )
    event_3.additional_speakers.add(ScheduleItemAdditionalSpeakerFactory())
    event_3.additional_speakers.add(ScheduleItemAdditionalSpeakerFactory())

    request = rf.post(
        "/",
        data={
            "manual_changes": "1",
            f"video_uploaded_path_{event_1.id}": "test",
            f"video_uploaded_path_{event_2.id}": "another-2",
            f"video_uploaded_path_{event_3.id}": "another-3",
        },
    )

    admin = ConferenceAdmin(
        model=conference.__class__,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()
    response = admin.map_videos(request, conference.id)

    assert response.status_code == 302

    event_1.refresh_from_db()
    event_2.refresh_from_db()
    event_3.refresh_from_db()

    assert event_1.video_uploaded_path == "test"
    assert event_2.video_uploaded_path == "another-2"
    assert event_3.video_uploaded_path == "another-3"
