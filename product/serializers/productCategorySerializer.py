# Модуль 'productCategorySerializer.py' отвечает за сериализацию/десериализацию 
# в формате JSON, а также за валидацию данных для модели ProductCategory (Категории продукта). 
# Классы, содержащиеся в этом пакете, отвечают за сериализацию/десериализацию для каждой 
# требуемой CRUD операции.

from product.models.productCategoryModel import ProductCategory
from rest_framework import serializers
from rest_framework.exceptions import ParseError


# Класс, отвечающий за создание категории продутка
class ProductCategorySerializerCreate(serializers.ModelSerializer):
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500
    )

    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'name',
            'description'
        )
    # Валидация названия категории
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название категории должно содержать минимум 2 символа.")
        if len(value) > 100:
            raise serializers.ValidationError("Название категории не может превышать 100 символов.")
        return value
    
    # Валидация описания категории
    def validate_description(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Описание категории не может превышать 500 символов.")
        return value
    
    def create(self, validated_data):
        name = validated_data.get('name')
        if ProductCategory.objects.filter(name=name).exists():
            raise serializers.ValidationError("Категория с таким именем уже существует.")
        
        # Создаем категорию с валидированными данными
        prodCat = ProductCategory.objects.create(**validated_data)
        return prodCat

# Класс, отвечающий за просмотр категории продутка
class ProductCategorySerializerRead(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'name',
            'description'
        )

# Класс, отвечающий за обновление категории продутка
class ProductCategorySerializerUpdate(serializers.ModelSerializer):
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        help_text="Описание категории (до 500 символов)"
    )

    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'description')
    
    # Валидация названия категории
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название категории должно содержать минимум 2 символа.")
        if len(value) > 100:
            raise serializers.ValidationError("Название категории не может превышать 100 символов.")
        return value
    
    # Валидация описания категории
    def validate_description(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Описание категории не может превышать 500 символов.")
        return value

    def update(self, instance, validated_data):
        # Валидация и обновление полей
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

# Класс, отвечающий за удаление категории продукта
class ProductCategorySerializerDelete(serializers.Serializer):
    id = serializers.IntegerField()

    def delete(self, validated_data):
        category_id = validated_data.get('id')
        try:
            productCategory = ProductCategory.objects.get(id=category_id)
            productCategory.delete()
            return {"message": "Категория успешно удалена."}  # Возвращаем сообщение об успешном удалении
        except ProductCategory.DoesNotExist:
            raise serializers.ValidationError("Категория с таким ID не найдена.")
