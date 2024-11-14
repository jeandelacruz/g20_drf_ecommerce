from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import status, parsers, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Product
from .serializers import ProductSerializer
from application.utils.pagination import CustomPagination


class ProductListCreateView(generics.GenericAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post']
    pagination_class = CustomPagination
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'q',
                openapi.IN_QUERY,
                description='Buscar por nombre o descripción',
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        query = request.query_params.get('q', '')
        filters = {'status': True}

        filtered_queryset = self.queryset.filter(**filters).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(
            filtered_queryset, request
        )
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ProductGetUpdateDeleteView(generics.GenericAPIView):
    queryset = Product.objects
    serializer_class = ProductSerializer
    http_method_names = ['get', 'patch', 'delete']
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        record = get_object_or_404(
            self.queryset, pk=id
        )
        serializer = self.serializer_class(record, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        record = get_object_or_404(
            self.queryset, pk=id
        )
        serializer = self.serializer_class(record, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        record = get_object_or_404(
            self.queryset, pk=id
        )
        serializer = self.serializer_class(record)
        serializer.delete(record)
        return Response(status=status.HTTP_204_NO_CONTENT)
