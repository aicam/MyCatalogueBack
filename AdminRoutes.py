from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from db import crud, models, schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(user: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)