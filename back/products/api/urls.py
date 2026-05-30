from django.urls import path
from .views import ProductListAPI, ProductDetailAPI, CategoryListAPI, search_products

urlpatterns = [
    path('products/', ProductListAPI.as_view(), name='api_products'),
    path('products/<slug:slug>/', ProductDetailAPI.as_view(), name='api_product_detail'),
    path('categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('search/', search_products, name='api_search'),
]