from pyrogram import Client
from config import Config

# Cliente principal del bot
bot = Client(
    "leech_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    print("Iniciando Bot de Telegram en el VPS...")
    # bot.run() se encarga de iniciar, mantener el bot escuchando (idle) y cerrarlo correctamente de forma nativa
    bot.run()
