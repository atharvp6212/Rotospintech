from django.db import models
from django.utils import timezone

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()  # Quantity available in stock
    
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SubPart(models.Model):
    name = models.CharField(max_length=100)
    raw_materials = models.ManyToManyField(RawMaterial, through='SubPartRawMaterial')
    

    def __str__(self):
        return self.name

    def calculate_production(self):
        production_counts = []
        for sprm in self.subpartrawmaterial_set.all():
            available = sprm.raw_material.quantity
            required = sprm.quantity_required
            production_counts.append(available // required)
        return min(production_counts) if production_counts else 0


class Product(models.Model):
    name = models.CharField(max_length=100)
    sub_parts = models.ManyToManyField(SubPart)
    
    def __str__(self):
        return self.name

class SubPartRawMaterial(models.Model):
    sub_part = models.ForeignKey(SubPart, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity_required = models.FloatField()  # Quantity required for this sub-part

    def __str__(self):
        return f"{self.sub_part.name} requires {self.quantity_required} of {self.raw_material.name}"
    
class StockHistory(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='stock_history')
    date_added = models.DateTimeField(default=timezone.now)
    quantity_before = models.FloatField()
    quantity_added = models.FloatField()
    quantity_after = models.FloatField()

    def __str__(self):
        return f"{self.raw_material.name} stock change on {self.date_added}"