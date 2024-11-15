from rest_framework import serializers

from rest_framework.exceptions import NotFound
from django.db import transaction

from shopping_cart.selectors import get_products_to_cart, clean_products_to_cart
from products.selectors import reduce_stocks_products

from products.models import Product

from .models import Order, OrderDetail


class OrderSerializer(serializers.Serializer):
    def save(self, user_id):
        # Validar los productos del carrito de compras
        shopping_cart = get_products_to_cart(user_id)
        products = shopping_cart['products']
        prices = shopping_cart['prices']

        # Validar si no hay productos en el caritto de compras
        if not products:
            raise NotFound('Not found products to shopping cart')

        with transaction.atomic():
            # Crear el pedido
            order = Order.objects.create(
                user_id=user_id,
                total_price=prices['total'],
                subtotal_price=prices['sub_total'],
                igv_price=prices['igv']
            )

            # Insertar el detalle del pedido
            items = [
                OrderDetail(
                    order_id=order.id,
                    product_id=product['id'],
                    price=product['price'],
                    quantity=product['quantity']
                )
                for product in products
            ]
            OrderDetail.objects.bulk_create(items)

            # Reducir el stock de los productos
            reduces_obj = reduce_stocks_products(products)
            Product.objects.bulk_update(reduces_obj, ['stock'])

            # limpiar el carrito de compras
            clean_cart = clean_products_to_cart(user_id)
            clean_cart.delete()
