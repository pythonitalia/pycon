# from hotels.admin import HotelRoomReservationAdmin
# from hotels.models import HotelRoomReservation
from pytest import mark


@mark.django_db
@mark.parametrize(
    "code", [("n", "Pending"), ("p", "Paid"), ("e", "Expired"), ("c", "Canceled")]
)
def test_admin_order_status(code, mocker):
    # obj = HotelRoomReservation(pretix_order_code="A")
    # admin = HotelRoomReservationAdmin(HotelRoomReservation)
    # admin.order_status()
    pass
