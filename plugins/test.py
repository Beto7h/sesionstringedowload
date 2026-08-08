from pyrogram import Client, filters

@Client.on_message(filters.command("test"))
async def test_cmd(client, message):
    await message.reply_text("¡Hola! Sí estoy recibiendo tus comandos correctamente. 🚀")
