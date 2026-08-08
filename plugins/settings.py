from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_config, update_user_config

# Diccionario para estados (esto se reinicia si el bot se reinicia)
user_states = {}

def get_buttons(config, state=None):
    hd_status = "✅" if config.get("hd_thumbnail_active") else "❌"
    pm_status = "✅" if config.get("pm_mode") else "❌"
    
    if state == "wait_session":
        return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancelar", callback_data="cancel_action")]])
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 Configurar Sesión", callback_data="set_session")],
        [InlineKeyboardButton("🖼 Configurar Miniatura", callback_data="set_thumb")],
        [InlineKeyboardButton(f"🎬 HD {hd_status}", callback_data="toggle_hd")],
        [InlineKeyboardButton(f"📩 PM {pm_status}", callback_data="toggle_pm")]
    ])

@Client.on_callback_query()
async def callback_handler(client, query):
    user_id = query.from_user.id
    config = await get_user_config(user_id)
    
    if query.data == "set_session":
        user_states[user_id] = "wait_session"
        await query.message.edit_text("🔑 **Envía tu String Session ahora.**\n(El mensaje se borrará al detectarse)", reply_markup=get_buttons(config, "wait_session"))
        
    elif query.data == "cancel_action":
        user_states[user_id] = None
        await query.message.edit_text("⚙️ **Panel Principal:**", reply_markup=get_buttons(config))

    # ... (añade aquí la lógica de los otros botones)

@Client.on_message(filters.text & ~filters.command(["start", "leech", "useting"]))
async def message_handler(client, message):
    user_id = message.from_user.id
    if user_states.get(user_id) == "wait_session":
        await update_user_config(user_id, {"string_session": message.text})
        try:
            await message.delete() # Borrar mensaje del usuario
        except:
            pass
        user_states[user_id] = None
        await message.reply("✅ Sesión guardada.", quote=True)
        # Aquí puedes llamar a una función que vuelva a mostrar el menú principal
