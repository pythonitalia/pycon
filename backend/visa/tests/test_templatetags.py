from visa.templatetags.invitation_letter_asset import invitation_letter_asset
from visa.tests.factories import InvitationLetterAssetFactory
import pytest

pytestmark = pytest.mark.django_db


def test_invitation_letter_asset():
    asset = InvitationLetterAssetFactory(identifier="test")

    output = invitation_letter_asset(
        {"config": asset.invitation_letter_conference_config},
        "test",
        width="60px",
        height="60px",
    )

    assert output == f'<img src="{asset.image.url}" style="width: 60px;height: 60px" />'

    output = invitation_letter_asset(
        {"config": asset.invitation_letter_conference_config}, "test", width="60px"
    )

    assert output == f'<img src="{asset.image.url}" style="width: 60px" />'

    output = invitation_letter_asset(
        {"config": asset.invitation_letter_conference_config}, "test", height="60px"
    )

    assert output == f'<img src="{asset.image.url}" style="height: 60px" />'

    output = invitation_letter_asset(
        {"config": asset.invitation_letter_conference_config}, "test"
    )

    assert output == f'<img src="{asset.image.url}" style="" />'


def test_invitation_letter_asset_invalid():
    asset = InvitationLetterAssetFactory(identifier="test")

    with pytest.raises(AssertionError, match="No asset found with identifier invalid"):
        invitation_letter_asset(
            {"config": asset.invitation_letter_conference_config}, "invalid"
        )
