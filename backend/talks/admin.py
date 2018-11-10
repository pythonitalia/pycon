from django.contrib import admin

from .models import Talk


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ('conference', 'title', 'topic', 'language',)
    list_filter = ('conference',)
    search_fields = ('title', 'abstract',)
