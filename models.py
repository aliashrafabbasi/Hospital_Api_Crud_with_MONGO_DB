# models.py
from bson import ObjectId
from db import db

collection = db.members


def patient_helper(member) -> dict:
    return {
        "id": str(member["_id"]),
        "name": str(member["name"]),
        "weight": float(member["weight"]),
        "age": int(member["age"]),
        "desease": str(member["desease"])
    }


async def create_patient_db(data: dict):
    result = await collection.insert_one(data)
    new = await collection.find_one({"_id": result.inserted_id})
    return patient_helper(new)


async def get_all_patients_db():
    patients = []
    async for i in collection.find():
        patients.append(patient_helper(i))
    return patients


async def update_patient_db(patient_id: str, data: dict):
    updated = await collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": data}
    )

    if updated.matched_count == 0:
        return None

    new_data = await collection.find_one({"_id": ObjectId(patient_id)})
    return patient_helper(new_data)


async def delete_patient_db(patient_id: str):
    deleted = await collection.delete_one({"_id": ObjectId(patient_id)})
    return deleted.deleted_count > 0


async def search_patient_db(name: str):
    patients = []
    query = {"name": {"$regex": name, "$options": "i"}}

    async for i in collection.find(query):
        patients.append(patient_helper(i))
    
    return patients
