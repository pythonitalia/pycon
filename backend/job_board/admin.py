from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import JobListing


@admin.register(JobListing)
class PostAdmin(OrderedModelAdmin):
    model = JobListing
    list_display = ("title", "company", "move_up_down_links")
