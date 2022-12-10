from django.urls import path, include

urlpatterns = [
    path("v1/account/", include("apps.Account.urls")),
]
