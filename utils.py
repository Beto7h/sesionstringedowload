import time
import math
import psutil
import shutil

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f}{power_labels[n]}"

async def progress_bar(current, total, status_msg, start_time, file_name, task_by_name, task_by_id):
    now = time.time()
    diff = now - start_time
    
    # Actualizar cada 3 segundos para no saturar la API de Telegram
    if round(diff % 3.00) != 0 and current != total:
        return

    speed = current / diff if diff > 0 else 0
    time_to_completion = round((total - current) / speed) if speed > 0 else 0
    percentage = current * 100 / total
    
    # Crear bloques de barra
    completed_blocks = int(math.floor(percentage / 10))
    bar = "■" * completed_blocks + "□" * (10 - completed_blocks)
    
    # Estadísticas del sistema
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = shutil.disk_usage('/')
    free_disk = format_bytes(disk.free)
    disk_percent = disk.percent

    # Formato traducido tal cual lo pediste
    text = (
        f"📄 {file_name}\n\n"
        f"Task By {task_by_name}  ( #ID{task_by_id} ) [Link]\n"
        f"┟ [{bar}] {percentage:.1f}%\n"
        f"┠ Procesado → {format_bytes(current)} de {format_bytes(total)}\n"
        f"┠ Estado → Descargando\n"
        f"┠ Velocidad → {format_bytes(speed)}/s\n"
        f"┠ Tiempo → {time_to_completion}s\n"
        f"┠ Motor → Pyrogram/Wzgram\n" # Ajustado a la realidad del motor
        f"┠ In Mode → #Telegram\n"
        f"┠ Out Mode → #Leech\n"
        f"┖ Stop → /cancel\n\n"
        f"⌬ Bot Stats\n"
        f"┟ CPU → {cpu}% | F → {free_disk} [{disk_percent}%]\n"
        f"┖ RAM → {ram}%"
    )
    
    try:
        await status_msg.edit_text(text)
    except:
        pass
