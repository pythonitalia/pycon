from django.contrib import admin
from django.http.request import HttpRequest

from community.models import Community, CommunityMember, Link


class LinkInline(admin.TabularInline):
    model = Link


class CommunityMemberInline(admin.TabularInline):
    model = CommunityMember
    autocomplete_fields = ("user",)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "hostname", "description")
    inlines = [LinkInline, CommunityMemberInline]
    fieldsets = (
        (
            "Community",
            {
                "fields": (
                    "name",
                    "hostname",
                    "description",
                ),
            },
        ),
        (
            "Landing Page",
            {
                "fields": (
                    "landing_page_primary_color",
                    "landing_page_secondary_color",
                    "landing_page_hover_color",
                    "landing_page_custom_logo_svg",
                ),
            },
        ),
    )

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if not obj:
            return False

        if request.user.is_superuser:
            return True

        if (
            obj.members.all()
            .filter(user=request.user, role=CommunityMember.Role.ADMIN)
            .exists()
        ):
            return True

        return False
