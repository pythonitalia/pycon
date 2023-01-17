from typing import Any

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.resources import ModelResource

from users.client import get_user_data_by_query, get_users_data_by_ids


class UserMixin:
    user_fk = None
    _PREFETCHED_USERS_BY_ID = {}

    def get_users_by_ids(self, queryset):
        users_ids = queryset.filter(
            **{
                f"{self.user_fk}__isnull": False,
            }
        ).values_list(self.user_fk, flat=True)
        self._PREFETCHED_USERS_BY_ID = get_users_data_by_ids(list(users_ids))
        return queryset

    def get_user_display_name(self, obj_id: Any) -> str:
        user = self.get_user_data(obj_id)

        if not user:
            return _("<no user found>")

        return user["displayName"]

    def get_user_data(self, obj_id: Any) -> dict[str, Any]:
        return self._PREFETCHED_USERS_BY_ID.get(str(obj_id), None)


class AdminUsersMixin(admin.ModelAdmin, UserMixin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        self.get_users_by_ids(queryset)
        return queryset


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


class ResourceUsersMixin(ModelResource, UserMixin):
    def before_export(self, queryset, *args, **kwargs):
        self.get_users_by_ids(queryset)
        return queryset


class ResourceUsersByIdsMixin(ModelResource, UserMixin):
    search_field = None
    _PREFETCHED_USERS_BY_ID = {}

    def before_export(self, queryset, *args, **kwargs):
        emails = queryset.values_list(self.search_field, flat=True)
        self._PREFETCHED_USERS_BY_ID = get_users_data_by_ids(list(emails))
        return queryset
