from decimal import Decimal

from .models import ShoppingCart
from .serializers import ShoppingCartListSerializer


def get_products_to_cart(user_id):
    # select_related -> Relación de un solo objeto
    # prefetch_related -> Relación de una lista de objetos
    records = ShoppingCart.objects.select_related(
        'product'
    ).filter(user_id=user_id).all()
    serializer = ShoppingCartListSerializer(records, many=True)
    products = serializer.data

    prices = {
        'total': 0,
        'sub_total': 0,
        'igv': 0
    }

    if products:
        igv_price = Decimal(0.18)

        for product in products:
            price = Decimal(product['price'])
            quantity = product['quantity']
            product_price_total = round(price * quantity, 2)
            product['price_total'] = product_price_total
            prices['sub_total'] += product_price_total

        prices['igv'] = round(prices['sub_total'] * igv_price, 2)
        prices['total'] = round(prices['sub_total'] + prices['igv'], 2)

    return {
        'products': products,
        'prices': prices
    }
