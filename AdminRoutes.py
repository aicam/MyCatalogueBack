from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database.admin.funcs import SessionLocal
from database.admin import crud, schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(user: schemas.AdminCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)