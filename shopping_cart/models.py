from django.db import models
from users.models import User
from products.models import Product


# Create your models here.
class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'shopping_cart'

    def __str__(self):
        return f'{self.user} - {self.product}'
