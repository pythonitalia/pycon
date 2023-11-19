from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import JobListing


@admin.register(JobListing)
class JobListingAdmin(OrderedModelAdmin):
    model = JobListing
    list_display = ("title", "company", "conference", "move_up_down_links")
    list_filter = ("conference",)
