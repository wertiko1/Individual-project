import os

from dotenv import load_dotenv

load_dotenv()


class BotSettings:
    load_dotenv()
    TOKEN: str = os.getenv('TOKEN')


class ModelSettings:
    VOSK_MODEL: str = "src/settings/vosk"
