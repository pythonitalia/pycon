from django import forms
from django.contrib import admin
from i18n.forms import I18nTextarea, I18nTextInput

from .models import Page


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = "__all__"
        widgets = {
            "title": I18nTextInput,
            "slug": I18nTextInput,
            "content": I18nTextarea,
        }


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "slug")
    form = PageForm
