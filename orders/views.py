from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import OrderSerializer


class OrderView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        serializer = self.serializer_class()
        serializer.save(user_id)
        return Response(status=status.HTTP_200_OK)
