from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product, Material, ProductMaterial, Warehouse

admin.site.register(Material)

@admin.register(Product)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['product_code','name']

@admin.register(ProductMaterial)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['product','material','quantity']

@admin.register(Warehouse)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','material','remainder','price']


