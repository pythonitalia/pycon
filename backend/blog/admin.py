from django import forms
from django.contrib import admin

from users.autocomplete import UsersBackendAutocomplete
from users.client import get_users_data_by_ids

from .models import Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            "author_id": UsersBackendAutocomplete(admin.site),
        }
        fields = [
            "author_id",
            "title",
            "slug",
            "content",
            "excerpt",
            "published",
            "image",
        ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("title", "published", "author_display_name")

    def author_display_name(self, obj):
        return self._users_by_id[str(obj.author_id)]["displayName"]

    author_display_name.short_description = "Author"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        author_ids = queryset.values_list("author_id", flat=True)
        self._users_by_id = get_users_data_by_ids(list(author_ids))
        return queryset
