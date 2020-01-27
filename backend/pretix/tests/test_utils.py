from pretix.utils import order_status_to_text
from pytest import mark


@mark.parametrize(
    "code", [("n", "Pending"), ("p", "Paid"), ("e", "Expired"), ("c", "Canceled")]
)
def convert_code_to_text(code):
    assert order_status_to_text(code[0]) == code[1]
