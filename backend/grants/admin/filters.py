from django.contrib.admin import SimpleListFilter


class IsProposedSpeakerFilter(SimpleListFilter):
    title = "Is Proposed Speaker"
    parameter_name = "is_proposed_speaker"

    def lookups(self, request, model_admin):
        return (
            (True, "Yes"),
            (False, "No"),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(is_proposed_speaker=self.value())
        return queryset


class IsConfirmedSpeakerFilter(SimpleListFilter):
    title = "Is Confirmed Speaker"
    parameter_name = "is_confirmed_speaker"

    def lookups(self, request, model_admin):
        return (
            (True, "Yes"),
            (False, "No"),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(is_confirmed_speaker=self.value())
        return queryset
