from i18n.strings import LazyI18nString

from schedule.models import ScheduleItem
from schedule.tests.factories import (
    ScheduleItemFactory,
)
import pytest
from schedule.video_upload import create_video_info


pytestmark = pytest.mark.django_db

VIDEO_TITLE_TEMPLATE = """
{% if has_zero_or_more_than_2_speakers %}
{{title}} - {{conference_name}}
{% else %}
{{title}} - {{speakers_names}}
{% endif %}
"""
VIDEO_DESCRIPTION_TEMPLATE = """
{% if has_zero_or_more_than_2_speakers %}
{{title}} - {{conference_name}}
{% else %}
{{title}} - {{speakers_names}} - {{conference_name}}
{% endif %}

{% if elevator_pitch %}
Elevator Pitch:
{{elevator_pitch}}
{% endif %}

{% if abstract %}
Description:
{{abstract}}
{% endif %}

{{hashtags}}
"""


def test_create_video_info_case1():
    schedule_item = ScheduleItemFactory(
        conference__name=LazyI18nString({"en": "Conf Name", "it": "Conf Name"}),
        type=ScheduleItem.TYPES.talk,
        submission=None,
        title="Schedule Item Title",
        description="Schedule Item Description",
        conference__video_title_template=VIDEO_TITLE_TEMPLATE,
        conference__video_description_template=VIDEO_DESCRIPTION_TEMPLATE,
    )

    output = create_video_info(schedule_item)

    assert output.title == "Schedule Item Title - Conf Name"
    assert (
        output.description
        == """Schedule Item Title - Conf Name

Description:
Schedule Item Description"""
    )


def test_create_video_info_case2_with_elevator_pitch_and_abstract():
    schedule_item = ScheduleItemFactory(
        conference__name=LazyI18nString({"en": "Conf Name", "it": "Conf Name"}),
        type=ScheduleItem.TYPES.talk,
        submission__abstract=LazyI18nString({"en": "Abstract", "it": "Abstract"}),
        submission__speaker__full_name="SpeakerName",
        submission__elevator_pitch=LazyI18nString(
            {"en": "Elevator Pitch", "it": "Elevator Pitch"}
        ),
        title="Schedule Item Title",
        description="Schedule Item Description",
        conference__video_title_template=VIDEO_TITLE_TEMPLATE,
        conference__video_description_template=VIDEO_DESCRIPTION_TEMPLATE,
    )

    output = create_video_info(schedule_item)

    assert output.title == "Schedule Item Title - SpeakerName"
    assert (
        output.description
        == """Schedule Item Title - SpeakerName - Conf Name

Elevator Pitch:
Elevator Pitch

Description:
Abstract"""
    )


def test_create_video_info_case3_with_tags():
    schedule_item = ScheduleItemFactory(
        conference__name=LazyI18nString({"en": "Conf Name", "it": "Conf Name"}),
        type=ScheduleItem.TYPES.talk,
        submission__abstract=LazyI18nString({"en": "Abstract", "it": "Abstract"}),
        submission__speaker__full_name="SpeakerName",
        submission__elevator_pitch=LazyI18nString(
            {"en": "Elevator Pitch", "it": "Elevator Pitch"}
        ),
        submission__tags=["django", "php"],
        title="Schedule Item Title",
        description="Schedule Item Description",
        conference__video_title_template=VIDEO_TITLE_TEMPLATE,
        conference__video_description_template=VIDEO_DESCRIPTION_TEMPLATE,
    )

    output = create_video_info(schedule_item)

    assert output.title == "Schedule Item Title - SpeakerName"
    assert (
        output.description
        == """Schedule Item Title - SpeakerName - Conf Name

Elevator Pitch:
Elevator Pitch

Description:
Abstract

#django #php"""
    )


def test_create_video_info_with_long_title_fallbacks_to_schedule_item_title():
    schedule_item = ScheduleItemFactory(
        conference__name=LazyI18nString({"en": "Conf Name", "it": "Conf Name"}),
        type=ScheduleItem.TYPES.talk,
        submission__abstract=LazyI18nString({"en": "Abstract", "it": "Abstract"}),
        submission__speaker__full_name="SpeakerName",
        submission__elevator_pitch=LazyI18nString(
            {"en": "Elevator Pitch", "it": "Elevator Pitch"}
        ),
        title="I am a very long title, in fact I am so long that I am long, almost 100 chars! Stop me, really! No",
        description="Schedule Item Description",
        conference__video_title_template=VIDEO_TITLE_TEMPLATE,
        conference__video_description_template=VIDEO_DESCRIPTION_TEMPLATE,
    )

    output = create_video_info(schedule_item)

    assert (
        output.title
        == "I am a very long title, in fact I am so long that I am long, almost 100 chars! Stop me, really! No"
    )
    assert (
        output.description
        == """I am a very long title, in fact I am so long that I am long, almost 100 chars! Stop me, really! No - SpeakerName - Conf Name

Elevator Pitch:
Elevator Pitch

Description:
Abstract"""
    )


def test_create_video_info_special_chars_are_replaced():
    schedule_item = ScheduleItemFactory(
        conference__name=LazyI18nString({"en": "Conf Name", "it": "Conf Name"}),
        type=ScheduleItem.TYPES.talk,
        submission=None,
        title="This is an <html/> talk!",
        description="We like to <<talk>> about HTML.",
        conference__video_title_template="{{title}}",
        conference__video_description_template="{{abstract}}",
    )

    output = create_video_info(schedule_item)

    assert output.title == "This is an \u1438html/\u1433 talk!"
    assert output.description == "We like to \u1438\u1438talk\u1433\u1433 about HTML."


def test_create_video_info_tags():
    schedule_item = ScheduleItemFactory(
        conference__name=LazyI18nString({"en": "Conf Name", "it": "Conf Name"}),
        type=ScheduleItem.TYPES.talk,
        submission__abstract=LazyI18nString({"en": "Abstract", "it": "Abstract"}),
        submission__speaker__full_name="SpeakerName",
        submission__tags=["Django Girls", "tag2", "php-5.3"],
        title="Schedule Item Title",
        description="Schedule Item Description",
        conference__video_title_template=VIDEO_TITLE_TEMPLATE,
        conference__video_description_template=VIDEO_DESCRIPTION_TEMPLATE,
    )

    output = create_video_info(schedule_item)

    assert output.tags == ["DjangoGirls", "tag2", "php53"]
    assert output.tags_as_str == "DjangoGirls,tag2,php53"
