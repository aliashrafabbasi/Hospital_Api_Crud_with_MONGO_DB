from bson import ObjectId
from db import db
from passlib.context import CryptContext

# ---------- COLLECTIONS ----------
patients_collection = db.patients
users_collection = db.users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- HELPERS ----------
def patient_helper(p) -> dict:
    return {
        "id": str(p["_id"]),
        "name": p["name"],
        "weight": p["weight"],
        "age": p["age"],
        "desease": p["desease"]
    }

def hash_password(password: str) -> str:
    # Bcrypt max 72 bytes, truncate if longer
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain.encode("utf-8")[:72], hashed)


# ---------- PATIENT CRUD ----------
async def create_patient_db(data: dict):
    result = await patients_collection.insert_one(data)
    new = await patients_collection.find_one({"_id": result.inserted_id})
    return patient_helper(new)

async def get_all_patients_db():
    patients = []
    async for p in patients_collection.find():
        patients.append(patient_helper(p))
    return patients

async def update_patient_db(patient_id: str, data: dict):
    updated = await patients_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": data}
    )
    if updated.matched_count == 0:
        return None
    new = await patients_collection.find_one({"_id": ObjectId(patient_id)})
    return patient_helper(new)

async def delete_patient_db(patient_id: str):
    deleted = await patients_collection.delete_one({"_id": ObjectId(patient_id)})
    return deleted.deleted_count > 0

async def search_patient_db(name: str):
    patients = []
    query = {"name": {"$regex": name, "$options": "i"}}
    async for p in patients_collection.find(query):
        patients.append(patient_helper(p))
    return patients

# ---------- AUTH ----------
async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def create_user_db(data: dict):
    data["password"] = hash_password(data["password"])
    result = await users_collection.insert_one(data)
    new_user = await users_collection.find_one({"_id": result.inserted_id})
    return {
        "id": str(new_user["_id"]),
        "email": new_user["email"],
        "user_name": new_user["user_name"]
    }
