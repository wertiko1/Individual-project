import os
import telebot
import whisper
import time

from config import settings
from telebot import types
from pydub import AudioSegment

bot = telebot.TeleBot(settings["TOKEN"])

# "base", "small", "medium", "large"
model = whisper.load_model("base")

def print_startup_message():
    print("\033[36m------------------------------------------------------------\033[0m")
    print("\033[36m _____                      _____                    \033[0m")
    print("\033[36m|  ___|  ___   _   _  _ __ |_   _| _   _  _ __   ___ \033[0m")
    print("\033[36m| |_    / _ \ | | | || '__|  | |  | | | || '__| / _ \\\033[0m")
    print("\033[36m|  _|  | (_) || |_| || |     | |  | |_| || |   |  __/\033[0m")
    print("\033[36m|_|     \___/  \__,_||_|     |_|   \__,_||_|    \___|\033[0m")
    print("\033[35mLogged in as FourTureProject. User: @fourprogect_bot\033[0m")
    print("\033[36m------------------------------------------------------------\033[0m")

def set_bot_commands():
    bot.set_my_commands([
        types.BotCommand("menu", "Главное меню"),
        types.BotCommand("notes", "Открыть ежедневник"),
        types.BotCommand("recognize", "Преобразование голосового сообщения в текст"),
    ])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    set_bot_commands()
    bot.reply_to(message, "Добро пожаловать! Используйте командное меню слева от строки ввода, чтобы начать.")
    main_menu(message)

# Главное меню
@bot.message_handler(commands=['menu'])
def main_menu(message):
    menu_text = "Выберите действие:"

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_menu = types.KeyboardButton("Главное меню")
    btn_notes = types.KeyboardButton("Ежедневник")
    markup.add(btn_menu, btn_notes)
    bot.send_message(message.chat.id, menu_text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if message.text == "Главное меню":
        main_menu(message)
    elif message.text == "Ежедневник":
        bot.reply_to(message, "Здесь будет функция ежедневника.")

@bot.message_handler(commands=['recognize'])
def start_recognize(message):
    bot.reply_to(message, "Пожалуйста, отправьте голосовое сообщение для распознавания.")


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        voice_file = bot.download_file(file_info.file_path)

        with open("voice.oga", "wb") as f:
            f.write(voice_file)

        audio = AudioSegment.from_ogg("voice.oga")
        audio.export("voice.wav", format="wav")

        result = model.transcribe("voice.wav")
        transcription = result["text"]

        bot.reply_to(message, transcription)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке сообщения. Попробуйте ещё раз.")
        print(f"Ошибка: {e}")
    finally:
        for temp_file in ["voice.oga", "voice.wav"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

def run_bot():
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Ошибка в polling: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print_startup_message()
    run_bot()