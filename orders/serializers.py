from rest_framework import serializers

from rest_framework.exceptions import NotFound
from django.db import transaction

from shopping_cart.selectors import get_products_to_cart, clean_products_to_cart
from products.selectors import reduce_stocks_products
from application.utils.mercadopago import MercadopagoClient

from products.models import Product

from .models import Order, OrderDetail


class OrderSerializer(serializers.Serializer):
    def save(self, user):
        # Validar los productos del carrito de compras
        user_id = user.id
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

            # Generar Link de pago
            checkout_data = self._create_payment_url(
                user, products, order, prices['igv']
            )
            order.checkout_id = checkout_data['id']
            order.checkout_url = checkout_data['init_point']
            order.save()

            # Reducir el stock de los productos
            reduces_obj = reduce_stocks_products(products)
            Product.objects.bulk_update(reduces_obj, ['stock'])

            # limpiar el carrito de compras
            clean_cart = clean_products_to_cart(user_id)
            clean_cart.delete()

    def event_trigger(self, body):
        topic = body['topic']
        mercadopago = MercadopagoClient()

        if topic == 'payment':
            payment_id = body['resource']
            payment_data = mercadopago.get_payment_by_id(payment_id)
            merchant_order_id = payment_data['order']['id']
            merchant_order = mercadopago.get_merchant_order_by_id(
                merchant_order_id
            )

            # Calculamos el monto pagado (MERCHANT_ORDER)
            paid_amount = sum(
                payment_merchant_order['transaction_amount']
                for payment_merchant_order in merchant_order['payments']
                if payment_merchant_order['status'] == 'approved'
            )

            if paid_amount >= merchant_order['total_amount']:
                external_reference = payment_data['external_reference']
                status = payment_data['status']
                record = Order.objects.filter(
                    id=int(external_reference)
                ).first()
                record.status = status.upper()
                record.save()

    def _create_payment_url(self, user, products, order, igv_price):
        payer = {
            'name': user.first_name,
            'surname': user.last_name,
            'email': user.email
        }

        items = [
            {
                'id': product['id'],
                'title': product['name'],
                'quantity': product['quantity'],
                'unit_price': float(product['price'])
            }
            for product in products
        ]

        items.append({
            'id': '99999',
            'title': 'Impuesto (18%)',
            'quantity': 1,
            'unit_price': float(igv_price)
        })

        mercadopago = MercadopagoClient()
        return mercadopago.create_preferences(payer, items, order.id)
