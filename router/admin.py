from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append('../parentdirectory')
from database.admin import schemas, crud
from dependencies import get_db, generate_key

router = APIRouter(
    prefix="/admin"
)

@router.post("/users/", response_model=schemas.Admin)
def create_user(user: schemas.AdminCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.Admin])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/login/")
def login(user: schemas.AdminCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=403, detail="Wrong username or password")
    if db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(status_code=403, detail="Wrong username or password")
    return {'key': generate_key(user.email)}