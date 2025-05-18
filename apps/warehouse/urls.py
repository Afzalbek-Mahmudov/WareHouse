from django.urls import path
from .views import ProductMaterialsAPIView

urlpatterns = [
    path('api/product-materials/', ProductMaterialsAPIView.as_view(), name='product-materials'),
]
