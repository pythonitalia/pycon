from django import forms
from django.contrib import admin

from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin

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
class PostAdmin(AdminUsersMixin):
    form = PostAdminForm
    list_display = ("title", "published", "author_display_name")
    user_fk = "author_id"

    @admin.display(
        description="Author",
    )
    def author_display_name(self, obj):
        return self.get_user_display_name(obj.author_id)

