from django.utils.translation import gettext_lazy as _
from model_utils import Choices

GENDERS = Choices(
    ("male", _("Male")),
    ("female", _("Female")),
    ("other", _("Other")),
    ("not_say", _("Prefer not to say")),
)
