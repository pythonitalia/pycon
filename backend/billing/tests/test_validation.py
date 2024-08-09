from billing.exceptions import (
    ItalianZipCodeIncorrectLengthError,
    ItalianZipCodeInvalidCharsError,
    FiscalCodeIncorrectLengthError,
    FiscalCodeInvalidCharsError,
    FiscalCodeInvalidControlCodeError,
    ItalianVatNumberIncorrectLengthError,
    ItalianVatNumberInvalidCharsError,
    ItalianVatNumberInvalidCodeError,
    SdiCodeIncorrectLengthError,
    SdiInvalidCharsError,
)
import pytest
from billing.validation import (
    validate_italian_zip_code,
    validate_fiscal_code,
    validate_italian_vat_number,
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


@pytest.mark.parametrize(
    "code",
    [
        "50121",
        "40127",
        "93100",
    ],
)
def test_validate_italian_zip_code_with_valid_code(code):
    assert validate_italian_zip_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "0",
        "11111111111",
        "123",
    ],
)
def test_validate_italian_zip_code_with_incorrect_length(code):
    with pytest.raises(ItalianZipCodeIncorrectLengthError):
        validate_italian_zip_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "ababc",
        "$)£_£",
        "4fdsf",
        "f9449",
    ],
)
def test_validate_italian_zip_code_with_non_numeric_code(code):
    with pytest.raises(ItalianZipCodeInvalidCharsError):
        validate_italian_zip_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "DOEJHN80A01D612J",
        "FRNGNN17M62B856J",
    ],
)
def test_validate_fiscal_code_with_valid_code(code):
    assert validate_fiscal_code(code)


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


@pytest.mark.parametrize(
    "code",
    ["IT00743110157", "00000000000", "44444444440"],
)
def test_validate_italian_vat_number_with_valid_code(code):
    assert validate_italian_vat_number(code)


@pytest.mark.parametrize(
    "code",
    ["11111", "111333333", "IT1111"],
)
def test_validate_italian_vat_number_with_invalid_length(code):
    with pytest.raises(ItalianVatNumberIncorrectLengthError):
        validate_italian_vat_number(code)


@pytest.mark.parametrize(
    "code",
    ["IT11HHHAAA000", "IT994JJAAAEEE", "9394393AX$@"],
)
def test_validate_italian_vat_number_with_invalid_chars(code):
    with pytest.raises(ItalianVatNumberInvalidCharsError):
        validate_italian_vat_number(code)


@pytest.mark.parametrize(
    "code",
    ["IT00743110151", "00000000001"],
)
def test_validate_italian_vat_number_with_invalid_check_digit(code):
    with pytest.raises(ItalianVatNumberInvalidCodeError):
        validate_italian_vat_number(code)
