from django.urls import path
from .views import OrderView, OrderEventView

urlpatterns = [
    path('', OrderView.as_view(), name='create'),
    path('webhook/', OrderEventView.as_view(), name='event')
]
