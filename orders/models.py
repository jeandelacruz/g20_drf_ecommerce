from django.db import models
from users.models import User
from products.models import Product


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=7, decimal_places=2)
    igv_price = models.DecimalField(max_digits=7, decimal_places=2)
    checkout_url = models.URLField(blank=True, null=True)
    checkout_id = models.CharField(blank=True, null=True)
    status = models.CharField(default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'orders_details'
