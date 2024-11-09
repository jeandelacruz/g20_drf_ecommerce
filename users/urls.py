from django.urls import path
from .views import UserListCreateView, UserGetUpdateDeleteView


urlpatterns = [
    path('', UserListCreateView.as_view(), name='list_create'),
    path('<int:id>', UserGetUpdateDeleteView.as_view(), name='read_update_delete')
]
