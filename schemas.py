# schemas.py
from pydantic import BaseModel,Field
from typing import Literal

class Hospital(BaseModel):
    name:str=Field(...,min_length=3,max_length=50) 
    weight: float=Field(...,gt=0,le=100)
    age: int=Field(...,ge=1,le=90)
    desease: str=Field(...,min_length=5,max_length=50)

class create_patient(Hospital):
    pass

class patient_out(Hospital):
    id: str
