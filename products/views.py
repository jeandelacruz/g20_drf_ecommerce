from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import status, parsers
from .models import Product
from .serializers import ProductSerializer
from application.utils.pagination import CustomPagination


class ProductListCreateView(generics.GenericAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post']
    pagination_class = CustomPagination
    parser_classes = [parsers.MultiPartParser]

    def get(self, request):
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(
            self.get_queryset(), request
        )
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
