from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from datetime import date
import random

# Подключаем наши модели и формы
from .models import CustomUser, Reaction, ChatMessage, Answer
from .forms import CustomUserCreationForm, UserUpdateForm

# --- 1. БАЗОВЫЕ СТРАНИЦЫ ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

# --- 2. УМНЫЙ ПОИСК (С защитой от перегрузки) ---
@login_required
def users_list(request):
    current_user = request.user
    
    # Исключаем себя и админов
    users = CustomUser.objects.exclude(id=current_user.id).filter(is_superuser=False)

    # Логика пола (Пункты 6 и 9 ТЗ)
    if current_user.goal != 'friendship':
        # Если не дружба - ищем только нужный пол
        users = users.filter(gender=current_user.looking_for_gender)
        # И показываем только тех, кто ищет нас (или ищет дружбу)
        users = users.filter(Q(looking_for_gender=current_user.gender) | Q(goal='friendship'))

    # Фильтры из формы (users_list.html)
    if request.GET.get('city'):
        users = users.filter(city=request.GET.get('city'))
    if request.GET.get('gender'):
        users = users.filter(gender=request.GET.get('gender'))

    # Фильтр по возрасту
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    if min_age and max_age:
        today = date.today()
        try:
            min_date = today.replace(year=today.year - int(max_age) - 1)
            max_date = today.replace(year=today.year - int(min_age))
            users = users.filter(birth_date__range=[min_date, max_date])
        except ValueError:
            pass

    # Ограничиваем выдачу 100 анкетами для скорости
    users = users[:100]

    return render(request, 'users_list.html', {
        'users': users,
        'CITY_CHOICES': CustomUser.CITY_CHOICES,
        'GENDER_CHOICES': CustomUser.GENDER_CHOICES,
    })

# --- 3. АНКЕТА И РЕАКЦИИ ---
@login_required
def user_detail(request, pk):
    user_obj = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'user_detail.html', {'user_obj': user_obj})

@login_required
def send_reaction(request, pk, type_key):
    receiver = get_object_or_404(CustomUser, pk=pk)
    if request.user != receiver:
        Reaction.objects.update_or_create(
            sender=request.user, receiver=receiver, defaults={'type': type_key}
        )
    return redirect('user_detail', pk=pk)

# --- 4. ВОПРОСЫ И ОТВЕТЫ ---
@login_required
def answer_question(request, pk, q_num):
    receiver = get_object_or_404(CustomUser, pk=pk)
    
    # Получаем текст вопроса из базы
    question_text = ""
    if q_num == 1: question_text = receiver.question1
    elif q_num == 2: question_text = receiver.question2
    elif q_num == 3: question_text = receiver.question3
    
    if request.method == 'POST':
        text = request.POST.get('answer_text')
        if text:
            Answer.objects.create(
                responder=request.user, receiver=receiver,
                question_number=q_num, question_text=question_text, answer_text=text
            )
            return redirect('user_detail', pk=pk)
            
    # Если файла answer_form.html нет, создай его (код был выше)
    return render(request, 'answer_form.html', {
        'receiver': receiver,
        'question_text': question_text,
        'q_num': q_num
    })

@login_required
def my_answers(request):
    # Показываем ответы мне + помечаем их прочитанными (опционально)
    answers = Answer.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'my_answers.html', {'answers': answers})

# --- 5. ЧАТЫ ---
@login_required
def chat_rooms(request):
    return render(request, 'chat_rooms.html', {'rooms': ChatMessage.ROOM_CHOICES})

@login_required
def room_detail(request, room_name):
    valid_rooms = dict(ChatMessage.ROOM_CHOICES)
    if room_name not in valid_rooms: return redirect('chat_rooms')

    if request.method == 'POST':
        text = request.POST.get('message')
        if text:
            ChatMessage.objects.create(room=room_name, user=request.user, text=text)
            return redirect('room_detail', room_name=room_name)

    messages = ChatMessage.objects.filter(room=room_name).select_related('user').order_by('created_at')[:50]
    return render(request, 'room_detail.html', {
        'room_name': room_name, 'room_display': valid_rooms[room_name], 'messages': messages
    })

# --- 6. ШЕЙКЕР API ---
def shaker_api(request):
    options = [
        "🃏 <b>Факт:</b> Если бы вы были фильмом, это была бы романтическая комедия.",
        "🔮 <b>Предсказание:</b> Ваша следующая встреча пройдет в уютной кофейне.",
        "💡 <b>Совет:</b> Спросите собеседника про самое странное путешествие в его жизни.",
        "❤️ <b>Комплимент:</b> Ваша улыбка может осветить весь Тель-Авив ночью.",
        "🎲 <b>Вопрос:</b> Если бы у вас был миллион шекелей, на что бы вы его потратили за час?",
        "📍 <b>Идея:</b> Прогулка по набережной Тель-Авива на закате.",
        "📍 <b>Место:</b> Секретный бар в Яффо.",
    ]
    return JsonResponse({'text': random.choice(options)})