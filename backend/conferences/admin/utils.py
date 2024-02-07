from unicodedata import normalize
import re


def cleanup_string(string: str) -> str:
    new_string = normalize(
        "NFKD", "".join(char for char in string if char.isprintable())
    ).lower()
    new_string = re.sub(r"\s+", " ", new_string)
    return new_string.strip()
