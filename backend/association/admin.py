from django.contrib import admin
from .filters import YearFilter
from .models import Membership

class MembershipAdmin(admin.ModelAdmin):
    list_filter = [YearFilter]

admin.site.register(Membership, MembershipAdmin)
