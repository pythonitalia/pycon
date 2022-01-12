from django.contrib import admin

from .models import JobListing


@admin.register(JobListing)
class PostAdmin(admin.ModelAdmin):
    model = JobListing
    list_display = ("title", "company")
