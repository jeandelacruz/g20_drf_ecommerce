from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import OrderSerializer


class OrderView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class()
        serializer.save(request.user)
        return Response(status=status.HTTP_200_OK)


class OrderEventView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class()
        serializer.event_trigger(request.data)
        return Response(status=status.HTTP_200_OK)
