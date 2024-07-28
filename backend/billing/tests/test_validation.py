from billing.exceptions import (
    CapCodeIncorrectLengthError,
    CapCodeInvalidCharsError,
    FiscalCodeIncorrectLengthError,
    FiscalCodeInvalidCharsError,
    FiscalCodeInvalidControlCodeError,
    SdiCodeIncorrectLengthError,
    SdiInvalidCharsError,
)
import pytest
from billing.validation import (
    validate_cap_code,
    validate_fiscal_code,
    validate_sdi_code,
)


def test_validate_sdi_code_with_valid_code():
    assert validate_sdi_code("6EXQA6Q")


@pytest.mark.parametrize(
    "code",
    [
        "1",
        "99",
        "123456789",
    ],
)
def test_validate_sdi_code_length(code):
    with pytest.raises(SdiCodeIncorrectLengthError):
        validate_sdi_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "___aa__",
        "$$$$$$$",
        "aa_aaa_",
    ],
)
def test_validate_sdi_code_invalid_chars(code):
    with pytest.raises(SdiInvalidCharsError):
        validate_sdi_code(code)


def test_validate_cap_code_with_valid_code():
    assert validate_cap_code("50121")
    assert validate_cap_code("40127")
    assert validate_cap_code("93100")


@pytest.mark.parametrize(
    "code",
    [
        "0",
        "11111111111",
        "123",
    ],
)
def test_validate_cap_code_with_incorrect_length(code):
    with pytest.raises(CapCodeIncorrectLengthError):
        validate_cap_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "ababc",
        "$)£_£",
        "4fdsf",
        "f9449",
    ],
)
def test_validate_cap_code_with_non_numeric_code(code):
    with pytest.raises(CapCodeInvalidCharsError):
        validate_cap_code(code)


def test_validate_fiscal_code_with_valid_code():
    assert validate_fiscal_code("DOEJHN80A01D612J")
    assert validate_fiscal_code("FRNGNN17M62B856J")


@pytest.mark.parametrize(
    "code",
    [
        "FRNGNN17M62B856C",
        "FRNGNN29M62B856C",
        "FRNGNN55F62B856C",
        "FRNGNN55F62A856C",
        "NCNGNN55M62A856A",
        "NCNGAA55M62A856A",
    ],
)
def test_validate_fiscal_code_with_incorrect_codes(code):
    with pytest.raises(FiscalCodeInvalidControlCodeError):
        validate_fiscal_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "FRNGNN17M",
        "FRNGNN29MAAAAAAAAAAAA",
        "F",
        "FAAAAAAAAAAAAAAAAAAAA",
        "",
    ],
)
def test_validate_fiscal_code_with_incorrect_length(code):
    with pytest.raises(FiscalCodeIncorrectLengthError):
        validate_fiscal_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "NCNGNN55M62A856$",
        "________________",
        "@_@______@__._¢_",
    ],
)
def test_validate_fiscal_code_only_allows_letters_and_numbers(code):
    with pytest.raises(FiscalCodeInvalidCharsError):
        validate_fiscal_code(code)
