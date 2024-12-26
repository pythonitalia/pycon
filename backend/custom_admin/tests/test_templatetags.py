from custom_admin.templatetags.to_json_for_prop import to_json_for_prop
from custom_admin.templatetags.empty_string_if_none import empty_string_if_none


def test_empty_string_if_none():
    assert empty_string_if_none("") == ""
    assert empty_string_if_none(None) == ""
    assert empty_string_if_none("value") == "value"


def test_to_json_for_prop():
    assert to_json_for_prop({"a": 123}) == "{\\u0022a\\u0022: 123}"
