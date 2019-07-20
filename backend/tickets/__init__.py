from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


QUESTION_TYPE_CHOICE = 'choice'
QUESTION_TYPE_TEXT = 'text'

QUESTION_TYPES = Choices(
    (QUESTION_TYPE_CHOICE, _('Option Choice')),
    (QUESTION_TYPE_TEXT, _('Free Text')),
)
