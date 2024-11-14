from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(write_only=True)

    class Meta:
        model = Product
        fields = '__all__'
