from loguru import logger
from telebot import TeleBot
from telebot.types import BotCommand

from src.handlers import register_start, register_recognize


def startup_message():
    print("\033[36m------------------------------------------------------------\033[0m")
    print("\033[36m _____                      _____                    \033[0m")
    print("\033[36m|  ___|  ___   _   _  _ __ |_   _| _   _  _ __   ___ \033[0m")
    print("\033[36m| |_    / _ \ | | | || '__|  | |  | | | || '__| / _ \\\033[0m")
    print("\033[36m|  _|  | (_) || |_| || |     | |  | |_| || |   |  __/\033[0m")
    print("\033[36m|_|     \___/  \__,_||_|     |_|   \__,_||_|    \___|\033[0m")
    print("\033[35mLogged in as FourTureProject. User: @fourprogect_bot\033[0m")
    print("\033[36m------------------------------------------------------------\033[0m")


def set_bot_commands(bot: TeleBot):
    bot.set_my_commands([
        BotCommand("menu", "Главное меню"),
        BotCommand("notes", "Открыть ежедневник"),
        BotCommand("recognize", "Преобразование голосового сообщения в текст"),
    ])
    logger.info("Commands loaded")


def register_handlers(bot):
    register_start(bot)
    register_recognize(bot)
