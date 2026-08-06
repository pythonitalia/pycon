from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from users.models import User


class Form(TimeStampedModel):
    class Purpose(models.TextChoices):
        GRANT = "grant", _("Grant")
        GENERIC = "generic", _("Generic")

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="forms",
    )
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.purpose}, {self.conference.name})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["conference", "purpose"],
                condition=~models.Q(purpose="generic"),
                name="unique_form_per_conference_and_purpose",
            )
        ]


class FormQuestion(TimeStampedModel):
    class QuestionType(models.TextChoices):
        TEXT = "text", _("Text")
        TEXTAREA = "textarea", _("Textarea")
        SELECT = "select", _("Select")
        MULTI_SELECT = "multi_select", _("Multi select")
        BOOLEAN = "boolean", _("Boolean")
        URL = "url", _("URL")

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    label = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    question_type = models.CharField(max_length=32, choices=QuestionType.choices)
    # list of {"id": "vegan", "label": "Vegan"}; only for select/multi_select
    options = models.JSONField(blank=True, default=list)
    required = models.BooleanField(default=False)
    max_length = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    # Fields that define what an answer means; frozen once any answer exists
    # so stored answers always match their questions. label/description/order/
    # active stay editable (deactivate instead of delete).
    FROZEN_FIELDS = ("form_id", "question_type", "options", "required")

    def clean(self):
        super().clean()
        self._check_frozen_fields()

    def save(self, *args, **kwargs):
        self._check_frozen_fields()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.form.answers.exists():
            raise ValidationError(
                "This question cannot be deleted because the form already has "
                "answers. Deactivate it instead."
            )
        return super().delete(*args, **kwargs)

    def _check_frozen_fields(self):
        if not self.pk:
            return

        stored = FormQuestion.objects.get(pk=self.pk)
        changed = [
            field
            for field in self.FROZEN_FIELDS
            if getattr(stored, field) != getattr(self, field)
        ]
        if changed and stored.form.answers.exists():
            fields = ", ".join(field.removesuffix("_id") for field in changed)
            raise ValidationError(
                f"The form already has answers; these fields cannot be "
                f"changed: {fields}. Add a new question or deactivate this "
                f"one instead."
            )

    def __str__(self):
        return self.label

    class Meta:
        ordering = ["order", "id"]


class FormAnswer(TimeStampedModel):
    form = models.ForeignKey(
        Form,
        on_delete=models.PROTECT,
        related_name="answers",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="form_answers",
    )
    # versioned envelope: {"version": 1, "answers": {"<question_pk>": value}}
    # value types (version 1): text/textarea/url -> str, select -> option id,
    # multi_select -> list of option ids, boolean -> bool
    answers = models.JSONField(default=dict)

    def __str__(self):
        return f"Answers of {self.user_id} to {self.form_id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["form", "user"],
                name="unique_form_answer_per_user",
            )
        ]
