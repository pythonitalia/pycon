import zipfile
from io import BytesIO

from lxml import etree


def zip_files(files):  # pragma: no cover
    outfile = BytesIO()
    with zipfile.ZipFile(outfile, "w") as zf:
        for file in files:
            zf.writestr(file[0], file[1])
    return outfile.getvalue()


def xml_to_string(xml):  # pragma: no cover
    return etree.tostring(xml, pretty_print=True).decode("utf-8")
