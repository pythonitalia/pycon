from django.contrib import admin
from conferences.frontend import trigger_frontend_revalidate
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        conference = obj.conference

        if not conference.frontend_revalidate_url:
            return

        trigger_frontend_revalidate(conference, obj)
