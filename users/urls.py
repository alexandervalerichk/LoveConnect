from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/', views.users_list, name='users_list'),
    
    # Реакции
    path('reaction/<int:pk>/<str:type_key>/', views.send_reaction, name='send_reaction'),
    
    # Шейкер
    path('api/shake/', views.shaker_api, name='shaker_api'),
    
    # Чаты
    path('chat/', views.chat_rooms, name='chat_rooms'),
    path('chat/<str:room_name>/', views.room_detail, name='room_detail'),
    
    # Вопросы и Ответы
    # Вопросы и Ответы
    path('answer/<int:user_id>/<int:question_number>/', views.answer_question, name='answer_question'),
    path('my-answers/', views.my_answers, name='my_answers'),
    
    # Главная страница
    path('', views.home, name='home'),
]
