from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

COLORS = Choices(
    ("blue", _("blue")),
    ("yellow", _("yellow")),
    ("orange", _("orange")),
    ("cindarella", _("cindarella")),
    ("violet", _("violet")),
    ("green", _("green")),
)
