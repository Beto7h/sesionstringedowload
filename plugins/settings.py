from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_config, update_user_config

def generate_settings_markup(config, first_name):
    hd_thumb_status = "✅ Activado" if config.get("hd_thumbnail_active") else "❌ Desactivado"
    pm_status = "✅ Activado" if config.get("pm_mode") else "❌ Desactivado"
    session_status = "✅ Registrada" if config.get("string_session") else "❌ Sin registro"

    text = f"⚙️ **Panel de Configuración de {first_name}**\n\nElige una opción para modificar:"
    
    buttons = [
        [InlineKeyboardButton(f"🔑 Enviar Sesión String ({session_status})", callback_data="set_session")],
        [InlineKeyboardButton("🖼 Mandar Miniatura Personalizada", callback_data="set_thumb")],
        [InlineKeyboardButton(f"🎬 Miniaturas HD (Min 1:30) [{hd_thumb_status}]", callback_data="toggle_hd")],
        [InlineKeyboardButton(f"📩 Enviar al Privado (PM) [{pm_status}]", callback_data="toggle_pm")]
    ]
    return text, InlineKeyboardMarkup(buttons)

@Client.on_message(filters.command("useting"))
async def useting_cmd(client, message):
    user_id = message.from_user.id
    config = await get_user_config(user_id)
    
    text, reply_markup = generate_settings_markup(config, message.from_user.first_name)
    await message.reply_text(text, reply_markup=reply_markup)

@Client.on_callback_query()
async def callback_handler(client, query):
    user_id = query.from_user.id
    config = await get_user_config(user_id)
    
    if query.data == "toggle_hd":
        new_status = not config.get("hd_thumbnail_active")
        await update_user_config(user_id, {"hd_thumbnail_active": new_status})
        await query.answer(f"Miniaturas HD {'Activadas' if new_status else 'Desactivadas'}", show_alert=False)
        
    elif query.data == "toggle_pm":
        new_status = not config.get("pm_mode")
        await update_user_config(user_id, {"pm_mode": new_status})
        await query.answer(f"Modo PM {'Activado' if new_status else 'Desactivado'}", show_alert=False)
        
    elif query.data == "set_session":
        await query.answer("Para configurar tu sesión string, responde a este mensaje o envía un comando de texto con tu sesión (próximamente interactivo).", show_alert=True)
        return

    elif query.data == "set_thumb":
        await query.answer("Envía la imagen que deseas usar como miniatura personalizada.", show_alert=True)
        return

    # Volvemos a consultar la config actualizada para refrescar el menú sin borrarlo
    updated_config = await get_user_config(user_id)
    text, reply_markup = generate_settings_markup(updated_config, query.from_user.first_name)
    
    # Actualiza el mensaje existente en lugar de borrarlo
    try:
        await query.message.edit_text(text, reply_markup=reply_markup)
    except Exception:
        pass
