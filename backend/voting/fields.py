from django.forms import CharField


class VoteValueField(CharField):
    def to_python(self, value):
        return value
