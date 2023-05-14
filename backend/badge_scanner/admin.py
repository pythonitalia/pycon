from django.contrib import admin


from .models import BadgeScan


@admin.register(BadgeScan)
class PostAdmin(admin.ModelAdmin):
    pass
