import asyncio
from aiohttp import web
from pyrogram import Client
from config import Config

# Cliente principal del bot. Lee los comandos de la carpeta 'plugins'
bot = Client(
    "leech_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

# Servidor de salud para Koyeb
async def handle_web(request):
    return web.Response(text="Bot Leech en línea")

async def web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle_web)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', Config.PORT)
    await site.start()
    print(f"Servidor web en puerto {Config.PORT}")

async def main():
    print("Iniciando Servidor Web...")
    await web_server()
    
    print("Iniciando Bot de Telegram...")
    await bot.start()
    print("¡Bot conectado exitosamente!")
    
    from pyrogram import idle
    await idle()
    
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
