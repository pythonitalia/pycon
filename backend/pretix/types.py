from __future__ import annotations

from typing import TypedDict


class Locale(TypedDict):
    en: str
    it: str


class Quota(TypedDict):
    id: int
    available: bool
    available_number: int
    items: list[int]
    name: str
    size: int
    variations: list[int]


class Option(TypedDict):
    id: int
    answer: Locale


class Question(TypedDict):
    id: int
    items: list[int]
    question: Locale
    required: bool
    options: list[Option] | None
    answer: Answer | None


class Answer(TypedDict):
    answer: str
    options: list[int]
    question: Question


class Category(TypedDict):
    id: int
    name: str
    internal_name: str


class ProductVariation(TypedDict):
    id: int
    value: Locale
    description: Locale
    active: bool
    default_price: str


class Item(TypedDict):
    id: int
    name: Locale
    description: Locale
    tax_rate: str
    active: bool
    default_price: str
    available_from: str
    available_until: str
    category: Category
    variations: list[ProductVariation]
    questions: list[Question] | None


class OrderPosition(TypedDict):
    id: int
    attendee_name: str
    attendee_email: str
    item: Item
    answers: list[Answer]
