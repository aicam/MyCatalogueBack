from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../parentdirectory')
from database import schemas, crud
from dependencies import get_db

router = APIRouter(
    prefix="/admin"

)

@router.post("/users/", response_model=schemas.Admin)
def create_user(user: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)