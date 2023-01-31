from typing import List

from django.contrib import admin
from django.urls import path

SITE_NAME = "PyCon Italia"

admin.site.site_header = SITE_NAME
admin.site.site_title = SITE_NAME
admin.site.enable_nav_sidebar = True


class CustomIndexLinks(admin.ModelAdmin):
    def get_index_links(self) -> List:
        return getattr(self, "index_links", [])

    def get_urls(self) -> List:
        base_urls = super().get_urls()
        index_links = self.get_index_links()
        additional_urls = []

        for index_link in index_links:
            func_name = index_link[1]
            additional_urls.append(
                path(
                    func_name,
                    self.admin_site.admin_view(
                        getattr(self, func_name),
                    ),
                    name=f"custom_index_link_{func_name}",
                )
            )
        return base_urls + additional_urls
