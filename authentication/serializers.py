from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from secrets import token_hex

from users.models import User
from application.utils.mailing import Mailing


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=120, write_only=True)
    password = serializers.CharField(max_length=60, write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        # Validar que el usuario exista
        if not user:
            raise AuthenticationFailed('Invalid username or password')

        # Validar que el usuario este activo
        if not user.is_active:
            raise AuthenticationFailed(f'User {username} is inactive')

        token = RefreshToken.for_user(user)

        return {
            'access_token': str(token.access_token),
            'refresh_token': str(token)
        }


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=120)

    def validate(self, attrs):
        email = attrs.get('email')
        new_password = token_hex(6)

        mailing = Mailing()

        # Validar el usuario
        user = get_object_or_404(
            User, email=email, is_active=True
        )
        user.set_password(new_password)
        user.save()

        mailing.mail_reset_password(
            email, user.first_name, new_password
        )

        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=120)
    confirm_password = serializers.CharField(max_length=120)

    def validate_confirm_password(self, value):
        password = self.initial_data.get('password')
        if value != password:
            raise serializers.ValidationError(
                'Password and Confirm Password do not match'
            )
        return value

    def update(self, instance, validated_data):
        password = validated_data['password']
        instance.set_password(password)
        instance.save()
        return validated_data
