import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    SUPPORT_CHAT_ID: int = int(os.getenv("SUPPORT_CHAT_ID"))
    MAX_LENGTH: int = int(os.getenv("MAX_LENGTH", 250))
    DB_NAME: str = os.getenv("DB_NAME", "support_bot.db")