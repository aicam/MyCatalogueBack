from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append('../parentdirectory')
from database.admin import schemas, crud
from dependencies import get_db, generate_key

router = APIRouter(
    prefix="/student"
)

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.StudentCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=schemas.User)
def read_users(user: schemas.StudentCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = user.email)
    return db_user

@router.get("/users/all")
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.post("/login/")
def login(user: schemas.StudentCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=403, detail="Wrong username or password")
    if db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(status_code=403, detail="Wrong username or password")
    if db_user.role != 'student' or db_user.role != user.role:
        raise HTTPException(status_code=403, detail="Wrong username or password")
    return {'key': generate_key(user.email)}

# new definition
@router.get("/profile/{student_id}", response_model=schemas.Student)
def view_profile(student_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, student_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="User not found")
    return db_profile

@router.patch("/profile/{student_id}")
def update_profile(student_id: int, student: schemas.StudentEdit ,db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, student_id)
    if not db_profile:
        raise HTTPException(status_code=403, detail="Access denied")
    db_profile = crud.update_student_info(db, student, student_id)
    return db_profile

@router.post("/app/", response_model = schemas.Application)
def new_apply(app: schemas.AppBase, db: Session = Depends(get_db)):
    db_uni_app = crud.new_application(db, app)
    return db_uni_app
