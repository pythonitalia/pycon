from django.urls import path
from .views import view_brochure

urlpatterns = [
    path("view-brochure/<int:sponsor_lead_id>/", view_brochure, name="view-brochure"),
]
