from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Request, Product, Brand, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтверждение пароля'})

# Форма регистрации для админа (с выбором роли)
class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}))
    role = forms.ChoiceField(choices=User.Role.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтверждение пароля'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.BUYER
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})

class AddProductRequestForm(forms.Form):
    name = forms.CharField(max_length=255, label="Название товара", widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Цена", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), label="Описание", required=False)
    amount = forms.IntegerField(label="Количество", initial=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label="Бренд", widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label="Комментарий", required=False)

class EditProductRequestForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Товар", widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=255, label="Новое название", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Новая цена", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), label="Новое описание", required=False)
    amount = forms.IntegerField(label="Новое количество", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label="Комментарий", required=False)

class MessageToAdminForm(forms.Form):
    subject = forms.CharField(max_length=200, label="Тема", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кратко опишите суть'}))
    message = forms.CharField(label="Сообщение", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Подробно опишите проблему или предложение...'}))
    priority = forms.ChoiceField(
        choices=[('low', 'Низкий'), ('medium', 'Средний'), ('high', 'Высокий')],
        label="Приоритет",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} ★") for i in range(1, 6)], attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Поделитесь своим впечатлением о товаре...'}),
        }
        labels = {
            'rating': 'Оценка',
            'text': 'Текст отзыва',
        }