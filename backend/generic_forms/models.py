from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
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

    # Frozen once any answer exists: moving a form to another conference or
    # purpose would re-contextualize the stored answers.
    FROZEN_FIELDS = ("conference_id", "purpose")

    def save(self, *args, **kwargs):
        self._check_frozen_fields()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self._check_frozen_fields()

    def _check_frozen_fields(self):
        if self._state.adding:
            return

        stored = Form.objects.filter(pk=self.pk).first()
        if stored is None:
            return

        changed = [
            field
            for field in self.FROZEN_FIELDS
            if getattr(stored, field) != getattr(self, field)
        ]
        if changed and stored.answers.exists():
            fields = ", ".join(field.removesuffix("_id") for field in changed)
            raise ValidationError(
                f"The form already has answers; these fields cannot be "
                f"changed: {fields}."
            )

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


def _is_valid_option(option) -> bool:
    return (
        isinstance(option, dict)
        and isinstance(option.get("id"), str)
        and option["id"] != ""
        and isinstance(option.get("label"), str)
        and option["label"] != ""
    )


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
    # Enforced in save()/clean() and a pre_delete signal: QuerySet.update()
    # and bulk_update() bypass both, so they must never be used on this model.
    # The exists()-then-write window is not locked; a first answer racing an
    # edit is accepted as a non-issue at this scale.
    FROZEN_FIELDS = ("form_id", "question_type", "options", "required")
    CHOICE_TYPES = (QuestionType.SELECT, QuestionType.MULTI_SELECT)

    def clean(self):
        super().clean()
        self._validate_options()
        self._check_frozen_fields()

    def save(self, *args, **kwargs):
        self._validate_options()
        self._check_frozen_fields()
        super().save(*args, **kwargs)

    def _validate_options(self):
        if self.question_type not in self.CHOICE_TYPES:
            if self.options:
                raise ValidationError(
                    {"options": "Only select questions can have options."}
                )
            return

        if not isinstance(self.options, list) or not self.options:
            raise ValidationError(
                {"options": "Select questions need a non-empty list of options."}
            )

        if not all(_is_valid_option(option) for option in self.options):
            raise ValidationError(
                {
                    "options": 'Every option must be {"id": "...", '
                    '"label": "..."} with non-empty strings.'
                }
            )

        ids = [option["id"] for option in self.options]
        if len(ids) != len(set(ids)):
            raise ValidationError({"options": "Option ids must be unique."})

    def _check_frozen_fields(self):
        if self._state.adding:
            return

        stored = FormQuestion.objects.filter(pk=self.pk).first()
        if stored is None:
            return

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


# pre_delete (not FormQuestion.delete) so QuerySet.delete() and cascades are
# guarded too. Forms with answers cannot cascade here: FormAnswer.form is
# PROTECT, so only questions of unanswered forms ever reach deletion.
@receiver(pre_delete, sender=FormQuestion)
def block_deleting_answered_questions(sender, instance, **kwargs):
    if instance.form.answers.exists():
        raise ValidationError(
            "This question cannot be deleted because the form already has "
            "answers. Deactivate it instead."
        )
