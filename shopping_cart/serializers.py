from rest_framework import serializers
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import ShoppingCart


class ShoppingCartListSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(
        max_digits=7, decimal_places=2, source='product.price'
    )
    quantity = serializers.IntegerField()


class ShoppingCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def update(self, instance, validated_data):
        product_id = validated_data['product_id']
        user_id = instance.id

        # Agregar el id del usuario al request
        validated_data['user_id'] = user_id

        # Validar si el producto existe
        get_object_or_404(Product, id=product_id, status=True)

        # Crear o Actualizar el producto
        # 1º Forma
        # record = ShoppingCart.objects.filter(
        #     user_id=user_id,
        #     product_id=product_id
        # ).first()

        # if record is None:
        #     # Crear el registro
        #     record = ShoppingCart.objects.create(**validated_data)
        # else:
        #     # Actualizar la cantidad
        #     record.quantity = quantity

        # record.save()

        # 2º Forma
        ShoppingCart.objects.update_or_create(
            user_id=user_id,
            product_id=product_id,
            defaults=validated_data
        )

        return validated_data
