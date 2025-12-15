from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserOut
from models import create_user_db, get_user_by_email  # ✅ correct functions

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # ✅ CALL create_user_db instead of create_patient_db
    return await create_user_db(user.dict())
