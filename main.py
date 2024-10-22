import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import random
import asyncio

API_TOKEN = '7912812196:AAGu9YWhQ0W7KMYjgTbPOqkVT4X3pwkAwc4'  # Вставьте ваш токен бота

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список блюд с категориями, описанием, временем приготовления, ссылками на рецепты и рестораны
meals = [
    # Закуски
    {"name": "🍕 Пицца", 
     "category": "Закуски", 
     "description": "Классическая итальянская пицца с хрустящей корочкой, сочным томатным соусом, расплавленным сыром и свежими ингредиентами. Идеальный выбор для вкусного обеда или ужина.", 
     "time": 40, 
     "ingredients": ["тесто", "сыр", "помидоры"], 
     "recipe_link": "https://example.com/pizza", 
     "restaurant_link": "https://pizzahut.com/pizza"},
    
    {"name": "🍣 Роллы", 
     "category": "Закуски", 
     "description": "Нежные японские роллы с рисом, свежей рыбой и морскими водорослями. Это идеальное сочетание свежести и вкуса, которое покорит вашего внутреннего гурмана.", 
     "time": 50, 
     "ingredients": ["рис", "рыба", "водоросли"], 
     "recipe_link": "https://example.com/rolls", 
     "restaurant_link": "https://restaurant.com/rolls"},
    
    # Салаты
    {"name": "🥗 Салат Цезарь", 
     "category": "Салаты", 
     "description": "Легендарный салат с хрустящими листьями салата, нежной курицей, золотистыми гренками и пикантным соусом на основе пармезана. Легкий и сытный вариант для любого приема пищи.", 
     "time": 20, 
     "ingredients": ["курица", "листья салата", "сыр"], 
     "recipe_link": "https://example.com/caesar-salad", 
     "restaurant_link": "https://olivegarden.com/caesar-salad"},
    
    {"name": "🥔 Оливье", 
     "category": "Салаты", 
     "description": "Традиционный русский салат с отварным картофелем, маринованными огурцами, колбасой и майонезом. Классика праздничного стола, любимая многими с детства.", 
     "time": 35, 
     "ingredients": ["картофель", "колбаса", "огурцы"], 
     "recipe_link": "https://example.com/olivier", 
     "restaurant_link": "https://restaurant.com/olivier"},
    
    # Супы
    {"name": "🍲 Борщ", 
     "category": "Супы", 
     "description": "Насыщенный и ароматный борщ на основе свеклы, капусты и мяса. Это традиционное блюдо согреет и подарит насыщенный вкус настоящей русской кухни.", 
     "time": 90, 
     "ingredients": ["свекла", "капуста", "мясо"], 
     "recipe_link": "https://example.com/borshch", 
     "restaurant_link": "https://restaurant.com/borshch"},
    
    {"name": "🍜 Куринный суп", 
     "category": "Супы", 
     "description": "Легкий и питательный куриный суп с овощами. Простое и полезное блюдо, которое идеально подходит для легкого обеда или ужина.", 
     "time": 30, 
     "ingredients": ["курица", "морковь", "лук"], 
     "recipe_link": "https://example.com/soup", 
     "restaurant_link": "https://restaurant.com/soup"},
    
    # Основные блюда
    {"name": "🍝 Паста", 
     "category": "Основные блюда", 
     "description": "Итальянская паста с томатным соусом и расплавленным сыром. Идеальное блюдо для тех, кто любит простую, но невероятно вкусную средиземноморскую кухню.", 
     "time": 25, 
     "ingredients": ["паста", "томаты", "сыр"], 
     "recipe_link": "https://example.com/pasta", 
     "restaurant_link": "https://restaurant.com/pasta"},
    
    {"name": "🥩 Стейк", 
     "category": "Основные блюда", 
     "description": "Сочный и ароматный стейк, приготовленный до идеальной степени прожарки. Для истинных ценителей мяса, которые не боятся экспериментировать с вкусом.", 
     "time": 60, 
     "ingredients": ["мясо", "специи"], 
     "recipe_link": "https://example.com/steak", 
     "restaurant_link": "https://restaurant.com/steak"},
    
    # Десерты
    {"name": "🥞 Блинчики", 
     "category": "Десерты", 
     "description": "Тонкие, нежные блинчики с разнообразными начинками. Простой и вкусный десерт, который можно приготовить на завтрак или подать к чаю.", 
     "time": 30, 
     "ingredients": ["молоко", "мука", "яйца"], 
     "recipe_link": "https://example.com/pancakes", 
     "restaurant_link": "https://restaurant.com/pancakes"},
    
    {"name": "🍰 Торт Наполеон", 
     "category": "Десерты", 
     "description": "Легендарный торт Наполеон из слоеного теста с нежным кремом. Изысканный десерт для сладкоежек и настоящих гурманов.", 
     "time": 120, 
     "ingredients": ["мука", "масло", "сахар"], 
     "recipe_link": "https://example.com/napoleon-cake", 
     "restaurant_link": "https://restaurant.com/napoleon-cake"},
    
    # Напитки
    {"name": "☕ Кофе", 
     "category": "Напитки", 
     "description": "Кофе — бодрящий напиток, который заряжает энергией и дарит наслаждение с каждой чашкой. Идеальный спутник для начала дня или перерыва.", 
     "time": 5, 
     "ingredients": ["кофе"], 
     "recipe_link": "https://example.com/coffee", 
     "restaurant_link": "https://starbucks.com/coffee"},
    
    {"name": "🍹 Смузи", 
     "category": "Напитки", 
     "description": "Освежающий смузи из свежих фруктов и йогурта. Легкий и полезный напиток, который дарит ощущение свежести и прилив энергии.", 
     "time": 10, 
     "ingredients": ["фрукты", "йогурт"], 
     "recipe_link": "https://example.com/smoothie", 
     "restaurant_link": "https://restaurant.com/smoothie"},
]

# Категории блюд
categories = ["Закуски", "Салаты", "Супы", "Основные блюда", "Десерты", "Напитки"]

# Функция для создания клавиатуры с категориями
def create_category_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="🎲 Случайное блюдо"))
    keyboard.add(KeyboardButton(text="📅 Случайное меню на день"))  # Новая кнопка для случайного меню
    for category in categories:
        keyboard.add(KeyboardButton(text=category))
    keyboard.add(KeyboardButton(text="🔍 Поиск по ингредиентам"))  # Добавляем кнопку для поиска по ингредиентам
    return keyboard.as_markup(resize_keyboard=True)

# Функция для создания клавиатуры с блюдами в выбранной категории
def create_meal_keyboard(category):
    keyboard = ReplyKeyboardBuilder()
    for meal in meals:
        if meal["category"] == category:
            keyboard.add(KeyboardButton(text=meal["name"]))
    keyboard.add(KeyboardButton(text="🔙 Вернуться к категориям"))  
    return keyboard.as_markup(resize_keyboard=True)

# Обрабатываем команду /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я твой помощник по выбору блюд! 🍽 Сначала выбери категорию или попробуй случайное блюдо. "
        "Ты также можешь создать случайное меню на день.",
        reply_markup=create_category_keyboard()
    )

# Обрабатываем выбор категории
@dp.message(lambda message: message.text in categories)
async def choose_category(message: types.Message):
    category = message.text
    if category == "Напитки":
        await message.answer(
            f"Ты выбрал категорию {category}. Теперь выбери напиток:",
            reply_markup=create_meal_keyboard(category)
        )
    else:
        await message.answer(
            f"Ты выбрал категорию {category}. Теперь выбери блюдо:",
            reply_markup=create_meal_keyboard(category)
        )

# Обрабатываем случайное блюдо
@dp.message(lambda message: message.text == "🎲 Случайное блюдо")
async def random_meal(message: types.Message):
    random_meal = random.choice(meals)
    
    inline_kb = InlineKeyboardBuilder()
    inline_kb.add(InlineKeyboardButton(text="📖 Рецепт", web_app=WebAppInfo(url=random_meal["recipe_link"])))
    inline_kb.add(InlineKeyboardButton(text="🍴 Где попробовать?", web_app=WebAppInfo(url=random_meal["restaurant_link"])))

    await message.answer(
        f"Попробуй это случайное блюдо: {random_meal['name']}!\n\n"
        f"Описание: {random_meal['description']}\n\n"
        f"Нажми на одну из кнопок ниже, чтобы узнать рецепт или место, где можно попробовать это блюдо!",
        reply_markup=inline_kb.as_markup()
    )

# Обрабатываем случайное меню на день
@dp.message(lambda message: message.text == "📅 Случайное меню на день")
async def random_daily_menu(message: types.Message):
    breakfast = random.choice(meals)
    lunch = random.choice(meals)
    dinner = random.choice(meals)

    response = (
        f"Твоё случайное меню на день:\n\n"
        f"🍽 Завтрак: {breakfast['name']} (время приготовления: {breakfast['time']} минут)\n"
        f"🍽 Обед: {lunch['name']} (время приготовления: {lunch['time']} минут)\n"
        f"🍽 Ужин: {dinner['name']} (время приготовления: {dinner['time']} минут)\n"
    )

    await message.answer(response)

# Обрабатываем выбор блюда
@dp.message(lambda message: any(meal["name"] == message.text for meal in meals))
async def show_meal_details(message: types.Message):
    chosen_meal = next(meal for meal in meals if meal["name"] == message.text)
    
    inline_kb = InlineKeyboardBuilder()
    inline_kb.add(InlineKeyboardButton(text="📖 Рецепт", web_app=WebAppInfo(url=chosen_meal["recipe_link"])))
    inline_kb.add(InlineKeyboardButton(text="🍴 Где попробовать?", web_app=WebAppInfo(url=chosen_meal["restaurant_link"])))

    await message.answer(
        f"Ты выбрал {chosen_meal['name']}.\n\n"
        f"Описание: {chosen_meal['description']}\n\n"
        f"Время приготовления: {chosen_meal['time']} минут\n\n"
        f"Ингредиенты: {', '.join(chosen_meal['ingredients'])}\n\n"
        f"Нажми на одну из кнопок ниже, чтобы узнать рецепт или место, где можно попробовать это блюдо!",
        reply_markup=inline_kb.as_markup()
    )

# Обработка нажатия кнопки "Вернуться к категориям"
@dp.message(lambda message: message.text == "🔙 Вернуться к категориям")
async def back_to_categories(message: types.Message):
    await message.answer("Выбери категорию:", reply_markup=create_category_keyboard())
     
# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
