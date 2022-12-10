from django.urls import path

from .views import ProjectListCreateView


urlpatterns = [
    path(
        "create",
        ProjectListCreateView.as_view(),
    ),
    path(
        "all",
        ProjectListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:key>",
        ProjectListCreateView.as_view(),
    ),
]
