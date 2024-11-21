from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_worker = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    can_add_stock = models.BooleanField(default=False)
    can_add_order = models.BooleanField(default=False)

class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_enter_raw_products = models.BooleanField(default=False)
    can_add_new_orders = models.BooleanField(default=False)
