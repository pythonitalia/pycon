from billing.exceptions import (
    FiscalCodeIncorrectLengthError,
    FiscalCodeInvalidCharsError,
    FiscalCodeInvalidControlCodeError,
    PartitaIvaIncorrectLengthError,
    PartitaIvaInvalidCharsError,
    PartitaIvaInvalidCodeError,
    SdiCodeIncorrectLengthError,
    SdiIncorrectDigitError,
    SdiInvalidCharsError,
    CapCodeIncorrectLengthError,
    CapCodeInvalidCharsError,
    CapCodeInvalidFirstDigitError,
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

    def char_to_value(char):
        if char.isalpha():
            return ord(char) - ord("A")

        return int(char) + 26

    sum_value = sum(char_to_value(sdi_code[i]) * (2 if i % 2 else 1) for i in range(6))
    expected_check_digit = chr((sum_value % 26) + ord("A"))

    if sdi_code[-1] != expected_check_digit:
        raise SdiIncorrectDigitError(expected_check_digit, sdi_code[-1])

    return True


def validate_cap_code(cap_code: str) -> bool:
    if len(cap_code) != 5:
        raise CapCodeIncorrectLengthError()

    if not cap_code.isnumeric():
        raise CapCodeInvalidCharsError()

    first_digit = int(cap_code[0])
    if not (0 <= first_digit <= 9):
        raise CapCodeInvalidFirstDigitError()

    return True


def validate_italian_partita_iva(partita_iva: str) -> bool:
    if len(partita_iva) != 11:
        raise PartitaIvaIncorrectLengthError()

    if not partita_iva.isdigit():
        raise PartitaIvaInvalidCharsError()

    digits = [int(d) for d in partita_iva]
    odd_sum = sum(digits[::2])
    even_sum = 0

    for digit in digits[1::2]:
        double_digit = digit * 2
        even_sum += (double_digit % 10) + (double_digit // 10)

    total = odd_sum + even_sum

    if not (10 - (total % 10)) % 10 == digits[-1]:
        raise PartitaIvaInvalidCodeError()

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
