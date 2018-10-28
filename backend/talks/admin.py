from django.contrib import admin

from .models import Talk


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    pass
