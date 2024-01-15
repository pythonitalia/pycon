class ConferencePermissionMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser or request.user.admin_all_conferences:
            return queryset

        return queryset.filter(
            conference_id__in=request.user.admin_conferences.values_list(
                "id", flat=True
            )
        )
