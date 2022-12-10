
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


User = get_user_model()


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            err_msg = "Unable to log in with provided credentials."
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(err_msg, code="authorization")
            user = authenticate(
                request=self.context.get("request"), username=user.username, password=password
            )
            if not user:
                raise serializers.ValidationError(err_msg, code="authorization")

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs
