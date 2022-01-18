from typing import Any

from django.contrib import admin

from users.client import get_user_data_by_query, get_users_data_by_ids


class AdminUsersMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        users_ids = queryset.values_list(self.user_fk, flat=True)
        self._PREFETCHED_USERS_BY_ID = get_users_data_by_ids(list(users_ids))
        return queryset

    def get_user_display_name(self, obj_id: Any) -> str:
        return self.get_user_data(obj_id)["displayName"]

    def get_user_data(self, obj_id: Any) -> dict[str, Any]:
        return self._PREFETCHED_USERS_BY_ID[str(obj_id)]


class SearchUsersMixin(admin.ModelAdmin):
    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        speaker_ids = get_user_data_by_query(search_term)

        queryset |= self.model.objects.filter(**{f"{self.user_fk}__in": speaker_ids})
        return queryset, may_have_duplicates
