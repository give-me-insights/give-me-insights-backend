from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token

from .serializers import AuthSerializer


class UserIsAuthenticatedView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class AuthView(views.ObtainAuthToken):
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # set cookie
        login(request, user=user)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFTokenView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response({"success": "CSRF cookie set"})
