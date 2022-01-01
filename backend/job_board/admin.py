from django.contrib import admin

from .models import JobListing


@admin.register(JobListing)
class PostAdmin:
    list_display = ("title", "company")
