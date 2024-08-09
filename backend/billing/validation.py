from billing.exceptions import (
    FiscalCodeIncorrectLengthError,
    FiscalCodeInvalidCharsError,
    FiscalCodeInvalidControlCodeError,
    ItalianVatNumberIncorrectLengthError,
    ItalianVatNumberInvalidCharsError,
    ItalianVatNumberInvalidCodeError,
    SdiCodeIncorrectLengthError,
    SdiInvalidCharsError,
    ItalianZipCodeIncorrectLengthError,
    ItalianZipCodeInvalidCharsError,
)
from billing.constants import (
    ITALIAN_FISCAL_CODE_CONTROL_CODE,
    ITALIAN_FISCAL_CODE_EVEN_VALUES,
    ITALIAN_FISCAL_CODE_ODD_VALUES,
)


def validate_sdi_code(sdi_code: str) -> bool:
    sdi_code = sdi_code.upper()

    if len(sdi_code) != 7:
        raise SdiCodeIncorrectLengthError()

    if not sdi_code.isalnum():
        raise SdiInvalidCharsError()

    return True


def validate_italian_zip_code(zip_code: str) -> bool:
    if len(zip_code) != 5:
        raise ItalianZipCodeIncorrectLengthError()

    if not zip_code.isnumeric():
        raise ItalianZipCodeInvalidCharsError()

    return True


def validate_italian_vat_number(vat_number: str) -> bool:
    if vat_number.startswith("IT"):
        vat_number = vat_number[2:]

    if len(vat_number) != 11:
        raise ItalianVatNumberIncorrectLengthError()

    if not vat_number.isdigit():
        raise ItalianVatNumberInvalidCharsError()

    total = 0
    for i, digit in enumerate(vat_number[:10]):
        n = int(digit)
        if i % 2 == 0:
            total += n
        else:
            n *= 2
            total += n if n < 10 else n - 9

    check = (10 - (total % 10)) % 10

    if check != int(vat_number[-1]):
        raise ItalianVatNumberInvalidCodeError()

    return True


def validate_fiscal_code(fiscal_code: str) -> bool:
    fiscal_code = fiscal_code.upper()

    if len(fiscal_code) != 16:
        raise FiscalCodeIncorrectLengthError()

    if not fiscal_code.isalnum():
        raise FiscalCodeInvalidCharsError()

    sum_odd = sum(
        ITALIAN_FISCAL_CODE_ODD_VALUES[fiscal_code[i]] for i in range(0, 15, 2)
    )
    sum_even = sum(
        ITALIAN_FISCAL_CODE_EVEN_VALUES[fiscal_code[i]] for i in range(1, 15, 2)
    )

    total_sum = sum_odd + sum_even
    check_char = ITALIAN_FISCAL_CODE_CONTROL_CODE[total_sum % 26]

    if check_char != fiscal_code[-1]:
        raise FiscalCodeInvalidControlCodeError()

    return True
