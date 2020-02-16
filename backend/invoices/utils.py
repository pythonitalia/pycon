import zipfile
from io import BytesIO

from django.utils.deconstruct import deconstructible
from jsonschema import validate
from lxml import etree

PRODUCT_SUMMARY_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "row": {"type": "integer"},
                "description": {"type": "string"},
                "quantity": {"type": "number"},
                "unit_price": {"type": "number"},
                "total_price": {"type": "number"},
                "vat_rate": {"type": "number"},
            },
            "required": [
                "row",
                "description",
                "quantity",
                "unit_price",
                "total_price",
                "vat_rate",
            ],
        }
    ],
}


@deconstructible
class JSONSchemaValidator:
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, value):
        validate(value, self.schema)

    def __eq__(self, other):
        return self.schema == other.schema


def zip_files(files):
    outfile = BytesIO()
    with zipfile.ZipFile(outfile, "w") as zf:
        for file in files:
            zf.writestr(file[0], file[1])
    return outfile.getvalue()


def xml_to_string(xml):
    return etree.tostring(xml, pretty_print=True).decode("utf-8")
