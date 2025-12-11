# db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_ur = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")   # FIXED: space removed

client = AsyncIOMotorClient(mongo_ur)
db = client[db_name]
