from decimal import Decimal
from typing import Dict, List

import unidecode
from lxml import etree

from .types import XMLDict


def _split_tags(tag_name: str, text: bytes) -> List[etree._Element]:
    tags: List[etree._Element] = []

    size = 200

    chunks = [text[y - size : y] for y in range(size, len(text) + size, size)]

    for value in chunks:
        tag = etree.Element(tag_name)
        tag.text = value
        tags.append(tag)

    return tags


def dict_to_xml(dict: XMLDict):
    tags: List[etree._Element] = []

    for key, value in dict.items():
        # skip empty value

        if not value:
            continue

        if isinstance(value, (Dict, List)):
            if not isinstance(value, List):
                value = [value]

            for item in value:
                tag = etree.Element(key)

                for subtag in dict_to_xml(item):
                    tag.append(subtag)

                tags.append(tag)
        else:
            if isinstance(value, (int, float, Decimal)):
                value = str(value)

            value = unidecode.unidecode(value).encode("latin_1")

            for tag in _split_tags(key, value):
                tags.append(tag)

    return tags


def format_price(value):
    return "{:.2f}".format(value)
