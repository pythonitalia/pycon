from django.contrib import admin

from .models import FAQ, GenericCopy, Menu, MenuLink


@admin.register(GenericCopy)
class GenericCopyAdmin(admin.ModelAdmin):
    list_display = ("key", "content", "conference")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("conference",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("identifier", "title", "conference")


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "menu")
    list_filter = ("menu", "is_primary")
