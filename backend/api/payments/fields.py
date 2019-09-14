from django import forms


class CartField(forms.CharField):
    def to_python(self, value):
        return value
