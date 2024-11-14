from django.urls import path
from .views import ProductListCreateView, ProductGetUpdateDeleteView


urlpatterns = [
    path('', ProductListCreateView.as_view(), name='list_create'),
    path(
        '<int:id>',
        ProductGetUpdateDeleteView.as_view(),
        name='read_update_delete'
    )
]
