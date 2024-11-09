from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from .models import User
from .pagination import CustomPagination


class UserListCreateView(generics.GenericAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Definir los permisos por verbos
    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [permissions.IsAuthenticated()]
    #     return [permissions.AllowAny()]

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


# /users/<id>
class UserGetUpdateDeleteView(generics.GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'delete']

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
        pass
