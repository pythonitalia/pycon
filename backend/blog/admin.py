from django import forms
from django.contrib import admin

from .models import Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "author",
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
    user_fk = "author_id"
    autocomplete_fields = ("author",)

    @admin.display(
        description="Author",
    )
    def author_display_name(self, obj):
        return obj.author.display_name
