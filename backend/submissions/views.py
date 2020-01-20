from dal import autocomplete

from .models import Submission


class SubmissionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Submission.objects.none()

        qs = Submission.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs
