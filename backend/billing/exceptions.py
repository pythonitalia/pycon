class SdiValidationError(ValueError):
    ...


class SdiCodeIncorrectLengthError(SdiValidationError):
    def __str__(self):
        return "SDI code must be 7 characters long"


class SdiInvalidCharsError(SdiValidationError):
    def __str__(self):
        return "SDI code must contain only letters and digits"


class CapCodeValidationError(ValueError):
    ...


class CapCodeIncorrectLengthError(CapCodeValidationError):
    def __str__(self):
        return "CAP code must be 5 characters long"


class CapCodeInvalidCharsError(CapCodeValidationError):
    def __str__(self):
        return "CAP code must contain only digits"


class ItalianVatNumberValidationError(ValueError):
    ...


class ItalianVatNumberIncorrectLengthError(ItalianVatNumberValidationError):
    def __str__(self):
        return "VAT number must be 11 characters long"


class ItalianVatNumberInvalidCharsError(ItalianVatNumberValidationError):
    def __str__(self):
        return "VAT number must contain only digits"


class ItalianVatNumberInvalidCodeError(ItalianVatNumberValidationError):
    def __str__(self):
        return "Invalid VAT number"


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
