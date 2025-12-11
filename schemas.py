# schemas.py
from pydantic import BaseModel

class Hospital(BaseModel):
    name: str
    weight: float
    age: int
    desease: str

class create_patient(Hospital):
    pass

class patient_out(Hospital):
    id: str
