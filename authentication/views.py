from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import generics
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import LoginSerializer, ResetPasswordSerializer, ChangePasswordSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data
        return Response(tokens, status=status.HTTP_200_OK)


class RefreshTokenView(TokenViewBase):
    serializer_class = TokenRefreshSerializer
    authentication_classes = [JWTAuthentication]


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
