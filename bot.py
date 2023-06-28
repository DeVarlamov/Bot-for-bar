
from telegram.ext import Updater
from telegram.ext import (CommandHandler,
                          ConversationHandler,
                          MessageHandler,
                          Filters)
import telegram


# Определите состояния для разговора
VINE_DAY = 0
VINE_MONTH = 1
VINE_TIME = 2
VINE_GUESTS = 3
VINE_CONTACT = 4


def start(update, context):
    """Обработчик команды start."""
    photo_path = 'картинки/лого.jpg'
    photo_file = open(photo_path, 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file)
    custom_keyboard = [['/menu📒', '/reserve👽']]
    reply_markup = telegram.ReplyKeyboardMarkup(
        custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Мерзавчики на связи кого чего сука! 🕶",
                             reply_markup=reply_markup)
    photo_file.close()


def reserve(update, context):
    """Обработчик команды menu."""
    context.user_data['reservation'] = {}
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Введите день (число) для резерва:")
    return VINE_DAY


def vine_choice1(update, context):
    """Ввод месяца."""
    day = update.message.text
    context.user_data['reservation']['day'] = day
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Введите месяц (название) для резерва:")
    return VINE_MONTH


def vine_choice2(update, context):
    """Ввод времени."""
    month = update.message.text
    context.user_data['reservation']['month'] = month
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Введите время (часы:минуты) для резерва:")
    return VINE_TIME


def vine_choice3(update, context):
    """Ввод колличества гостей."""
    time = update.message.text
    context.user_data['reservation']['time'] = time
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Введите количество гостей для резерва:")
    return VINE_GUESTS


def vine_choice5(update, context):
    """Ввод контактной информации."""
    contact_info = update.message.text
    context.user_data['reservation']['contact'] = contact_info
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Введите ваши контакты для обратной связи:")
    return VINE_CONTACT


def vine_choice4(update, context):
    """Сообщение подтверждение брони."""
    guests = update.message.text
    context.user_data['reservation']['guests'] = guests
    reservation_data = context.user_data['reservation']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Спасибо за резерв! Ваш столик забронирован на {day} {month} "
        "в {time} для {contact} гостей. Ваша контактная"
        "информация: {guests}.".format(**reservation_data)
        )
    context.bot.send_message(
        chat_id='1106421798',
        text="бронь на  {day} {month} "
        "в {time} для {contact} гостей. Контактная"
        "информация: {guests}.".format(**reservation_data)
        )

    return ConversationHandler.END


def menu(update, context):
    """Меню."""
    menu_keyboard = [['/bar🍸', '/kuhny🍖'], ['/start⏪']]
    reply_markup = telegram.ReplyKeyboardMarkup(
        menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Хорошо давай 🕶",
        reply_markup=reply_markup
    )


def bar(update, context):
    """Бар ."""
    photo_path = 'картинки/бар.jpg'
    photo_file = open(photo_path, 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file)

    bar_keyboard = [['/start⏪', '/menu📒']]
    reply_markup = telegram.ReplyKeyboardMarkup(
        bar_keyboard, one_time_keyboard=True,
        resize_keyboard=True
        )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="окей 🕶",
                             reply_markup=reply_markup)


def kuhny(update, context):
    """Кухня."""
    photo_path = 'картинки/кухня.jpg'
    photo_file = open(photo_path, 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file)

    kuhny_keyboard = [['/start⏪', '/menu📒']]
    reply_markup = telegram.ReplyKeyboardMarkup(
        kuhny_keyboard, one_time_keyboard=True,
        resize_keyboard=True
        )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="окей 🕶",
                             reply_markup=reply_markup)


updater = Updater(token='6134349352:AAFkZye0yzWv42zytlJMSM2uGYp6Hc3clIU',
                  use_context=True)

# Create an instance of the Dispatcher class using updater.dispatcher
dispatcher = updater.dispatcher
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('reserve', reserve)],
    states={
        VINE_DAY: [(MessageHandler(Filters.text, vine_choice1))],
        VINE_MONTH: [(MessageHandler(Filters.text, vine_choice2))],
        VINE_TIME: [(MessageHandler(Filters.text, vine_choice3))],
        VINE_CONTACT: [(MessageHandler(Filters.text, vine_choice4))],
        VINE_GUESTS: [(MessageHandler(Filters.text, vine_choice5))],
    },
    fallbacks=[],)

# Add our handlers to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('menu', menu))
dispatcher.add_handler(CommandHandler('bar', bar))
dispatcher.add_handler(CommandHandler('kuhny', kuhny))
dispatcher.add_handler(conv_handler)

# Start the bot
updater.start_polling()
