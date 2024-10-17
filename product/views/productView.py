from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from product.serializers.productSerializer import ProductSerializerCreate, ProductSerializerDelete, ProductSerializerRead, ProductSerializerUpdate
from product.models.productModel import Product

# Представление, отвечающее за создание продукта
@extend_schema_view(
    post=extend_schema(request=ProductSerializerCreate,
                       summary='Создание товара', tags=['Товары']),
)
class ProductCreateView(APIView):
    def post(self, request):
        serializer = ProductSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Товар успешно создан"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Представление, отвечающее за предоставление информации о продукте
@extend_schema_view(
    get=extend_schema(summary='Получение списка товаров', tags=['Товары']),
)
class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        
        if not products.exists():
            return Response({"error": "Товары отсутствуют"}, status=status.HTTP_204_NO_CONTENT)

        serializer = ProductSerializerRead(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Представление, отвечающее за обновление продукта
@extend_schema_view(
    put=extend_schema(request=ProductSerializerUpdate,
                      summary='Обновление товара', tags=['Товары']),
)
class ProductUpdateView(APIView):
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializerUpdate(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Товар успешно обновлен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Представление, отвечающее за удаление продукта
@extend_schema_view(
    delete=extend_schema(request=None,  # Запрос не требуется, так как ID передается через URL
                         summary='Удаление продукта', tags=['Товары']),
)
class ProductDeleteView(APIView):
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({"message": "Продукт успешно удален."}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Продукт с таким ID не найден."}, status=status.HTTP_404_NOT_FOUND)

