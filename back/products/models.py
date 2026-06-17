from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название бренда"
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='brands/',
        blank=True,
        null=True,
        verbose_name="Логотип бренда"
    )

    class Meta:
        db_table = 'products_brand'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название категории"
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name="Изображение категории"
    )

    class Meta:
        db_table = 'products_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )

    description = models.TextField(
        blank=True,
        default=''
    )

    amount = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество"
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Изображение товара"
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    aver_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Средняя оценка")
    rating_count = models.PositiveIntegerField(default=0, verbose_name="Количество оценок")
    has_variants = models.BooleanField(default=False, verbose_name="Есть вариации")

    class Meta:
        db_table = 'products_product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, verbose_name="Название вариации")  # например: "Красный", "128GB"
    sku = models.CharField(max_length=100, unique=True, blank=True, verbose_name="Артикул")
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Корректировка цены")
    amount = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    image = models.ImageField(upload_to='product_variants/', blank=True, null=True, verbose_name="Изображение вариации")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'products_product_variant'
        verbose_name = 'Вариация товара'
        verbose_name_plural = 'Вариации товаров'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.sku:
            base_sku = f"{self.product.id}-{slugify(self.name)}"
            sku = base_sku
            counter = 1
            while ProductVariant.objects.filter(sku=sku).exists():
                sku = f"{base_sku}-{counter}"
                counter += 1
            self.sku = sku
        super().save(*args, **kwargs)
    
    def get_price(self):
        return self.product.price + self.price_adjustment
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"


class User(AbstractUser):

    class Role(models.TextChoices):
        # GUEST = 'guest', 'Гость'
        BUYER = 'buyer', 'Покупатель'
        MANAGER = 'manager', 'Менеджер'
        ADMIN = 'admin', 'Администратор'

    phone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )


    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.BUYER
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )

    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_user_set',
    #     blank=True,
    # )

    class Meta:
        db_table = 'products_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_manager(self):
        return self.role == self.Role.MANAGER or self.is_superuser

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает обработки'
        COMPLETED = 'completed', 'Завершен'
        CANCELLED = 'cancelled', 'Отменен'
        PAID = 'paid', 'Оплачен'
        SHIPPED = 'shipped', 'Отправлен'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Для гостей
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Информация о доставке
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    comment = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Заказ #{self.id}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    variant_name = models.CharField(max_length=100, blank=True, default='')
    quantity = models.PositiveIntegerField(default=1)
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total(self):
        return self.quantity * self.price_at_moment
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    # ###
    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total_price(self):
        return sum(item.get_total() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        if self.user:
            return f"Корзина {self.user.username}"
        return f"Корзина гостя {self.session_key}"
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_total(self):
        return self.quantity * self.price_at_moment
    
    def get_display_name(self):
        if self.variant:
            return f"{self.product.name} ({self.variant.name})"
        return self.product.name
    class Meta:
        verbose_name = "Запись корзины"
        verbose_name_plural = "Записи корзины"
    

    
class Request(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'На рассмотрении'
        APPROVED = 'approved', 'Одобрено'
        REJECTED = 'rejected', 'Отклонено'

    class Type(models.TextChoices):
        ADD_PRODUCT = 'add_product', 'Добавление товара'
        EDIT_PRODUCT = 'edit_product', 'Редактирование товара'
        DELETE_PRODUCT = 'delete_product', 'Удаление товара'
        ADD_BRAND = 'add_brand', 'Добавление бренда'
        EDIT_BRAND = 'edit_brand', 'Редактирование бренда'
        ADD_CATEGORY = 'add_category', 'Добавление категории'
        MESSAGE_TO_ADMIN = 'message', 'Сообщение администратору'

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name="Статус")

    data = models.JSONField(verbose_name="Данные заявки", null=True, blank=True, help_text="Содержит информацию о предлагаемом изменении")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests', verbose_name="Кто создал")

    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests', verbose_name="Кто модерировал")

    type = models.CharField(max_length=30, choices=Type.choices,  help_text="Содержит информацию о предлагаемом изменении")

    comment = models.TextField(blank=True, default='', verbose_name="Комментарий менеджера")
    
    # Ответ администратора
    admin_response = models.TextField(blank=True, default='', verbose_name="Ответ администратора")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"Заявка #{self.id} ({self.get_type_display()}) - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    admin_reply = models.TextField(blank=True, null=True, verbose_name="Ответ менеджера")
    admin_replied_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата ответа")
    admin_replied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='review_replies', verbose_name="Кто ответил")
    
    class Meta:
        db_table = 'products_review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['product', 'user']
    
    def can_delete(self, user):
        """Проверка, может ли пользователь удалить отзыв"""
        return user.is_authenticated and (user.is_superuser or user.role == 'admin' or user.role == 'manager')
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}⭐"