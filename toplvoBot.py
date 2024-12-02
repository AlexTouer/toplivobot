import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
bot = telebot.TeleBot("7789401850:AAGYtBbfgYFmSkjevCkHtopaWTIK8HedBSM")


# Словарь для хранения временных данных пользователей
user_data = {}

markup = ReplyKeyboardMarkup(resize_keyboard=True)
start_button = KeyboardButton("Начать расчет")
markup.add(start_button)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я помогу рассчитать расход топлива на 100 км и стоимость 1 км.\n"
        "Нажмите кнопку 'Начать расчет', чтобы начать.",
        reply_markup=markup
    )
    # Сбрасываем данные пользователя
    user_data[message.chat.id] = {"liters": None, "distance": None, "fuel_price": None}

@bot.message_handler(func=lambda message: message.text == "Начать расчет")
def start_calculation(message):
    bot.send_message(
        message.chat.id,
        "Введите количество литров топлива, которое вы заправили:"
    )
    user_data[message.chat.id] = {"liters": None, "distance": None, "fuel_price": None}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("liters") is None)
def get_liters(message):
    try:
        liters = float(message.text)
        if liters <= 0:
            bot.send_message(message.chat.id, "Количество литров должно быть больше 0. Попробуйте снова.")
            return
        user_data[message.chat.id]["liters"] = liters
        bot.send_message(
            message.chat.id,
            "Отлично! Теперь введите расстояние, которое вы проехали (в км):"
        )
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число литров.")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("distance") is None and user_data[message.chat.id].get("liters") is not None)
def get_distance(message):
    try:
        distance = float(message.text)
        if distance <= 0:
            bot.send_message(message.chat.id, "Расстояние должно быть больше 0. Попробуйте снова.")
            return
        user_data[message.chat.id]["distance"] = distance
        bot.send_message(
            message.chat.id,
            "Теперь введите стоимость 1 литра топлива в гривнах:"
        )
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число километров.")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("fuel_price") is None and user_data[message.chat.id].get("distance") is not None)
def get_fuel_price(message):
    try:
        fuel_price = float(message.text)
        if fuel_price <= 0:
            bot.send_message(message.chat.id, "Стоимость топлива должна быть больше 0. Попробуйте снова.")
            return
        user_data[message.chat.id]["fuel_price"] = fuel_price

        # Выполняем расчёты
        liters = user_data[message.chat.id]["liters"]
        distance = user_data[message.chat.id]["distance"]

        # Расход топлива на 100 км
        consumption = (liters / distance) * 100

        # Стоимость 1 км пробега
        cost_per_km = fuel_price * (liters / distance)

        bot.send_message(
            message.chat.id,
            f"Ваш расход топлива: {consumption:.2f} литров на 100 км.\n"
            f"Стоимость 1 км пробега: {cost_per_km:.2f} грн."
        )

        # Сбрасываем данные пользователя
        user_data.pop(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число стоимости топлива.")

@bot.message_handler(func=lambda message: True)
def default_response(message):
    bot.send_message(
        message.chat.id,
        "Пожалуйста, следуйте инструкциям и введите корректные данные."
    )
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Возникла ошибка: {e}")

