from django.db import models

# Create your models here.

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_code = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name

class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.material.name} ({self.quantity})"

class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='warehouse')
    remainder = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Warehouse ID: {self.id}"

