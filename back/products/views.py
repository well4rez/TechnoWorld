from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Product, Category, User, Cart, CartItem, Request, Order, OrderItem, ProductVariant
from .forms import RegistrationForm, LoginForm, AdminRegistrationForm, AddProductRequestForm, EditProductRequestForm
from django.db import models
from .forms import MessageToAdminForm
import json
from .models import Product, Category, Review
from .forms import ReviewForm
from django.views.decorators.http import require_POST

def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.order_by('-created_at')
    categories = Category.objects.all()
    
    # Сохраняем поисковый запрос
    if query:
        products = products.filter(name__icontains=query)
    
    # ====== СОРТИРОВКА ======
    sort = request.GET.get('sort', 'newest')
    
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    else:  # newest
        products = products.order_by('-created_at')
    
    cart = get_cart(request)
    cart_items_count = cart.items.count() if cart else 0
    
    return render(request, 'products/index.html', {
        'products': products,
        'categories': categories,
        'cart_items_count': cart_items_count,
        'current_sort': sort,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    
    # Обновляем среднюю оценку
    if reviews.exists():
        avg = sum([r.rating for r in reviews]) / reviews.count()
        product.aver_rating = round(avg, 2)
        product.rating_count = reviews.count()
        product.save(update_fields=['aver_rating', 'rating_count'])
    
    # Получаем выбранную вариацию
    variant_id = request.GET.get('variant')
    selected_variant = None
    
    if product.has_variants and product.variants.exists():
        if variant_id:
            try:
                selected_variant = product.variants.get(id=variant_id, is_active=True)
            except ProductVariant.DoesNotExist:
                selected_variant = product.variants.filter(is_active=True).first()
        else:
            selected_variant = product.variants.filter(is_active=True).first()
    
    cart_item = None
    if request.user.is_authenticated:
        cart = get_cart(request)
        if cart:
            cart_item = CartItem.objects.filter(
                cart=cart, 
                product=product,
                variant=selected_variant
            ).first()
    
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if not user_review:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Ваш отзыв успешно добавлен!')
                return redirect('products:product_detail', slug=product.slug)
        else:
            messages.warning(request, 'Вы уже оставили отзыв на этот товар')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ReviewForm()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'categories': categories,
        'reviews': reviews,
        'review_form': form,
        'user_review': user_review,
        'selected_variant': selected_variant,
        'cart_item': cart_item,
    })
    

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    
    sort = request.GET.get('sort', 'newest')
    
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('-created_at')
    
    return render(request, 'products/category_products.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
    })

# РЕГИСТРАЦИЯ (для гостей - обычная)
# def register(request):
#     if request.user.is_authenticated:
#         return redirect('products:product_list')
    
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = User.Role.GUEST  # Обычные пользователи получают роль гостя
#             user.save()
#             login(request, user)
#             messages.success(request, f'Добро пожаловать, {user.username}!')
#             return redirect('products:product_list')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = RegistrationForm()
    
#     return render(request, 'products/register.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('products:product_list')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = RegistrationForm()
    
    return render(request, 'products/register.html', {'form': form})

#  АДМИНОМ (для создания менеджеров и админов)
def is_admin(user):
    return user.role=='admin' or user.is_superuser
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'products/admin/users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Пользователь {user.username} создан с ролью {user.get_role_display()}')
            return redirect('products:user_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = AdminRegistrationForm()
    
    return render(request, 'products/admin/admin_register.html', {'form': form})

def is_manager(user):
    return user.role in ['manager', 'admin'] or user.is_superuser

def is_admin(user):
    return user.role == 'admin' or user.is_superuser

# ==АДМИН ЗАЯВЫ==
@login_required
@user_passes_test(is_manager)
def my_requests(request):
    requests_list = Request.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'products/requests/my_requests.html', {'requests': requests_list})

@login_required
@user_passes_test(is_admin)
def pending_requests(request):
    pending_reqs = Request.objects.filter(status=Request.Status.PENDING).order_by('-created_at')
    return render(request, 'products/requests/pending_requests.html', {'requests': pending_reqs})

@login_required
@user_passes_test(is_admin)
def moderate_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_response = request.POST.get('admin_response', '')
        
        if action == 'approve':
            try:
                if req.type == 'add_product':
                    data = req.data
                    Product.objects.create(
                        name=data.get('name'),
                        price=data.get('price'),
                        description=data.get('description', ''),
                        amount=int(data.get('amount', 0)),
                        brand_id=data.get('brand'),
                        category_id=data.get('category'),
                    )
                elif req.type == 'edit_product':
                    data = req.data
                    product = get_object_or_404(Product, id=data.get('product'))
                    if data.get('name'):
                        product.name = data['name']
                    if data.get('price'):
                        product.price = data['price']
                    if data.get('description'):
                        product.description = data['description']
                    if data.get('amount'):
                        product.amount = data['amount']
                    product.save()
                elif req.type == 'message':
                    pass # не прочитаным и буит
                
                req.status = Request.Status.APPROVED
                messages.success(request, f'Заявка #{req.id} одобрена')
                
            except Exception as e:
                messages.error(request, f'Ошибка при выполнении заявки: {e}')
                req.status = Request.Status.REJECTED
                admin_response = f"{admin_response}\nОшибка: {str(e)}"
        
        elif action == 'reject':
            req.status = Request.Status.REJECTED
            messages.warning(request, f'Заявка #{req.id} отклонена')
        
        req.reviewed_by = request.user
        req.admin_response = admin_response
        req.save()
        
        return redirect('products:pending_requests')
    
    return render(request, 'products/requests/moderate_request.html', {'request': req})

    


# ==МАНАГЕР ЗАЯВЫ==
@login_required
@user_passes_test(is_manager)
def create_request(request, type):
    
    if type == 'add_product':
        form = AddProductRequestForm(request.POST or None)
        title = "Заявка на добавление товара"
        template = 'products/requests/add_product_request.html'
    elif type == 'edit_product':
        form = EditProductRequestForm(request.POST or None)
        title = "Заявка на редактирование товара"
        template = 'products/requests/edit_product_request.html'
    else:
        messages.error(request, 'Неверный тип заявки')
        return redirect('products:requests_list')
    
    if request.method == 'POST':
        if form.is_valid():
            # JSON
            data = {}
            for field, value in form.cleaned_data.items():
                if value is not None:
                    if hasattr(value, 'id'):
                        data[field] = value.id
                    else:
                        data[field] = str(value) if not isinstance(value, (int, float, bool)) else value
            
            Request.objects.create(
                created_by=request.user,
                type=type,
                data=data,
                comment=form.cleaned_data.get('comment', '')
            )
            messages.success(request, 'Заявка успешно создана и отправлена администратору!')
            return redirect('products:my_requests')
    
    return render(request, template, {'form': form, 'title': title})

@login_required
@user_passes_test(is_manager)
def my_requests(request):
    requests_list = Request.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'products/requests/my_requests.html', {'requests': requests_list})


@login_required
@user_passes_test(is_admin)
def change_user_role(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in [User.Role.BUYER, User.Role.MANAGER]:
            target_user.role = new_role
            target_user.save()
            messages.success(request, f'Роль пользователя {target_user.username} изменена на {target_user.get_role_display()}')
        else:
            messages.error(request, 'Недопустимая роль')
    
    return redirect('products:user_list')


# ВХОД
def user_login(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'С возвращением, {username}!')
                return redirect('products:product_list')
        messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'products/login.html', {'form': form})

# ВЫХОД
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('products:product_list')

# ПРОФИЛЬ
@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'products/profile.html', {
        'user': request.user,
        'orders': orders,
    })

User = get_user_model()

def get_cart(request):
    if request.user.is_authenticated:
        if not hasattr(request.user, 'cart'):
            Cart.objects.create(user=request.user)
        return request.user.cart
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
            return cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    variant_id = request.POST.get('variant_id') or request.GET.get('variant_id')
    variant = None
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
    
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id)
        stock_available = variant.amount
    else:
        stock_available = product.amount
    
    if stock_available <= 0:
        messages.error(request, 'Товар временно отсутствует на складе')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    if quantity > stock_available:
        messages.warning(request, f'Доступно только {stock_available} шт.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    cart_item = CartItem.objects.filter(cart=cart, product=product, variant=variant).first()
    
    if cart_item:
        if cart_item.quantity + quantity > stock_available:
            messages.warning(request, f'Доступно только {stock_available} шт.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Количество увеличено до {cart_item.quantity}')
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            variant=variant,
            quantity=quantity,
            price_at_moment=variant.get_price() if variant else product.price
        )
        messages.success(request, f'Товар добавлен в корзину')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def cart_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Для просмотра корзины необходимо авторизоваться')
        return redirect('products:login')
    cart = get_cart(request)
    items = cart.items.all() if cart else []
    total_price = cart.get_total_price() if cart else 0
    
    return render(request, 'products/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
    })

def remove_from_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = item.product.name
    item.delete()
    messages.success(request, f'{product_name} удалён из корзины')
    return redirect('products:cart_view')

def categories_list(request):
    categories = Category.objects.all().annotate(
        products_count=models.Count('products')
    )
    return render(request, 'products/categories.html', {'categories': categories})

@login_required
@user_passes_test(is_manager)
def message_to_admin(request):
    
    if request.method == 'POST':
        form = MessageToAdminForm(request.POST)
        if form.is_valid():
            data = {
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
                'priority': form.cleaned_data['priority'],
                'from_user': request.user.username,
                'from_user_id': request.user.id,
            }
            
            Request.objects.create(
                created_by=request.user,
                type='message',
                data=data,
                comment=form.cleaned_data['subject']
            )
            messages.success(request, 'Ваше сообщение отправлено администратору!')
            return redirect('products:my_requests')
    else:
        form = MessageToAdminForm()
    
    return render(request, 'products/requests/message_to_admin.html', {'form': form})

# Реализация ордеров
def cart_view(request):
    cart = get_cart(request)
    items = cart.items.all() if cart else []
    total_price = sum(item.get_total() for item in items)
    
    return render(request, 'products/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
    })

def remove_from_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, 'Товар удалён из корзины')
    return redirect('products:cart_view')

def update_cart_quantity(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            messages.error(request, 'Некорректное значение')
            return redirect('products:cart_view')
        
        # Получаем остаток на складе
        if item.variant:
            stock_available = item.variant.amount
        else:
            stock_available = item.product.amount
        
        if new_quantity <= 0:
            item.delete()
            messages.success(request, 'Товар удалён из корзины')
        elif new_quantity > stock_available:
            messages.warning(request, f'Доступно только {stock_available} шт.')
        else:
            item.quantity = new_quantity
            item.save()
            messages.success(request, 'Количество обновлено')
    
    return redirect('products:cart_view')

def checkout(request):
    cart = get_cart(request)
    items = cart.items.all()
    
    if not items:
        messages.error(request, 'Корзина пуста')
        return redirect('products:cart_view')
    
    last_orders = None
    if request.user.is_authenticated:
        last_orders = Order.objects.filter(
            user=request.user
        ).exclude(
            address__isnull=True,
            phone__isnull=True
        ).order_by('-created_at')[:5]
    
    if request.method == 'POST':
        selected_item_ids = request.POST.getlist('selected_items')
        
        if not selected_item_ids:
            messages.error(request, 'Выберите хотя бы один товар для заказа')
            return redirect('products:checkout')
        
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        comment = request.POST.get('comment', '')
        
        selected_items = items.filter(id__in=selected_item_ids)
        
        if not selected_items:
            messages.error(request, 'Выбранные товары не найдены')
            return redirect('products:checkout')
        
        total_price = sum(item.get_total() for item in selected_items)
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if not request.user.is_authenticated else None,
            total_amount=total_price,
            address=address,
            phone=phone,
            comment=comment
        )
        
        for item in selected_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                variant_name=item.variant.name if item.variant else '',
                quantity=item.quantity,
                price_at_moment=item.price_at_moment
            )
            item.delete()
        
        messages.success(request, f'Заказ #{order.id} успешно оформлен!')
        return redirect('products:order_detail', order_id=order.id)
    
    total_price = sum(item.get_total() for item in items)
    return render(request, 'products/checkout.html', {
        'items': items,
        'total_price': total_price,
        'last_orders': last_orders,
    })

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.user.is_authenticated:
        if order.user != request.user and not request.user.is_admin():
            messages.error(request, 'У вас нет доступа к этому заказу')
            return redirect('products:product_list')
    
    # Привязываем изображение: сначала пробуем найти вариацию по имени, иначе используем изображение продукта (если есть)
    items = list(order.items.all())
    for item in items:
        image_url = ''
        try:
            product = Product.objects.filter(name=item.product_name).first()
            if product:
                if item.variant_name:
                    variant = product.variants.filter(name=item.variant_name).first()
                    if variant and variant.image:
                        image_url = variant.image.url
                if not image_url and product.image:
                    image_url = product.image.url
        except Exception:
            image_url = ''
        item.image_url = image_url

    return render(request, 'products/order_detail.html', {'order': order, 'items': items})

@login_required
@user_passes_test(is_admin)
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'products/admin/all_orders.html', {'orders': orders})

@login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in Order.Status.choices]:
            order.status = new_status
            order.save()
            messages.success(request, f'Статус заказа #{order.id} обновлён')
    
    return redirect('products:all_orders')

@login_required
def profile_update(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        user = request.user
        if email:
            user.email = email
        if phone:
            user.phone = phone
        user.save()
        
        messages.success(request, 'Профиль успешно обновлён')
        return redirect('products:profile')
    
    return redirect('products:profile')

#ОТЗЫВЫ
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')

    if request.method == 'POST':
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            messages.warning(request, 'Для отправки отзыва необходимо авторизоваться')
            return redirect('products:login')
    
    # Обновляем среднюю оценку
    if reviews.exists():
        avg = sum([r.rating for r in reviews]) / reviews.count()
        product.aver_rating = round(avg, 2)
        product.rating_count = reviews.count()
        product.save(update_fields=['aver_rating', 'rating_count'])
    
    # Проверяем, может ли пользователь оставить отзыв
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if not user_review:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Ваш отзыв успешно добавлен!')
                return redirect('products:product_detail', slug=product.slug)
        else:
            messages.warning(request, 'Вы уже оставили отзыв на этот товар')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ReviewForm()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'categories': categories,
        'reviews': reviews,
        'review_form': form,
        'user_review': user_review,
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if not request.user.is_superuser and request.user.role not in ['admin', 'manager']:
        messages.error(request, 'У вас нет прав на удаление отзывов')
        return redirect('products:product_detail', slug=review.product.slug)
    
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Отзыв успешно удалён')
    return redirect('products:product_detail', slug=product_slug)

@login_required
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Проверка прав: только админ или менеджер
    if not request.user.is_superuser and request.user.role not in ['admin', 'manager']:
        messages.error(request, 'У вас нет прав для ответа на отзывы')
        return redirect('products:product_detail', slug=review.product.slug)
    
    if request.method == 'POST':
        admin_reply = request.POST.get('admin_reply', '').strip()
        if admin_reply:
            review.admin_reply = admin_reply
            review.admin_replied_at = timezone.now()
            review.admin_replied_by = request.user
            review.save()
            messages.success(request, 'Ответ на отзыв успешно добавлен')
        else:
            messages.error(request, 'Ответ не может быть пустым')
        return redirect('products:product_detail', slug=review.product.slug)
    
    return redirect('products:product_detail', slug=review.product.slug)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Проверяем, можно ли отменить заказ (только если статус не завершён и не отменён)
    if order.status in ['completed', 'cancelled']:
        messages.warning(request, 'Этот заказ уже нельзя отменить')
        return redirect('products:profile')
    
    order.status = 'cancelled'
    order.save()
    messages.success(request, f'Заказ #{order.id} успешно отменён')
    
    # Возвращаемся туда, откуда пришли
    next_url = request.META.get('HTTP_REFERER', 'products:profile')
    return redirect(next_url)

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user.is_superuser:
        messages.error(request, 'Нельзя удалить суперпользователя')
        return redirect('products:user_list')
    
    if target_user == request.user:
        messages.error(request, 'Нельзя удалить самого себя')
        return redirect('products:user_list')
    
    target_user.delete()
    messages.success(request, f'Пользователь {target_user.username} удалён')
    return redirect('products:user_list')

# интерактивная панель добавления в корзину и изменения количества
@login_required
@require_POST
def update_cart_item_ajax(request, item_id):
    """Обновление количества в корзине через AJAX"""
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    try:
        delta = int(request.POST.get('delta', 0))
        new_quantity = item.quantity + delta
    except ValueError:
        return JsonResponse({'error': 'Неверное значение'}, status=400)
    
    if item.variant:
        stock_available = item.variant.amount
    else:
        stock_available = item.product.amount
    
    if new_quantity <= 0:
        item.delete()
        return JsonResponse({
            'success': True,
            'action': 'removed',
            'item_id': item_id,
        })
    elif new_quantity > stock_available:
        return JsonResponse({
            'error': f'Доступно только {stock_available} шт.'
        }, status=400)
    else:
        item.quantity = new_quantity
        item.save()
        return JsonResponse({
            'success': True,
            'action': 'updated',
            'item_id': item_id,
            'quantity': new_quantity,
            'total': float(item.get_total()),
            'cart_total': float(get_cart(request).get_total_price()),
        })

@login_required
@require_POST
def remove_from_cart_ajax(request, item_id):
    """Удаление товара из корзины через AJAX"""
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return JsonResponse({
        'success': True,
        'action': 'removed',
        'item_id': item_id,
    })

