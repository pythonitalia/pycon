from typing import List, TypedDict


class Quota(TypedDict):
    id: int
    available: bool
    available_number: int
    items: List[int]
    name: str
    size: int
    variations: List[int]
