from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton


def send_welcome(message: Message, bot: TeleBot):
    bot.reply_to(message, "Добро пожаловать! Используйте командное меню слева от строки ввода, чтобы начать.")
    main_menu(message)


def main_menu(message: Message, bot: TeleBot):
    menu_text = "Выберите действие:"

    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_menu = KeyboardButton("Главное меню")
    btn_notes = KeyboardButton("Ежедневник")
    markup.add(btn_menu, btn_notes)
    bot.send_message(message.chat.id, menu_text, reply_markup=markup)


def handle_text_message(message: Message, bot: TeleBot):
    if message.text == "Главное меню":
        main_menu(message)
    elif message.text == "Ежедневник":
        bot.reply_to(message, "Здесь будет функция ежедневника.")


def register_handlers(bot: TeleBot):
    bot.register_message_handler(handle_text_message, content_types=['text'])
    bot.register_message_handler(main_menu, commands=['menu'])
    bot.register_message_handler(send_welcome, commands=['start'])
