from pydub import AudioSegment
from telebot import TeleBot
from telebot.types import Message

from src.utils import recognize_audio


def start_recognize(message: Message, bot: TeleBot):
    bot.reply_to(message, "Пожалуйста, отправьте голосовое сообщение для распознавания.")


def handle_voice_message(message: Message, bot: TeleBot):
    try:
        file_info = bot.get_file(message.voice.file_id)
        voice_file = bot.download_file(file_info.file_path)

        with open("voice.oga", "wb") as f:
            f.write(voice_file)

        audio = AudioSegment.from_ogg("voice.oga")
        audio.export("voice.wav", format="wav")

        # хз будет ли оно работать xd
        transcription = recognize_audio("voice.wav")

        bot.reply_to(message, transcription)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке сообщения. Попробуйте ещё раз.")
        print(f"Ошибка: {e}")


def register_handlers(bot: TeleBot):
    bot.register_message_handler(start_recognize, commands=['recognize'])
    bot.register_message_handler(handle_voice_message, content_types=['voice'])
