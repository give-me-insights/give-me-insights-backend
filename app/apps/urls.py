from django.urls import path, include

urlpatterns = [
    path("v1/account/", include("apps.Account.urls")),
    path("v1/projects/", include("apps.Projects.urls")),
]
