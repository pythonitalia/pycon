from typing import Any

from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource

from conferences.models.conference import Conference
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


class ResourceUsersMixin(ModelResource):
    def get_queryset(self):
        qs = super().get_queryset()

        # TODO: find a way to used admin form's fields
        conference = Conference.objects.all().order_by("-start")[0]
        qs = qs.filter(**{self.conference_filter_by: conference})
        users_ids = qs.values_list(self.user_fk, flat=True)
        self._PREFETCHED_USERS_BY_ID = get_users_data_by_ids(list(users_ids))
        return qs

    def get_user_display_name(self, obj_id: Any) -> str:
        return self.get_user_data(obj_id)["displayName"]

    def get_user_data(self, obj_id: Any) -> dict[str, Any]:
        return self._PREFETCHED_USERS_BY_ID[str(obj_id)]


class ExportUsersMixin(ExportMixin):
    # https://github.com/django-import-export/django-import-export/blob/125c1cff2958a43f9824843ee90c27f5dc0280d5/import_export/resources.py#L933
    # I want the queryset to be done in the ResourceUsersMixin in order to have the Users
    # data stored and available when we export, so here I will return None
    # so that the baseclass Resource will call my custom get_queryset
    # The disadvantage is that we lose the request object and the filters...
    def get_export_queryset(self, request):
        return None
