from django.db import models

# Класс, отвечающий за представление сущности "Категории товара"

class ProductCategory(models.Model):
    # атрибут "Name" - название категории.
    name = models.CharField("Name", db_column="Name", unique=True, max_length=100)

    # атрибут "Description" - описание категории (необязательно).
    description = models.TextField("Description", db_column="Description", null=True, blank=True)

    class Meta:
        db_table = "ProductCategory"