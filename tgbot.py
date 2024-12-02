import telebot

from src.settings import BotSettings
from src.utils.setup_func import (
    startup_message,
    set_bot_commands,
    register_handlers
)

bot = telebot.TeleBot(BotSettings.TOKEN)


def main():
    startup_message()
    set_bot_commands(bot)
    register_handlers(bot)
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    main()
