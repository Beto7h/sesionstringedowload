from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

client = AsyncIOMotorClient(Config.MONGO_URI)
db = client['leech_bot_db']
users_collection = db['users']

async def get_user_config(user_id):
    user = await users_collection.find_one({"user_id": user_id})
    if not user:
        default_config = {
            "user_id": user_id,
            "string_session": None,
            "custom_thumbnail": None,
            "hd_thumbnail_active": False,
            "pm_mode": False
        }
        await users_collection.insert_one(default_config)
        return default_config
    return user

async def update_user_config(user_id, update_data):
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": update_data},
        upsert=True
    )
