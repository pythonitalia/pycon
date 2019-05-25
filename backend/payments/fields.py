from django import forms



class CartItemField(forms.CharField):
    def to_python(self, value):
        return value


class CartField(forms.CharField):
    def to_python(self, value):
        return value
