from django.contrib import admin
from voting.models import Vote, VoteRange


@admin.register(VoteRange)
class VoteRangeAdmin(admin.ModelAdmin):
    list_display = ("name", "first", "last", "step")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("submission", "user", "value")
    list_filter = ("submission", "user", "value")
    search_fields = ("submission", "user")
