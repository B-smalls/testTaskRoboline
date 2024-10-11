from django.db import models

# Класс, отвечающий за представление сущности "Товар"

class Product(models.Model):
    # атрибут "Name" - название товара.
    name = models.CharField()

    # атрибут "Description" - описание товара.
    description = models.TextField()

    # атрибут "Price" - цена товара.
    price = models.DecimalField()

    #атрибут "СategoryID" - идентификатор категории, к которой относится товар.
    categoryID = models.ForeignKey(
        'product.ProductCategory', models.CASCADE
    )
