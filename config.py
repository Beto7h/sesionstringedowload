import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    OWNER_STRING = os.getenv("OWNER_STRING", "") # Tu sesión premium
    AUTH_GROUP_ID = int(os.getenv("AUTH_GROUP_ID", 0))
    DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", 0))
    MONGO_URI = os.getenv("MONGO_URI", "")
    PORT = int(os.getenv("PORT", 8080))
