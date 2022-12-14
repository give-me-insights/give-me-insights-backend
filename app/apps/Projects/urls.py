from django.urls import path

from .views import (
    ProjectListCreateRetrieveView,
    DataSourceListCreateView,
    EventListCreateView,
    ProjectLinkListCreateView,
    SourceDataRawView,
)


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
    ),
    path(
        "retrieve/<slug:project_key>/sources/delete/<slug:key>",
        DataSourceListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/events/create",
        EventListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/events/all",
        EventListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/events/delete/<slug:key>",
        EventListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/project-links/create",
        ProjectLinkListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/project-links/all",
        ProjectLinkListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/project-links/delete/<slug:key>",
        ProjectLinkListCreateView.as_view(),
    ),
    path(
        "retrieve/<slug:project_key>/sources/retrieve/<slug:source>/raw-data",
        SourceDataRawView.as_view(),
    )
]
