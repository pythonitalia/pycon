class SdiValidationError(ValueError):
    ...


class SdiCodeIncorrectLengthError(SdiValidationError):
    def __str__(self):
        return "SDI code must be 7 characters long"


class SdiInvalidCharsError(SdiValidationError):
    def __str__(self):
        return "SDI code must contain only letters and digits"


class SdiIncorrectDigitError(SdiValidationError):
    expected: str
    got: str

    def __init__(self, expected: str, got: str):
        self.expected = expected
        self.got = got

    def __str__(self):
        return "Invalid SDI code"


class CapCodeValidationError(ValueError):
    ...


class CapCodeIncorrectLengthError(CapCodeValidationError):
    def __str__(self):
        return "CAP code must be 5 characters long"


class CapCodeInvalidCharsError(CapCodeValidationError):
    def __str__(self):
        return "CAP code must contain only digits"


class CapCodeInvalidFirstDigitError(CapCodeValidationError):
    def __str__(self):
        return "First digit of CAP code must be between 0 and 9"


class PartitaIvaValidationError(ValueError):
    ...


class PartitaIvaIncorrectLengthError(PartitaIvaValidationError):
    def __str__(self):
        return "Partita IVA must be 11 characters long"


class PartitaIvaInvalidCharsError(PartitaIvaValidationError):
    def __str__(self):
        return "Partita IVA must contain only digits"


class PartitaIvaInvalidCodeError(PartitaIvaValidationError):
    def __str__(self):
        return "Invalid Partita IVA code"


class FiscalCodeValidationError(ValueError):
    ...


class FiscalCodeIncorrectLengthError(FiscalCodeValidationError):
    def __str__(self):
        return "Fiscal code must be 16 characters long"


class FiscalCodeInvalidCharsError(FiscalCodeValidationError):
    def __str__(self):
        return "Fiscal code must contain only letters and digits"


class FiscalCodeInvalidControlCodeError(FiscalCodeValidationError):
    def __str__(self):
        return "Invalid fiscal code"
