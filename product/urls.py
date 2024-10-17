from django.urls import path

from product.views import productCategoryView, productView
urlpatterns = [
    # Категории товаров
    path('product-categories/', productCategoryView.ProductCategoryListView.as_view(), name='list-product-categories'),
    path('product-categories/create/', productCategoryView.ProductCategoryCreateView.as_view(), name='create-product-category'),
    path('product-categories/update/<int:pk>/', productCategoryView.ProductCategoryUpdateView.as_view(), name='update-product-category'),
    path('product-categories/delete/<int:pk>/', productCategoryView.ProductCategoryDeleteView.as_view(), name='delete-product-category'),

    # Товары
    path('products/', productView.ProductListView.as_view(), name='list-products'),
    path('products/create/', productView.ProductCreateView.as_view(), name='create-product'),
    path('products/update/<int:pk>/', productView.ProductUpdateView.as_view(), name='update-product'),
    path('products/delete/<int:pk>/', productView.ProductDeleteView.as_view(), name='delete-product'),
]
