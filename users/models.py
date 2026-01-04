from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class CustomUser(AbstractUser):
    # --- 10. СПИСОК ГОРОДОВ ИЗРАИЛЯ ---
    # --- 10. СПИСОК ГОРОДОВ ИЗРАИЛЯ ---
    CITY_CHOICES = (
        # ТОП Города
        ('jerusalem', 'Иерусалим'), 
        ('tlv', 'Тель-Авив'), 
        ('haifa', 'Хайфа'),
        ('rishon', 'Ришон-ле-Цион'), 
        ('ashdod', 'Ашдод'), 
        ('beersheva', 'Беэр-Шева'),
        ('netanya', 'Нетания'),
        
        ('divider', '————'), # Разделитель
        
        # Полный список по алфавиту
        ('akko', 'Акко'), 
        ('arad', 'Арад'), 
        ('ariel', 'Ариэль'), 
        ('afula', 'Афула'),
        ('ashkelon', 'Ашкелон'), 
        ('baka', 'Бака-эль-Гарбия'),
        ('batyam', 'Бат-Ям'), 
        ('beitar', 'Бейтар-Илит'),
        ('beitshean', 'Бейт-Шеан'),
        ('beitshemesh', 'Бейт-Шемеш'), 
        ('beeryakov', 'Беэр-Яаков'),
        ('bneibrak', 'Бней-Брак'), 
        ('gefer', 'Гефер-Явне'),
        ('herzliya', 'Герцлия'),
        ('givataim', 'Гиватаим'), 
        ('givatshmuel', 'Гиват-Шмуэль'),
        ('dimona', 'Димона'), 
        ('elad', 'Елaд'),
        ('yehud', 'Йехуд-Моноссон'),
        ('yokneam', 'Йокнеам-Илит'),
        ('karmiel', 'Кармиэль'), 
        ('cesarea', 'Кесария'),
        ('kalansua', 'Калансуа'),
        ('kafrkase', 'Кафр-Касем'),
        ('kfar_sava', 'Кфар-Сава'), 
        ('kiryatata', 'Кирьят-Ата'),
        ('kiryatbialik', 'Кирьят-Бялик'),
        ('kiryatgat', 'Кирьят-Гат'),
        ('kiryatmalahi', 'Кирьят-Малахи'),
        ('kiryatmotzkin', 'Кирьят-Моцкин'),
        ('kiryatono', 'Кирьят-Оно'),
        ('kiryatshmona', 'Кирьят-Шмона'),
        ('kiryatyam', 'Кирьят-Ям'),
        ('lod', 'Лод'),
        ('maale', 'Маале-Адумим'),
        ('maalot', 'Маалот-Таршиха'),
        ('migdal', 'Мигдаль-ха-Эмек'),
        ('modiinilit', 'Модиин-Илит'),
        ('modiin', 'Модиин-Маккабим-Реут'),
        ('nazareth', 'Назарет'), 
        ('nahariya', 'Нагария'), 
        ('ofakim', 'Офаким'),
        ('petah_tikva', 'Петах-Тиква'),
        ('raanana', 'Раанана'), 
        ('ramat_gan', 'Рамат-Ган'), 
        ('ramatsharon', 'Рамат-ха-Шарон'),
        ('ramla', 'Рамла'),
        ('rahat', 'Рахат'),
        ('rehovot', 'Реховот'),
        ('rosh', 'Рош-ха-Аин'),
        ('sderot', 'Сдерот'),
        ('tiberias', 'Тверия'), 
        ('tlv_jaffa', 'Тель-Авив-Яффо'),
        ('tira', 'Тира'),
        ('tirat', 'Тират-Кармиш'),
        ('umm', 'Умм-эль-Фахм'),
        ('hader', 'Хадера'),
        ('holon', 'Холон'),
        ('eilat', 'Эйлат'),
        ('other', 'Другой город'),
    )

    # --- УРОВНИ ПОДПИСКИ ---
    SUBSCRIPTION_CHOICES = (
        ('free', 'Free'),
        ('gold', 'Gold ⭐️'),
        ('vip', 'VIP 👑'),
    )

    # --- ПОЛ И ЦЕЛИ (Учли пункт 9 про пары) ---
    GENDER_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
        ('couple', 'Пара М+Ж'), # Для свингеров или поиска друзей семье
    )
    
    # Пункт 6: Цели знакомства
    GOAL_CHOICES = (
        ('friendship', 'Дружба/Общение'), # Видят всех
        ('serious', 'Серьезные отношения'),
        ('date_evening', 'Свидание на вечер'), # Только выбранный пол
        ('travel', 'Попутчики'),
    )

    # --- ОСНОВНЫЕ ПОЛЯ ---
    subscription = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default='free', verbose_name="Статус")
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default='tlv', verbose_name="Город")
    
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Кто вы")
    looking_for_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female', verbose_name="Кого ищете")
    
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='serious', verbose_name="Цель")
    
    # Физика
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name="Рост (см)")
    weight = models.PositiveIntegerField(null=True, blank=True, verbose_name="Вес (кг)")
    
    # Текст
    about = models.TextField(blank=True, verbose_name="О себе")
    interests = models.TextField(blank=True, verbose_name="Интересы (теги)")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Фото")
    
    # --- ГЕОЛОКАЦИЯ ---
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")

    # --- 3. ТРИ ВОПРОСА (Айсбрейкеры) ---
    question1 = models.CharField(max_length=100, blank=True, verbose_name="Вопрос 1 (для гостей)")
    question2 = models.CharField(max_length=100, blank=True, verbose_name="Вопрос 2")
    question3 = models.CharField(max_length=100, blank=True, verbose_name="Вопрос 3")

    # Для SEO (Meta description пользователя) - Пункт 10
    def get_meta_description(self):
        return f"{self.username}, {self.get_city_display()}. Ищу: {self.get_goal_display()}."

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    def __str__(self):
        return self.username

# --- 2. МОДЕЛЬ РЕАКЦИЙ (Лайки, Избранное) ---
class Reaction(models.Model):
    REACTION_TYPES = (
        ('like', '❤️ Лайк'),
        ('star', '⭐️ Избранное'),
        ('check', '✅ Готов встретиться'),
    )
    
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_reactions')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reactions')
    type = models.CharField(max_length=10, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver', 'type') # Чтобы нельзя было лайкнуть дважды

        # --- МОДЕЛЬ ЧАТА ---
class ChatMessage(models.Model):
    ROOM_CHOICES = (
        ('general', '📢 Общий чат'),
        ('tlv', '🏖️ Тель-Авив тусовка'),
        ('relationships', '❤️ Про отношения'),
        ('hobby', '🎨 Хобби и интересы'),
        ('travel', '🚗 Попутчики по Израилю'),
    )
    
    room = models.CharField(max_length=20, choices=ROOM_CHOICES, verbose_name="Комната")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время")

    class Meta:
        ordering = ['created_at'] # Старые сообщения сверху, новые снизу

    def __str__(self):
        return f"{self.user} in {self.room}: {self.text[:20]}"

# --- 4. МОДЕЛЬ ОТВЕТОВ НА ВОПРОСЫ ---
class Answer(models.Model):
    responder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_answers', verbose_name="Кто ответил")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_answers', verbose_name="Кому ответили")
    
    # Мы храним номер вопроса (1, 2 или 3), на который ответили
    question_number = models.IntegerField(choices=((1, 'Вопрос 1'), (2, 'Вопрос 2'), (3, 'Вопрос 3')), verbose_name="Номер вопроса")
    question_text = models.CharField(max_length=100, verbose_name="Текст вопроса") # Копируем текст вопроса на случай если его поменяют
    answer_text = models.TextField(verbose_name="Ответ")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата ответа")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ответ от {self.responder} для {self.receiver}"

# --- 5. ЛИЧНЫЕ СООБЩЕНИЯ (VIP) ---
class DirectMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_direct_messages', verbose_name="Отправитель")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_direct_messages', verbose_name="Получатель")
    text = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение от {self.sender} к {self.receiver}"