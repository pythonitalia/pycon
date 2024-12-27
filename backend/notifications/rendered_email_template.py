from typing import TYPE_CHECKING
from dataclasses import dataclass
from functools import cached_property
from django.utils.safestring import mark_safe
from notifications.template_utils import render_template_from_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags

if TYPE_CHECKING:
    from notifications.models import EmailTemplate


@dataclass
class RenderedEmailTemplate:
    email_template: "EmailTemplate"
    placeholders: dict
    show_placeholders: bool

    def __post_init__(self):
        self.placeholders = self.placeholders or {}

    @property
    def all_placeholders(self):
        return {
            "conference": self.email_template.conference,
            **self.placeholders,
        }

    @cached_property
    def subject(self):
        return self.render_text(self.email_template.subject)

    @cached_property
    def preview_text(self):
        return self.render_text(self.email_template.preview_text)

    @cached_property
    def body(self):
        return self.render_text(self.email_template.body)

    @cached_property
    def html_body(self):
        return render_to_string(
            "notifications/email-template.html",
            {
                **self.all_placeholders,
                "subject": self.subject,
                "preview_text": self.preview_text,
                "body": self.body,
            },
        )

    @cached_property
    def text_body(self):
        return strip_tags(self.body)

    def render_text(self, text: str) -> str:
        return mark_safe(
            render_template_from_string(
                text, self.all_placeholders, show_placeholders=self.show_placeholders
            )
        )
