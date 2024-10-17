# Модуль 'productSerializer.py' отвечает за сериализацию/десериализацию 
# в формате JSON, а также за валидацию данных для модели Product (Продукта). 
# Классы, содержащиеся в этом пакете, отвечают за сериализацию/десериализацию для каждой 
# требуемой CRUD операции.

from product.models.productModel import Product
from product.models.productCategoryModel import ProductCategory
from rest_framework import serializers
from product.serializers.productCategorySerializer import ProductCategorySerializerRead

# Класс, отвечающий за создание продутка
class ProductSerializerCreate(serializers.ModelSerializer):
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    price = serializers.DecimalField(
        max_digits=19, decimal_places=2,
        min_value=0.01,
    )
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'categoryID')

    # Валидация названия товара
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название товара должно содержать минимум 2 символа.")
        if len(value) > 100:
            raise serializers.ValidationError("Название товара не может превышать 100 символов.")
        return value
    
    # Валидация описания товара
    def validate_description(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Описание товара не может превышать 500 символов.")
        return value
    
    # Валидация категории
    def validate_categoryID(self, value):
        if not ProductCategory.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Категория с таким ID не существует.")
        return value
    
    # Общая валидация для создания продукта
    def validate(self, data):
        name = data.get('name')
        categoryID = data.get('categoryID')

        # Проверка наличия товара с таким же названием и категорией
        if Product.objects.filter(name=name, categoryID=categoryID).exists():
            raise serializers.ValidationError(
                f"Товар с названием '{name}' в этой категории уже существует."
            )
        return data
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


# Класс, отвечающий за получение продутка
class ProductSerializerRead(serializers.ModelSerializer):
    # Вложенный сериализатор для категории продукта
    categoryID = ProductCategorySerializerRead(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'categoryID')

# Класс, отвечающий за обновление продутка
class ProductSerializerUpdate(serializers.ModelSerializer):
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    price = serializers.DecimalField(
        max_digits=19, decimal_places=2,
        min_value=0.01,
        help_text="Цена товара должна быть положительным числом"
    )
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'categoryID')

    # Валидация названия товара
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название товара должно содержать минимум 2 символа.")
        if len(value) > 100:
            raise serializers.ValidationError("Название товара не может превышать 100 символов.")
        return value

    # Валидация описания товара
    def validate_description(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Описание товара не может превышать 500 символов.")
        return value

    # Валидация цены
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительным числом.")
        return value

    # Валидация категории
    def validate_categoryID(self, value):
        if not ProductCategory.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Категория с таким ID не существует.")
        return value

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.categoryID = validated_data.get('categoryID', instance.categoryID)
        instance.save()
        return instance

# Класс, отвечающий за удаление продукта
class ProductSerializerDelete(serializers.Serializer):
    id = serializers.IntegerField()

    def delete(self, validated_data):
        product_id = validated_data.get('id')
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар с таким ID не найден.")

