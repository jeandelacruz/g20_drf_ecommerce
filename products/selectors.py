from .models import Product


def reduce_stocks_products(products):
    obj_updates = []

    for product in products:
        record = Product.objects.filter(id=product['id']).first()
        new_stock = record.stock - product['quantity']
        record.stock = new_stock
        obj_updates.append(record)

    return obj_updates
