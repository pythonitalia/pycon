from conferences.models.conference_voucher import ConferenceVoucher
from conferences.models.conference import Conference
from users.models import User
from pretix import create_voucher


def create_conference_voucher(
    *,
    conference: Conference,
    user: User,
    voucher_type: ConferenceVoucher.VoucherType,
) -> ConferenceVoucher:
    conference_voucher = ConferenceVoucher(
        conference=conference,
        user=user,
        voucher_type=voucher_type,
        voucher_code=ConferenceVoucher.generate_code(),
    )

    price_mode, value = conference_voucher.get_voucher_configuration()

    pretix_voucher = create_voucher(
        conference=conference_voucher.conference,
        code=conference_voucher.voucher_code,
        comment=f"Voucher for user_id={conference_voucher.user_id}",
        tag=conference_voucher.voucher_type,
        quota_id=conference_voucher.conference.pretix_conference_voucher_quota_id,
        price_mode=price_mode,
        value=value,
    )

    pretix_voucher_id = pretix_voucher["id"]
    conference_voucher.pretix_voucher_id = pretix_voucher_id
    conference_voucher.save()
    return conference_voucher
