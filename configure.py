import os

# ----------------- CREDENCIALES BASE -----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "TU_BOT_TOKEN_AQUI")
API_ID = int(os.environ.get("API_ID", "TU_API_ID_AQUI"))
API_HASH = os.environ.get("API_HASH", "TU_API_HASH_AQUI")

# ----------------- CONFIGURACIÓN DEL DUEÑO -----------------
USER_ID = int(os.environ.get("USER_ID", "TU_ID_DE_ADMIN_AQUI"))
AUTHORIZED_CHATS = [-100123456789, USER_ID]
BOT_PM = True

# ----------------- WZML-X DUMP & SESIONES -----------------
OWNER_SESSION = os.environ.get("OWNER_SESSION", "TU_STRING_SESSION_PREMIUM_AQUI")
DUMP_CHAT_ID = int(os.environ.get("DUMP_CHAT_ID", "TU_CHAT_DUMP_ID_AQUI"))

# ----------------- BASE DE DATOS -----------------
DATABASE_URL = os.environ.get("DATABASE_URL", "TU_MONGODB_URI_AQUI")

# ----------------- PERSONALIZACIÓN -----------------
TEXT_STYLE = os.environ.get("TEXT_STYLE", "code")
