from django.contrib import admin
from django.urls import path, include
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Главная и Auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Поиск и Анкета
    path('search/', views.users_list, name='users_list'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    
    # Интерактив
    path('reaction/<int:pk>/<str:type_key>/', views.send_reaction, name='send_reaction'),
    path('answer/<int:pk>/<int:q_num>/', views.answer_question, name='answer_question'),
    path('my-answers/', views.my_answers, name='my_answers'),
    
    # Чаты
    path('chats/', views.chat_rooms, name='chat_rooms'),
    path('chats/<str:room_name>/', views.room_detail, name='room_detail'),
    
    # API
    path('api/shake/', views.shaker_api, name='shaker_api'),
]

# Раздача фоток в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)