import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_config, update_user_config

# Diccionario simple para rastrear estados (en memoria)
user_states = {}

def generate_settings_markup(config, first_name, state=None):
    if state == "wait_session":
        return "🔑 **Enviando Sesión:**\n\nPor favor, escribe o pega tu String Session aquí. El mensaje será eliminado automáticamente tras detectarse.", \
               InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancelar", callback_data="cancel_action")]])
    
    if state == "wait_thumb":
        return "🖼 **Enviando Miniatura:**\n\nEnvía la foto que deseas usar. Luego presiona 'Enviar'.", \
               InlineKeyboardMarkup([[InlineKeyboardButton("📤 Enviar", callback_data="confirm_thumb"), InlineKeyboardButton("❌ Cancelar", callback_data="cancel_action")]])

    # Panel Principal
    hd_status = "✅" if config.get("hd_thumbnail_active") else "❌"
    pm_status = "✅" if config.get("pm_mode") else "❌"
    text = f"⚙️ **Panel de Configuración de {first_name}**"
    buttons = [
        [InlineKeyboardButton("🔑 Configurar Sesión String", callback_data="set_session")],
        [InlineKeyboardButton("🖼 Configurar Miniatura", callback_data="set_thumb")],
        [InlineKeyboardButton(f"🎬 Miniaturas HD {hd_status}", callback_data="toggle_hd")],
        [InlineKeyboardButton(f"📩 Modo Privado {pm_status}", callback_data="toggle_pm")]
    ]
    return text, InlineKeyboardMarkup(buttons)

@Client.on_callback_query()
async def callback_handler(client, query):
    user_id = query.from_user.id
    data = query.data
    
    if data == "set_session":
        user_states[user_id] = "wait_session"
        text, markup = generate_settings_markup({}, query.from_user.first_name, state="wait_session")
        await query.message.edit_text(text, reply_markup=markup)
        
    elif data == "set_thumb":
        user_states[user_id] = "wait_thumb"
        text, markup = generate_settings_markup({}, query.from_user.first_name, state="wait_thumb")
        await query.message.edit_text(text, reply_markup=markup)

    elif data == "cancel_action":
        user_states[user_id] = None
        config = await get_user_config(user_id)
        text, markup = generate_settings_markup(config, query.from_user.first_name)
        await query.message.edit_text(text, reply_markup=markup)

    elif data == "confirm_thumb":
        # Conteo regresivo
        msg = query.message
        for i in range(6, 0, -1):
            await msg.edit_text(f"⏳ Procesando miniatura en {i} segundos...\n(Puedes cancelar antes)", 
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancelar", callback_data="cancel_action")]]))
            await asyncio.sleep(1)
        await query.answer("Miniatura guardada correctamente", show_alert=True)
        user_states[user_id] = None
        # Regresar al menú principal...

# Escuchar la respuesta del usuario para la sesión o la foto
@Client.on_message(filters.text | filters.photo)
async def message_handler(client, message):
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id] == "wait_session":
        # Guardar en DB
        await update_user_config(user_id, {"string_session": message.text})
        await message.delete() # Elimina la sesión enviada
        user_states[user_id] = None
        await message.reply("✅ Sesión guardada con éxito.", quote=True)
        # Aquí podrías volver a mostrar el /useting
