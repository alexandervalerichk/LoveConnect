from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Reaction, ChatMessage, Answer, DirectMessage
from django.utils.html import format_html

# 1. КАСТОМНАЯ АДМИНКА ПОЛЬЗОВАТЕЛЕЙ
class CustomUserAdmin(UserAdmin):
    # Поля, которые отображаются в списке
    list_display = ('username', 'get_avatar', 'email', 'subscription', 'city', 'gender', 'goal', 'date_joined')
    
    # Поля, по которым можно фильтровать справа
    list_filter = ('subscription', 'city', 'gender', 'goal', 'is_staff', 'date_joined')
    
    # Поля для поиска
    search_fields = ('username', 'email', 'city')
    
    # Сортировка по умолчанию
    ordering = ('-date_joined',)
    
    # Группировка полей внутри карточки пользователя
    fieldsets = UserAdmin.fieldsets + (
        ('Dating Profile', {'fields': ('subscription', 'city', 'birth_date', 'gender', 'looking_for_gender', 'goal', 'avatar')}),
        ('Physical', {'fields': ('height', 'weight')}),
        ('About', {'fields': ('about', 'interests')}),
        ('Location', {'fields': ('latitude', 'longitude')}),
        ('Questions', {'fields': ('question1', 'question2', 'question3')}),
    )
    
    # Отображение аватарки в списке
    def get_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="30" height="30" style="border-radius:50%;" />', obj.avatar.url)
        return "👤"
    get_avatar.short_description = 'Фото'

# 2. АДМИНКА ЧАТОВ (Модерация)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'text_preview', 'created_at')
    list_filter = ('room', 'created_at')
    search_fields = ('text', 'user__username')
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Сообщение'

# 3. АДМИНКА РЕАКЦИЙ (Аналитика)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'type', 'created_at')
    list_filter = ('type', 'created_at')

# Регистрация моделей
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Reaction, ReactionAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Answer)
admin.site.register(DirectMessage)
