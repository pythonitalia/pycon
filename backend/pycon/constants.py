import zoneinfo
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

COLORS = Choices(
    ("blue", _("blue")),
    ("yellow", _("yellow")),
    ("orange", _("orange")),
    ("cinderella", _("cinderella")),
    ("violet", _("violet")),
    ("green", _("green")),
)

KB = 1024
MB = 1024 * KB
GB = 1024 * MB

UTC = zoneinfo.ZoneInfo("UTC")
