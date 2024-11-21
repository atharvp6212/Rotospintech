from django.db import models
from inventory.models import SubPart, Color, RawMaterial

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date/time when an order is created
    # Other fields

    def __str__(self):
        return f"Order {self.id}"

class OrderedSubPart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_sub_parts')
    sub_part = models.ForeignKey(SubPart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.sub_part.name} - {self.quantity} units"
