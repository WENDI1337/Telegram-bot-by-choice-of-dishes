import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import asyncio

API_TOKEN = '7912812196:AAGu9YWhQ0W7KMYjgTbPOqkVT4X3pwkAwc4'  # Замените на токен вашего бота

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список блюд с ссылками на рецепты и рестораны
meals = [
    {"name": "Пицца", "recipe_link": "https://example.com/pizza", "restaurant_link": "https://restaurant.com/pizza"},
    {"name": "Салат Цезарь", "recipe_link": "https://example.com/caesar-salad", "restaurant_link": "https://restaurant.com/caesar-salad"},
    {"name": "Борщ", "recipe_link": "https://example.com/borshch", "restaurant_link": "https://restaurant.com/borshch"},
    {"name": "Паста", "recipe_link": "https://example.com/pasta", "restaurant_link": "https://restaurant.com/pasta"},
    {"name": "Стейк", "recipe_link": "https://example.com/steak", "restaurant_link": "https://restaurant.com/steak"},
    {"name": "Шашлык", "recipe_link": "https://example.com/shashlyk", "restaurant_link": "https://restaurant.com/shashlyk"},
    {"name": "Роллы", "recipe_link": "https://example.com/rolls", "restaurant_link": "https://restaurant.com/rolls"},
    {"name": "Пельмени", "recipe_link": "https://example.com/pelmeni", "restaurant_link": "https://restaurant.com/pelmeni"},
    {"name": "Суп", "recipe_link": "https://example.com/soup", "restaurant_link": "https://restaurant.com/soup"},
    {"name": "Оливье", "recipe_link": "https://example.com/olivier", "restaurant_link": "https://restaurant.com/olivier"},
    {"name": "Курица", "recipe_link": "https://example.com/chicken", "restaurant_link": "https://restaurant.com/chicken"},
    {"name": "Блинчики", "recipe_link": "https://example.com/pancakes", "restaurant_link": "https://restaurant.com/pancakes"},
    {"name": "Морс", "recipe_link": "https://example.com/mors", "restaurant_link": "https://restaurant.com/mors"},
    {"name": "Кофе", "recipe_link": "https://example.com/coffee", "restaurant_link": "https://restaurant.com/coffee"},
    {"name": "Смузи", "recipe_link": "https://example.com/smoothie", "restaurant_link": "https://restaurant.com/smoothie"}
]

# Функция для создания клавиатуры с блюдами
def create_meal_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for meal in meals:
        keyboard.add(KeyboardButton(text=meal["name"]))
    return keyboard.as_markup(resize_keyboard=True)

# Обрабатываем команду /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я твой помощник по выбору блюд! 🍽 Выбирай блюдо из списка ниже:",
        reply_markup=create_meal_keyboard()
    )

# Обрабатываем выбор блюда
@dp.message(lambda message: any(meal["name"] == message.text for meal in meals))
async def choose_meal(message: types.Message):
    selected_meal = next(meal for meal in meals if meal["name"] == message.text)
    
    # Создаем inline-клавиатуру с Web App для перехода на сайт ресторана
    inline_kb = InlineKeyboardBuilder()
    inline_kb.add(InlineKeyboardButton(text="Где попробовать?", web_app=WebAppInfo(url=selected_meal["restaurant_link"])))
    
    # Отправляем сообщение с рецептом и кнопкой для перехода
    await message.answer(
        f"Ты выбрал {selected_meal['name']}! 🎉 Вот рецепт: {selected_meal['recipe_link']}\n"
        f"Если хочешь попробовать это блюдо, нажми на кнопку ниже!",
        reply_markup=inline_kb.as_markup()
    )

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
