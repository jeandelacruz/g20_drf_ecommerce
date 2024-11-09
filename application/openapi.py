from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path


view_swagger = get_schema_view(
    openapi.Info(
        title='DRF Boilerplate',
        description='Documentación de las apis del Boilerplate',
        default_version='0.1'
    ),
    public=True
)

urlpatterns = [
    path('', view_swagger.with_ui('swagger'), name='swagger-ui')
]
