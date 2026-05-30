from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import Cart, CartItem, OrderItem, Product, Brand, Category, Order, ProductVariant, User, Request

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['name', 'sku', 'price_adjustment', 'amount', 'image', 'is_active']
    show_change_link = True

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['id', 'name', 'price', 'amount', 'has_variants', 'brand', 'category', 'created_at']
    list_filter = ['brand', 'category', 'has_variants', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'amount']
    inlines = [ProductVariantInline]

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['id', 'user_display', 'total_amount', 'status', 'items_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__username', 'address', 'phone']
    list_editable = ['status']
    readonly_fields = ['user', 'session_key', 'total_amount', 'created_at']
    
    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Гость ({obj.session_key[:8] if obj.session_key else 'аноним'})"
    user_display.short_description = 'Пользователь'
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Товаров'
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('id', 'user', 'session_key', 'status', 'total_amount', 'created_at')
        }),
        ('Данные доставки', {
            'fields': ('address', 'phone', 'comment')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['id', 'order', 'product_name', 'variant_name', 'quantity', 'price_at_moment']
    list_filter = ['order__status']
    search_fields = ['product_name']

@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone']
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'email', 'password')
        }),
        ('Личные данные', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar')
        }),
        ('Права доступа', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups')
        }),
        ('Бонусы', {
            'fields': ('bonus_points',)
        }),
    )

@admin.register(Request)
class RequestAdmin(ModelAdmin):
    list_display = ['id', 'type', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'type', 'created_at']
    search_fields = ['created_by__username', 'comment', 'admin_response']
    readonly_fields = ['created_by', 'data', 'comment', 'created_at']
    fieldsets = (
        ('Информация о заявке', {
            'fields': ('type', 'status', 'data')
        }),
        ('Отправитель', {
            'fields': ('created_by', 'comment', 'created_at')
        }),
        ('Модерация', {
            'fields': ('reviewed_by', 'admin_response')
        }),
    )

@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = ['id', 'product', 'name', 'sku', 'price_adjustment', 'amount', 'is_active']
    list_filter = ['product', 'is_active']
    search_fields = ['name', 'sku']

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ['id', 'user_display', 'session_key', 'get_total_price', 'get_total_items', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    
    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Гость ({obj.session_key[:8] if obj.session_key else '?'})"
    user_display.short_description = 'Пользователь'
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Сумма'
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Товаров'

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ['id', 'cart', 'get_display_name', 'quantity', 'price_at_moment', 'get_total']
    list_filter = ['cart__user', 'added_at']
    search_fields = ['product__name', 'variant__name']
    
    def get_display_name(self, obj):
        return obj.get_display_name()
    get_display_name.short_description = 'Товар'
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Сумма'