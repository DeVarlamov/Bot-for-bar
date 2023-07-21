import datetime
import telegram
import telegram_bot_calendar
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

def start(update, context):
    # Отправляем приветственное сообщение
    update.message.reply_text('Привет! Я помогу тебе забронировать место в нашем ресторане.')

    # Создаем календарь для выбора даты
    reply_markup = telegram_bot_calendar.create_calendar(
        name='calendar',
        year=datetime.datetime.now().year,
        month=datetime.datetime.now().month,
        day=datetime.datetime.now().day,
        callback_prefix='calendar_'
    )

    # Отправляем сообщение с календарем
    update.message.reply_text('Выбери дату:', reply_markup=reply_markup)

def calendar_selected(update, context):
    # Получаем выбранную дату
    query = update.callback_query
    selected, date = telegram_bot_calendar.process_calendar_selection(context.bot, query)

    # Сохраняем выбранную дату
    context.user_data['date'] = date.strftime('%d.%m.%Y')

    # Создаем кнопки для выбора времени
    keyboard = [
        [KeyboardButton('12:00'), KeyboardButton('13:00'), KeyboardButton('14:00')],
        [KeyboardButton('15:00'), KeyboardButton('16:00'), KeyboardButton('17:00')],
        [KeyboardButton('18:00'), KeyboardButton('19:00'), KeyboardButton('20:00')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем сообщение с кнопками для выбора времени
    update.callback_query.message.reply_text('Выбери время:', reply_markup=reply_markup)

def time_selected(update, context):
    # Получаем выбранное время и дату
    time = update.message.text
    date = context.user_data['date']

    # Сохраняем выбранное время и дату
    context.user_data['time'] = time
    context.user_data['datetime'] = f'{date} {time}'

    # Запрашиваем количество гостей
    update.message.reply_text('Сколько гостей будет?', reply_markup=ReplyKeyboardMarkup([['1', '2', '3', '4']], resize_keyboard=True))

def guests_selected(update, context):
    # Получаем количество гостей
    guests = update.message.text

    # Сохраняем количество гостей и дату-время брони в базу данных или файл
    datetime_str = context.user_data['datetime']
    datetime_obj = datetime.datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')
    reservation_data = {'datetime': datetime_obj, 'guests': guests}
    # сохраняем reservation_data в базу данных или файл

    # Отправляем подтверждение бронирования
    update.message.reply_text(f'Спасибо за бронирование! Вы забронировали место на {datetime_str} для {guests} гостей.')

def main():
    # Создаем объект updater и получаем токен из файла token.txt
    token = '6134349352:AAFkZye0yzWv42zytlJMSM2uGYp6Hc3clIU'
    updater = Updater(token)

    # Создаем объект dispatcher и добавляем обработчики команд и сообщений
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(calendar_selected, pattern='^calendar'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, time_selected))
    dp.add_handler(MessageHandler(Filters.regex(r'^[1-4]$'), guests_selected))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
