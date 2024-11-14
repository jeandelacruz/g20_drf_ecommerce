from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)  # 99999.99
    stock = models.IntegerField(default=0)
    image_url = models.URLField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'products'
