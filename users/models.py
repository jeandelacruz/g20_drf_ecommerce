from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # Polimorfismo
    email = models.EmailField(unique=True)

    # Crear nuevos atributos (columnas)
    # auto_now_add -> insertar la fecha y hora actual, unicamente en la creación
    # auto_now -> insertar la fecha y hora actual, por cada cambio realizado
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
