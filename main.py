from fastapi import FastAPI, HTTPException
from bson import ObjectId
from schemas import CreatePatient, PatientOut
from models import (
    create_patient_db,
    get_all_patients_db,
    update_patient_db,
    delete_patient_db,
    search_patient_db
)
from auth.auth_routes import router as auth_router

app = FastAPI(
    title="Hospital Management System",
    version="1.0.0"
)

# ---------- UTILS ----------
def validate_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return id

# ---------- ROUTERS ----------
app.include_router(auth_router)

# ---------- PATIENT ROUTES ----------

@app.post("/patients", response_model=PatientOut)
async def create_patient(patient: CreatePatient):
    return await create_patient_db(patient.dict())

@app.get("/patients", response_model=list[PatientOut])
async def get_patients():
    return await get_all_patients_db()

@app.put("/patients/{patient_id}", response_model=PatientOut)
async def update_patient(patient_id: str, data: CreatePatient):
    validate_object_id(patient_id)
    updated = await update_patient_db(patient_id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated

@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: str):
    validate_object_id(patient_id)
    deleted = await delete_patient_db(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

@app.get("/patients/search", response_model=list[PatientOut])
async def search_patient(name: str):
    return await search_patient_db(name)
