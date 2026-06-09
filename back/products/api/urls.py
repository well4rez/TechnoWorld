from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductListAPI, ProductDetailAPI, CategoryListAPI, search_products, get_current_user, register_user

urlpatterns = [
    path('products/', ProductListAPI.as_view(), name='api_products'),
    path('products/<slug:slug>/', ProductDetailAPI.as_view(), name='api_product_detail'),
    path('categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('search/', search_products, name='api_search'),

    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User endpoints
    path('user/', get_current_user, name='get_current_user'),
    path('register/', register_user, name='register_user'),
]