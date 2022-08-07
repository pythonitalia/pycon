from api.forms import ContextAwareModelForm, HashidModelChoiceField
from domain_events.publisher import notify_new_comment_on_submission
from submissions.models import Submission, SubmissionComment


class SendSubmissionCommentForm(ContextAwareModelForm):
    submission = HashidModelChoiceField(queryset=Submission.objects.all())

    def save(self, commit=True):
        request = self.context.request
        self.instance.author_id = self.context.request.user.id
        comment = super().save(commit=commit)

        notify_new_comment_on_submission(
            comment,
            request,
        )

        return comment

    class Meta:
        model = SubmissionComment
        fields = ("text", "submission")
