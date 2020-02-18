from typing import Any, Dict, List, Union

from mypy_extensions import TypedDict

ProductSummary = TypedDict(
    "ProductSummary",
    {
        "row": int,
        "description": str,
        "quantity": float,
        "unit_price": float,
        "total_price": float,
        "vat_rate": float,
    },
)

# nested recursive types are not supported in MYPY
XMLDict = Dict[str, Union[str, int, List[Any], Any]]
