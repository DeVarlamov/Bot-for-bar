import re
import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token)
chat = (config.chat_id)

menu = types.KeyboardButton("📒 Меню")
reserve = types.KeyboardButton("👽 Резерв стола")
cancellation = types.KeyboardButton("отмена⛔️")
bar_btn = types.KeyboardButton("Бар🥃")
kitchen_btn = types.KeyboardButton("Кухня🍕")
back = types.KeyboardButton("🔙")

craft = types.KeyboardButton("Сами наливаем🛠")
vino = types.KeyboardButton("Винная карта🍷")
strong = types.KeyboardButton("Крепач🚀")
non_alcoholic = types.KeyboardButton("Без Алко🏇")


def start_markup():
    """старт ."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(menu, reserve)
    return markup


def main_menu_markup():
    """Меню ."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(bar_btn, kitchen_btn, back)
    return markup


def bar_menu_markup():
    """бар меню ."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(craft, vino, strong, non_alcoholic, back)
    return markup


def send_photo_with_markup(chat_id, photo_path, caption, markup):
    """Фото."""
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, caption=caption, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    """Функция старта."""
    markup = start_markup()
    send_photo_with_markup(message.chat.id, 'картинки/лого.jpg', 
                           "Привет, {0.first_name}! Вас приветствуют "
                           "бар мерзавчики.🐴🐴🐴".format(message.from_user), 
                           markup)


@bot.message_handler(content_types=['text'])
def func(message):
    """Функция ответа пользователю."""
    if message.text == "👽 Резерв стола":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(cancellation)
        bot.send_message(message.chat.id, text="Введите дату (дд.мм.):",
                         reply_markup=markup)
        bot.register_next_step_handler(message, get_date)

    elif message.text == "📒 Меню":
        markup = main_menu_markup()
        bot.send_message(message.chat.id, text="Смотри что у нас есть",
                         reply_markup=markup)

    elif message.text == "🔙":
        markup = start_markup()
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню",
                         reply_markup=markup)

    elif message.text == "Бар🥃":
        markup = bar_menu_markup()
        bot.send_message(message.chat.id, text="Ну, {0.first_name}! "
                         "Чем нахуяримся?".format(message.from_user),
                         reply_markup=markup)

    elif message.text == "Кухня🍕":
        markup = main_menu_markup()
        send_photo_with_markup(message.chat.id,
                               'картинки/кухня.jpg',
                               "{0.first_name} это еда ее едят!".format(
                                message.from_user), markup)

    elif message.text == "Сами наливаем🛠":
        markup = bar_menu_markup()
        send_photo_with_markup(message.chat.id, 
                               'картинки/бар.jpg', 
                               "{0.first_name}, а ты шутить не любишь!".format(
                                message.from_user), markup)

    elif message.text == "Винная карта🍷":
        markup = bar_menu_markup()
        send_photo_with_markup(message.chat.id,
                               'картинки/Вино.jpg', 
                               "{0.first_name}, вот наша винность".format(
                                message.from_user), markup)

    elif message.text == "Игорь гей":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(menu, back)
        send_photo_with_markup(message.chat.id,
                               'картинки/Игорь.jpg',
                               "{0.first_name}, Ты хотел сказать его "
                               "величество Гейство?!".format(
                                message.from_user), markup)

    elif message.text == "Крепач🚀":
        markup = bar_menu_markup()
        send_photo_with_markup(
            message.chat.id, 'картинки/крепкий.bmp',
            "{0.first_name}, ну поехали".format(message.from_user), markup)

    elif message.text == "Без Алко🏇":
        markup = bar_menu_markup()
        send_photo_with_markup(
            message.chat.id, 'картинки/БА.jpg',
            "{0.first_name}, Выходной, так выходной!".format(
             message.from_user), markup)

    else:
        bot.send_message(message.chat.id,
                         text="На такую команду я не запрограммировал..")


def get_date(message):
    """Функция проверки ввода даты."""
    date_pattern = r'^\d{2}\.\d{2}$'
    if re.match(date_pattern, message.text):
        date = message.text
        if "отмена⛔️" in date.lower():
            bot.send_message(message.chat.id, text="Бронирование отменено",)
            start(message)
        else:
            bot.send_message(message.chat.id, "Введите время (чч:мм):")
            bot.register_next_step_handler(message, get_time, date)
    else:
        if "отмена⛔️" in message.text.lower():
            bot.send_message(message.chat.id, text="Бронирование отменено",)
            start(message)
        else:
            bot.send_message(message.chat.id,
                             text="Пожалуйста, введите дату в формате дд.мм.")
            bot.register_next_step_handler(message, get_date)


def get_time(message, date):
    """Получение времени."""
    time = message.text
    # Проверяем, что время введено в формате ЧЧ:ММ
    if not re.match(r'^\d{1,2}:\d{2}$', time):
        if "отмена⛔️" in time.lower():
            bot.send_message(message.chat.id, text="Бронирование отменено")
            start(message)
        bot.send_message(message.chat.id,
                         "Пожалуйста, введите время в формате часы:минута")
        return bot.register_next_step_handler(message, get_time, date)
    if "отмена⛔️" in time.lower():
        bot.send_message(message.chat.id, text="Бронирование отменено")
        start(message)
    else:
        bot.send_message(message.chat.id, "Введите количество гостей:")
        bot.register_next_step_handler(message, get_guests, date, time)


def get_guests(message, date, time):
    """Получение количества гостей."""
    guests = message.text
    # Проверяем, что введено число
    if not guests.isdigit():
        if "отмена⛔️" in time.lower():
            bot.send_message(message.chat.id, text="Бронирование отменено")
            start(message)
        bot.send_message(message.chat.id, "Пожалуйста, введите число гостей")
        return bot.register_next_step_handler(message, get_guests, date, time)
    if "отмена⛔️" in guests.lower():
        bot.send_message(message.chat.id, text="Бронирование отменено")
        start(message)
    else:
        if "отмена⛔️" in guests.lower():
            bot.send_message(message.chat.id, text="Бронирование отменено")
            start(message)
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1,
                                                 resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Отправить телефон",
                                                request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, 'Ваши данные для брони',
                         reply_markup=keyboard)
        bot.register_next_step_handler(
            message, get_contact_info,
            date, time, guests
            )


def get_contact_info(message, date, time, guests):
    """Получение сообщения."""
    contact_info = message.contact
    # Check if the message text contains keywords to cancel the reservation
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("🔙")
    markup.add(back)
    bot.send_message(message.chat.id, text="Спасибо за резерв! "
                     " Мы ждем {}х гостей, {} в {} ."
                     "\nВаши контакты: {} ({})".format(
                            guests, date, time, contact_info.first_name,
                            contact_info.phone_number
                            ), reply_markup=markup)
    bot.send_message(
            chat_id=chat,
            text="Внимание бронь на {} "
            "в {} для {} гостей. Контактная"
            " информация: {} ({}). UserID({})".format(
                date, time, guests, contact_info.first_name,
                contact_info.phone_number,
                contact_info.user_id
                                           ))


bot.polling(none_stop=True)
