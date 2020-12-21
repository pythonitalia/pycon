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
