from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_config, update_user_config

@Client.on_message(filters.command("useting"))
async def useting_cmd(client, message):
    user_id = message.from_user.id
    config = await get_user_config(user_id)
    
    # Textos dinámicos dependiendo del estado
    hd_thumb_status = "✅ Activado" if config.get("hd_thumbnail_active") else "❌ Desactivado"
    pm_status = "✅ Activado" if config.get("pm_mode") else "❌ Desactivado"
    session_status = "✅ Registrada" if config.get("string_session") else "❌ Sin registro"

    text = f"⚙️ **Panel de Configuración de {message.from_user.first_name}**\n\nElige una opción para modificar:"
    
    buttons = [
        [InlineKeyboardButton(f"🔑 Enviar Sesión String ({session_status})", callback_data="set_session")],
        [InlineKeyboardButton("🖼 Mandar Miniatura Personalizada", callback_data="set_thumb")],
        [InlineKeyboardButton(f"🎬 Miniaturas HD (Min 1:30) [{hd_thumb_status}]", callback_data="toggle_hd")],
        [InlineKeyboardButton(f"📩 Enviar al Privado (PM) [{pm_status}]", callback_data="toggle_pm")]
    ]
    
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query()
async def callback_handler(client, query):
    user_id = query.from_user.id
    config = await get_user_config(user_id)
    
    if query.data == "toggle_hd":
        new_status = not config.get("hd_thumbnail_active")
        await update_user_config(user_id, {"hd_thumbnail_active": new_status})
        await query.answer(f"Miniaturas HD {'Activadas' if new_status else 'Desactivadas'}", show_alert=True)
        
    elif query.data == "toggle_pm":
        new_status = not config.get("pm_mode")
        await update_user_config(user_id, {"pm_mode": new_status})
        await query.answer(f"Modo PM {'Activado' if new_status else 'Desactivado'}", show_alert=True)
        
    # La lógica para 'set_session' y 'set_thumb' requeriría usar la librería pyromod o 
    # guardar un estado (FSM) para esperar el próximo mensaje del usuario.
    # Por ahora, cerramos la alerta.
    await query.message.delete()
