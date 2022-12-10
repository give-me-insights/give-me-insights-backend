from django.urls import path

from .views import UserIsAuthenticatedView, AuthView, GetCSRFTokenView


urlpatterns = [
    path(
        "is-authenticated",
        UserIsAuthenticatedView.as_view(),
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
