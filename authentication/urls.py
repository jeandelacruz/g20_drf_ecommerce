from django.urls import path
from .views import LoginView, RefreshTokenView, ResetPasswordView, ChangePasswordView

urlpatterns = [
    path('signin/', LoginView.as_view(), name='signin'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('password/reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password/change/', ChangePasswordView.as_view(), name='password_change')
]
