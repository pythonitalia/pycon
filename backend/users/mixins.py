from typing import Any, Type

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.utils.translation import gettext_lazy as _
from import_export.resources import ModelResource

from users.client import get_user_data_by_query, get_users_data_by_ids


class UserMixin:
    user_fk = None
    _PREFETCHED_USERS_BY_ID = {}

    def get_users_by_ids(self, queryset):
        # todo use := once we are on a newer python version
        users_ids = [
            getattr(obj, self.user_fk, None)
            for obj in queryset
            if getattr(obj, self.user_fk, None)
        ]
        self._PREFETCHED_USERS_BY_ID = get_users_data_by_ids(users_ids)
        return queryset

    def get_user_display_name(self, obj_id: Any) -> str:
        user = self.get_user_data(obj_id)

        if not user:
            return _("<no user found>")

        return user["displayName"]

    def get_user_data(self, obj_id: Any) -> dict[str, Any]:
        return self._PREFETCHED_USERS_BY_ID.get(str(obj_id), None)


class AdminUsersChangeList(ChangeList):
    def get_results(self, request) -> None:
        super().get_results(request)
        self.model_admin.get_users_by_ids(self.result_list)


class AdminUsersMixin(admin.ModelAdmin, UserMixin):
    def get_changelist(self, request, **kwargs: Any) -> Type[ChangeList]:
        return AdminUsersChangeList


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
