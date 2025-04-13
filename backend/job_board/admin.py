from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from custom_admin.widgets import RichEditorWidget

from .models import JobListing


@admin.register(JobListing)
class JobListingAdmin(OrderedModelAdmin):
    model = JobListing
    list_display = ("title", "company", "conference", "move_up_down_links")
    list_filter = ("conference",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "description":
            kwargs["widget"] = RichEditorWidget()

        return super().formfield_for_dbfield(db_field, **kwargs)
