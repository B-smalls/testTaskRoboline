from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from product.serializers.productCategorySerializer import ProductCategorySerializerCreate, ProductCategorySerializerDelete, ProductCategorySerializerRead, ProductCategorySerializerUpdate
from product.models.productCategoryModel import ProductCategory

# Представление, отвечающее за создание категории продукта
@extend_schema_view(
    post=extend_schema(request=ProductCategorySerializerCreate,
                       summary='Создание категории товара', tags=['Категории товаров']),
)
class ProductCategoryCreateView(APIView):
    def post(self, request):
        serializer = ProductCategorySerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Категория успешно создана"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Представление, отвечающее за предоставление информации о категории продукта
@extend_schema_view(
    get=extend_schema(summary='Получение списка категорий товаров', tags=['Категории товаров']),
)
class ProductCategoryListView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        
        if not categories.exists():
            return Response({"error": "Категории товаров отсутствуют"}, status=status.HTTP_204_NO_CONTENT)

        serializer = ProductCategorySerializerRead(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Представление, отвечающее за обновление категории продукта
@extend_schema_view(
    put=extend_schema(request=ProductCategorySerializerUpdate,
                      summary='Обновление категории товара', tags=['Категории товаров']),
)
class ProductCategoryUpdateView(APIView):
    def put(self, request, pk):
        try:
            category = ProductCategory.objects.get(pk=pk)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Категория не найдена"}, status=status.HTTP_404_NOT_FOUND)

        
        # partial=True позволяет обновлять только переданные поля
        serializer = ProductCategorySerializerUpdate(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Категория успешно обновлена"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Представление, отвечающее за удаление категории продукта
@extend_schema_view(
    delete=extend_schema(request=None,  # Указываем, что запрос не требуется
                         summary='Удаление категории товара', tags=['Категории товаров']),
)
class ProductCategoryDeleteView(APIView):
    def delete(self, request, pk):
        try:
            product_category = ProductCategory.objects.get(pk=pk)
            product_category.delete()
            return Response({"message": "Категория успешно удалена."}, status=status.HTTP_204_NO_CONTENT)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Категория с таким ID не найдена."}, status=status.HTTP_404_NOT_FOUND)
