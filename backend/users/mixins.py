from typing import Any

from django.contrib import admin

from users.client import get_users_data_by_ids


class AdminUsersMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        users_ids = queryset.values_list(self.user_fk, flat=True)
        self._PREFETCHED_USERS_BY_ID = get_users_data_by_ids(list(users_ids))
        return queryset

    def get_user_display_name(self, obj_id: Any) -> str:
        return self._PREFETCHED_USERS_BY_ID[str(obj_id)]["displayName"]
