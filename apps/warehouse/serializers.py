from rest_framework import serializers
from .models import Product, Material, Warehouse

class ProductMaterialResponseSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField(allow_null=True)
    material_name = serializers.CharField()
    qty = serializers.FloatField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    enough = serializers.CharField(allow_null=True)

class ProductResponseSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_qty = serializers.IntegerField()
    product_materials = ProductMaterialResponseSerializer(many=True)


