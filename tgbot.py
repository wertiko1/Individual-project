import os
import telebot
import whisper
import time

from config import settings
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
    print(f"\033[35mLogged in as FourTureProject. User: @fourprogect_bot\033[0m")
    print("\033[36m------------------------------------------------------------\033[0m")

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

if __name__ == "__main__":
    print_startup_message()
    bot.polling()