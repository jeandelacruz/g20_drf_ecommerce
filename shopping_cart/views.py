from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartDeleteSerializer
from .selectors import get_products_to_cart


class ShoppingCartView(generics.GenericAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    http_method_names = ['get', 'put']
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        user_id = request.user.id
        cart_products = get_products_to_cart(user_id)
        return Response(cart_products, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartDeleteView(generics.GenericAPIView):
    serializer_class = ShoppingCartDeleteSerializer
    http_method_names = ['delete']
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        user_id = request.user.id
        serializer = self.serializer_class(data={'product_id': product_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
