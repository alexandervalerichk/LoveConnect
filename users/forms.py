from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Добавляем city и gender сразу при регистрации
        fields = ('username', 'email', 'city', 'gender', 'birth_date', 'goal', 'avatar')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # --- ДОБАВЛЯЕМ НОВЫЕ ПОЛЯ ИЗ ТЗ ---
        fields = (
            'city', 'gender', 'looking_for_gender', # Кто я и кого ищу
            'goal', 'birth_date', 
            'height', 'weight', 
            'interests', 'about', 
            'avatar',
            # Те самые 3 вопроса
            'question1', 'question2', 'question3'
        )
        widgets = {
            'city': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'looking_for_gender': forms.Select(attrs={'class': 'form-select'}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
            
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '170'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '60'}),
            
            'interests': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Например: джаз, путешествия, коты'}),
            'about': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            
            'question1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Какой твой идеальный выходной?'}),
            'question2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Твое любимое блюдо?'}),
            'question3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Кошки или собаки?'}),
            
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }