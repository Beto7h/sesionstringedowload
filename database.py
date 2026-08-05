from motor.motor_asyncio import AsyncIOMotorClient
from configure import DATABASE_URL

# Conectar a MongoDB
client = AsyncIOMotorClient(DATABASE_URL)
db = client["leech_bot_db"]
users_collection = db["users"]

async def get_user(user_id):
    """Obtiene los datos del usuario. Si no existe, crea un perfil por defecto."""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        user = {
            "_id": user_id, 
            "session_string": None, 
            "auto_thumb_hd": True # Activado por defecto
        }
        await users_collection.insert_one(user)
    return user

async def update_user(user_id, data: dict):
    """Actualiza campos específicos del usuario."""
    await users_collection.update_one({"_id": user_id}, {"$set": data}, upsert=True)

async def reset_user(user_id):
    """Resetea la configuración del usuario a los valores de fábrica."""
    default_data = {"session_string": None, "auto_thumb_hd": True}
    await users_collection.update_one({"_id": user_id}, {"$set": default_data}, upsert=True)
