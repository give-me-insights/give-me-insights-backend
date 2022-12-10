from django.urls import path

from .views import ProjectListCreateRetrieveView, DataSourceListCreateView


urlpatterns = [
    path(
        "create",
        ProjectListCreateRetrieveView.as_view(),
    ),
    path(
        "all",
        ProjectListCreateRetrieveView.as_view(),
    ),
    path(
        "retrieve/<slug:key>",
        ProjectListCreateRetrieveView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/sources/create",
        DataSourceListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/sources/all",
        DataSourceListCreateView.as_view(),
    )
]
