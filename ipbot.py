import telebot
from pydub import AudioSegment
import whisper
import time
import os

TELEGRAM_BOT_TOKEN = '7262419252:AAHAQwTqYAve5fjHa6rABN-BHqJ_khV7vNc'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

model = whisper.load_model("large") # 'base', 'small', 'medium', 'large'


@bot.message_handler(commands=['распознать-сообщение'])
def start_recognition(message):
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
        if os.path.exists("voice.oga"):
            os.remove("voice.oga")
        if os.path.exists("voice.wav"):
            os.remove("voice.wav")

def run_bot():
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Ошибка в polling: {e}")
            time.sleep(5)

run_bot()