from django.urls import path
from .views import *
from .api.views import ProductListAPI, ProductDetailAPI, CategoryListAPI, search_products

app_name = 'products'

urlpatterns = [
    path('api/products/', ProductListAPI.as_view(), name='api_products'),
    path('api/products/<slug:slug>/', ProductDetailAPI.as_view(), name='api_product_detail'),
    path('api/categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('api/search/', search_products, name='api_search'),


    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('category/<slug:slug>/', category_products, name='category_list'),
    
    # Аутентификация
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    
    # Админские URL
    path('admin/products/user/', user_list, name='user_list'),
    path('admin/user/<int:user_id>/change-role', change_user_role, name='change_user_role'),

    # Админ заявы
    path('requests/', pending_requests, name='pending_requests'),
    path('requests/<int:request_id>/', moderate_request, name='moderate_request'),

    # Манагер заявы
    path('requests/create/<str:type>/', create_request, name="create_request"),
    path('requests/my', my_requests, name="my_requests"),


    path('categories/', categories_list, name='categories_list'),

    path('requests/message/', message_to_admin, name='message_to_admin'),

    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),
    
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),

    path('admin/orders/', all_orders, name='admin_orders'),
    path('admin/orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
    

]