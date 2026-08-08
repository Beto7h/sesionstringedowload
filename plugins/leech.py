import os
import time
from pyrogram import Client, filters
from config import Config
from database import get_user_config
from utils import progress_bar
import wzgram # Asumiendo que esta es tu librería de subida

# Cliente extra con la cuenta premium del DUEÑO para archivos pesados
owner_client = Client("owner_session", session_string=Config.OWNER_STRING, api_id=Config.API_ID, api_hash=Config.API_HASH)

@Client.on_message(filters.command("leech") & filters.chat(Config.AUTH_GROUP_ID))
async def leech_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Debes enviar un link. Ejemplo: `/leech https://t.me/c/123/45`")
        
    link = message.command[1]
    user_id = message.from_user.id
    config = await get_user_config(user_id)
    
    if not config.get("string_session"):
        return await message.reply_text("❌ No tienes una sesión registrada. Usa /useting.")

    # Crear cliente temporal con la sesión del usuario
    user_client = Client("temp_user", session_string=config["string_session"], api_id=Config.API_ID, api_hash=Config.API_HASH)
    await user_client.start()

    status_msg = await message.reply_text("🔄 **Iniciando proceso...**")
    
    try:
        chat_id = int("-100" + link.split("/")[-2])
        msg_id = int(link.split("/")[-1])
        
        msg_to_download = await user_client.get_messages(chat_id, msg_id)
        file_size = msg_to_download.document.file_size if msg_to_download.document else msg_to_download.video.file_size
        file_name = msg_to_download.document.file_name if msg_to_download.document else "video.mp4"
        
        start_time = time.time()
        
        # 1. DESCARGA
        file_path = await user_client.download_media(
            msg_to_download, 
            file_name=f"downloads/{file_name}",
            progress=progress_bar,
            progress_args=(status_msg, start_time, file_name, message.from_user.first_name, user_id)
        )
        await user_client.stop()

        # 2. PROCESAMIENTO (Miniatura 1:30 si está activo)
        thumb_path = None
        if config.get("hd_thumbnail_active"):
            await status_msg.edit_text("🎬 **Extrayendo miniatura HD al minuto 1:30...**")
            thumb_path = f"downloads/thumb_{user_id}.jpg"
            os.system(f"ffmpeg -ss 00:01:30 -i '{file_path}' -vframes 1 -q:v 2 '{thumb_path}' -y")

        # 3. DESTINO (Grupo o PM)
        target_chat = user_id if config.get("pm_mode") else message.chat.id

        # 4. LÓGICA DE SUBIDA (Menos o más de 2GB)
        await status_msg.edit_text("⬆️ **Subiendo archivo...**")
        
        if file_size > 2 * 1024 * 1024 * 1024:
            # Archivo > 2GB: Subir al Dump Channel con la sesión Premium del dueño
            await owner_client.start()
            uploaded_msg = await owner_client.send_document(
                chat_id=Config.DUMP_CHANNEL_ID,
                document=file_path,
                thumb=thumb_path
            )
            # Reenviar desde el canal Dump al usuario/grupo con el Bot
            await client.copy_message(chat_id=target_chat, from_chat_id=Config.DUMP_CHANNEL_ID, message_id=uploaded_msg.id)
            await owner_client.stop()
        else:
            # Archivo < 2GB: Subida normal (Puedes integrar wzgram aquí si lo prefieres)
            await client.send_document(
                chat_id=target_chat,
                document=file_path,
                thumb=thumb_path
            )

        await status_msg.edit_text("✅ **¡Descarga y subida completada!**")
        
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** {str(e)}")
        if user_client.is_connected:
            await user_client.stop()
            
    finally:
        # Limpieza de servidor
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        if 'thumb_path' in locals() and thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
