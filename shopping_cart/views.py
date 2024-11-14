from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartListSerializer


class ShoppingCartView(generics.GenericAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    http_method_names = ['get', 'put']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ShoppingCartListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
