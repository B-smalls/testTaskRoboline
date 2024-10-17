from django.db import models

# Класс, отвечающий за представление сущности "Товар"

class Product(models.Model):
    # атрибут "Name" - название товара.
    name = models.CharField("Name", db_column="Name", max_length=100)

    # атрибут "Description" - описание товара.
    description = models.TextField("Description", db_column="Description")

    # атрибут "Price" - цена товара.
    price = models.DecimalField("Price", db_column="Price", max_digits=19, decimal_places=2)

    #атрибут "СategoryID" - идентификатор категории, к которой относится товар.
    categoryID = models.ForeignKey(
        'product.ProductCategory', 
        models.CASCADE, 
        verbose_name="CategoryID",
        db_column="CategoryID"
    )

    class Meta:
        db_table = "Product"
