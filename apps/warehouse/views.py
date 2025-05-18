from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, ProductMaterial, Warehouse
from .serializers import ProductResponseSerializer


class ProductMaterialsAPIView(APIView):
    def post(self, request):
        products = request.data.get("products")

        if not isinstance(products, list) or not products:
            return Response({"error": "products must be a list and required."}, status=status.HTTP_400_BAD_REQUEST)

        result = []
        for product_data in products:
            validation_error = self.validate_product_data(product_data)
            if validation_error:
                return validation_error

            product_code = product_data["product_code"]
            quantity = int(product_data["quantity"])

            try:
                product = Product.objects.get(product_code=product_code)
            except Product.DoesNotExist:
                return Response({"error": f"Product with code {product_code} not found."}, status=status.HTTP_404_NOT_FOUND)

            materials_info = self.get_required_materials(product, quantity)

            result.append({
                "product_name": product.name,
                "product_qty": quantity,
                "product_materials": materials_info
            })

        serializer = ProductResponseSerializer(result, many=True)
        return Response({"result": serializer.data})

    def validate_product_data(self, data):
        """product_code va quantity ni tekshiradi"""
        if not isinstance(data, dict):
            return Response({"error": "Each item must be a dictionary."}, status=status.HTTP_400_BAD_REQUEST)

        product_code = data.get("product_code")
        quantity = data.get("quantity")

        if product_code is None or quantity is None:
            return Response({"error": "product_code and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            int(quantity)
        except ValueError:
            return Response({"error": "quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        return None

    def get_required_materials(self, product, quantity):
        """Mahsulot uchun kerakli materiallarni omborlardan chiqaradi"""
        product_materials = ProductMaterial.objects.filter(product=product)
        result_materials = []

        for i in product_materials:
            required_qty = i.quantity * quantity
            warehouses = Warehouse.objects.filter(material=i.material).order_by('id')

            total_available = sum([w.remainder for w in warehouses])
            qty_left = required_qty

            for b in warehouses:
                if qty_left <= 0:
                    break

                take_qty = min(b.remainder, qty_left)
                if take_qty > 0:
                    result_materials.append({
                        "warehouse_id": b.id,
                        "material_name": i.material.name,
                        "qty": take_qty,
                        "price": b.price,
                    })
                    qty_left -= take_qty

            if qty_left > 0:
                result_materials.append({
                    "warehouse_id": None,
                    "enough": f"Not enough material: {qty_left} more of '{i.material.name}' required.",
                    "material_name": i.material.name,
                    "qty": qty_left,
                    "price": None
                })

        return result_materials
