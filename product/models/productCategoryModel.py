from django.db import models

# Класс, отвечающий за представление сущности "Категории товара"

class ProductCategory(models.Model):
    # атрибут "Name" - название категории.
    name = models.CharField()

    # атрибут "Description" - описание категории (необязательно).
    description = models.TextField()