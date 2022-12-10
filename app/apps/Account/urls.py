from django.urls import path

from .views import AuthenticatedUserView, AuthView, GetCSRFTokenView


urlpatterns = [
    path(
        "get-authenticated-user",
        AuthenticatedUserView.as_view(),
    ),
    path(
        "perform-authentication",
        AuthView.as_view(),
    ),
    path(
        "get-csrf-token",
        GetCSRFTokenView.as_view(),
    ),
]
