from fastapi import FastAPI, HTTPException
from bson import ObjectId
from schemas import create_patient, patient_out
from models import (
    create_patient_db,
    get_all_patients_db,
    update_patient_db,
    delete_patient_db,
    search_patient_db
)

app = FastAPI(
    title="Hospital Management System API with MongoDB",
    description="A fully asynchronous FastAPI CRUD service using Motor and MongoDB.",
    version="1.0.0"
)


# 🔹 ObjectId validation helper
def validate_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Invalid patient id format"
        )
    return ObjectId(id)


@app.post("/create_patient", response_model=patient_out)
async def add_patients(patient: create_patient):
    new_patient = await create_patient_db(patient.dict())
    return new_patient


@app.get("/view_all_patients", response_model=list[patient_out])
async def fetch_patients():
    return await get_all_patients_db()


@app.put("/patient/{patient_id}", response_model=patient_out)
async def update_patient_route(patient_id: str, data: create_patient):
    obj_id = validate_object_id(patient_id)

    updated_patient = await update_patient_db(str(obj_id), data.dict())

    if updated_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found!")

    return updated_patient


@app.delete("/patient/{patient_id}")
async def delete_patient_route(patient_id: str):
    obj_id = validate_object_id(patient_id)

    deleted = await delete_patient_db(str(obj_id))

    if not deleted:
        raise HTTPException(status_code=404, detail=f"{patient_id} Patient not found!")

    return {"message": f"{patient_id} Patient deleted successfully!"}


@app.get("/patient/search", response_model=list[patient_out])
async def search_patient_route(name: str):
    patients = await search_patient_db(name)

    if not patients:
        raise HTTPException(status_code=404, detail="No patient found!")

    return patients
