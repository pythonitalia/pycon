from dal import autocomplete
from django.db.models import Q

from .models import User


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(
                Q(name__istartswith=self.q)
                | Q(full_name__istartswith=self.q)
                | Q(email=self.q)
            )

        return qs
