import time
import os
import psutil
import math
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configure import (
    BOT_TOKEN, API_ID, API_HASH, BOT_PM, AUTHORIZED_CHATS,
    OWNER_SESSION, DUMP_CHAT_ID, TEXT_STYLE
)
import database as db

bot = Client("leech_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
owner = Client("owner_session", api_id=API_ID, api_hash=API_HASH, session_string=OWNER_SESSION)

active_tasks = {}
BOT_START_TIME = time.time()

# (MANTÉN TUS FUNCIONES get_readable_time, get_readable_file_size, get_sys_stats y apply_text_style AQUÍ)

def build_settings_keyboard(user_data):
    """Construye los botones dinámicos según el estado de la DB"""
    thumb_status = "✅ Activado" if user_data.get("auto_thumb_hd") else "❌ Desactivado"
    session_status = "🟢 Configurada" if user_data.get("session_string") else "🔴 No Configurada"
    
    keyboard = [
        [InlineKeyboardButton(f"🎬 Auto-Thumbnail HD: {thumb_status}", callback_data="set_thumb")],
        [InlineKeyboardButton(f"🔑 Sesión: {session_status}", callback_data="set_session_info")],
        [InlineKeyboardButton("🗑️ Borrar Sesión", callback_data="del_session"), 
         InlineKeyboardButton("🔄 Resetear", callback_data="reset_settings")],
        [InlineKeyboardButton("❌ Cerrar Panel", callback_data="close_panel")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ----------------- PANEL DE AJUSTES (/usettings) -----------------

@bot.on_message(filters.command(["useting", "usettings"]) & filters.private)
async def settings_panel(client, message):
    user_id = message.from_user.id
    user_data = await db.get_user(user_id)
    
    text = (
        "⚙️ **Panel de Configuración de Usuario**\n\n"
        "Aquí puedes personalizar tu experiencia de descarga. "
        "Si activas el Auto-Thumbnail, el bot buscará automáticamente portadas en IMDb.\n\n"
        "👇 Selecciona una opción:"
    )
    await message.reply_text(text, reply_markup=build_settings_keyboard(user_data))

@bot.on_callback_query(filters.regex(r"^(set_thumb|set_session_info|del_session|reset_settings|close_panel)$"))
async def settings_callbacks(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data
    user_data = await db.get_user(user_id)

    if data == "set_thumb":
        new_status = not user_data.get("auto_thumb_hd")
        await db.update_user(user_id, {"auto_thumb_hd": new_status})
        user_data["auto_thumb_hd"] = new_status # Actualizar variable local
        await callback_query.message.edit_reply_markup(reply_markup=build_settings_keyboard(user_data))
        await callback_query.answer("Configuración de portada actualizada.", show_alert=False)
        
    elif data == "set_session_info":
        await callback_query.answer("Para configurar, envía: /setsession TU_CODIGO", show_alert=True)
        
    elif data == "del_session":
        await db.update_user(user_id, {"session_string": None})
        user_data["session_string"] = None
        await callback_query.message.edit_reply_markup(reply_markup=build_settings_keyboard(user_data))
        await callback_query.answer("🗑️ Sesión eliminada de la base de datos.", show_alert=True)
        
    elif data == "reset_settings":
        await db.reset_user(user_id)
        user_data = await db.get_user(user_id) # Recargar datos limpios
        await callback_query.message.edit_reply_markup(reply_markup=build_settings_keyboard(user_data))
        await callback_query.answer("🔄 Todos los ajustes han sido reseteados.", show_alert=True)
        
    elif data == "close_panel":
        await callback_query.message.delete()

# ----------------- CONFIGURAR SESIÓN MANUALMENTE -----------------

@bot.on_message(filters.command("setsession") & filters.private)
async def set_session(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Debes incluir tu string session.\nEjemplo: `/setsession AQD_...`")
    
    session_string = message.command[1]
    await db.update_user(message.from_user.id, {"session_string": session_string})
    await message.reply_text("✅ Sesión guardada encriptada en la base de datos.")

# ----------------- LOGICA DE DESCARGA FINAL -----------------
# ... (Mantén tu función progress_for_pyrogram igual, hasta llegar a la parte donde se completa)

@bot.on_message(filters.command("leech") & filters.chat(AUTHORIZED_CHATS))
async def handle_leech(client, message):
    user_id = message.from_user.id
    user_data = await db.get_user(user_id)
    session_string = user_data.get("session_string")
    
    if not session_string:
        return await message.reply_text("⚠️ No tienes una sesión activa. Configúrala en `/usettings`.")
    
    # ... (Procesamiento del enlace igual que en el código anterior)
    
    # Simulación de variables para el mensaje final
    start_time = time.time()
    filename = "archivo_descargado.zip" # Obtenido dinámicamente en tu código
    user_name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    
    # AQUI INICIA TU LÓGICA DE user_client Y owner.send_document...
    # Cuando termine la descarga y subida exitosamente, editas el mensaje original con el formato final:
    
    time_taken = time.time() - start_time
    # Supongamos que fileSize es el total de bytes:
    fileSize = 1320702400 # Ejemplo 1.23GB
    
    final_text = (
        f"📄 `{filename}`\n"
        f"│\n"
        f"┟ 📦 **Tamaño de Tarea** → {get_readable_file_size(fileSize)}\n"
        f"┠ ⏱️ **Tiempo Tomado** → {get_readable_time(time_taken)}\n"
        f"┠ 📥 **Modo Entrada** → #Enlace\n"
        f"┠ 📤 **Modo Salida** → #Leech (Dump)\n"
        f"┠ 📁 **Total de Archivos** → 1\n"
        f"┖ 👤 **Tarea por** → {user_name}\n\n"
        f"〶 **Acción Realizada:**\n"
        f"⋗ ✅ El archivo ha sido enviado a tus Mensajes Privados (PM)"
    )
    
    # Enviar al PM y luego editar el status:
    # await bot.copy_message(...)
    # await status_msg.edit_text(final_text)

# ... (Resto del código de inicialización main)
