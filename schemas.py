from pydantic import BaseModel, Field, EmailStr

# ---------- PATIENT ----------

class Hospital(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    weight: float = Field(..., gt=0, le=100)
    age: int = Field(..., ge=1, le=90)
    desease: str = Field(..., min_length=5, max_length=50)

class CreatePatient(Hospital):
    pass

class PatientOut(Hospital):
    id: str


# ---------- USER (AUTH) ----------

class UserBase(BaseModel):
    email: EmailStr
    user_name: str = Field(..., min_length=3, max_length=30)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserOut(UserBase):
    id: str
