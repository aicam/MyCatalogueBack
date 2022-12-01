from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append('../')
from database import crud, schemas, scrypt_test
from dependencies import get_db, generate_key, get_ml_model
from ml.model import RegressionModel

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
    if scrypt_test.compareHashed(user.password, db_user.hashed_password) == False:
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
def update_profile(student_id: int, student: schemas.StudentEdit, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, student_id)
    if not db_profile:
        raise HTTPException(status_code=403, detail="Access denied")
    db_profile = crud.update_student_info(db, student, student_id)
    return db_profile

@router.post("/app/", response_model = schemas.Application)
def new_apply(app: schemas.AppBase, db: Session = Depends(get_db)):
    db_uni_app = crud.new_application(db, app)
    return db_uni_app


@router.get("/app/", response_model = List[schemas.Application])
def view_apps(student_id: int, db:Session = Depends(get_db)):
    db_app_list = crud.get_student_apps(db, student_id)
    return db_app_list

@router.post("/score/", response_model = schemas.TestScore)
def new_score(score: schemas.TestBase, db: Session = Depends(get_db)):
    db_test = crud.new_test_score(db, score)
    return db_test

@router.get("/score/", response_model = List[schemas.TestScore])
def view_scores(student: schemas.Student, db:Session = Depends(get_db)):
    db_score_list = crud.get_student_scores(db, student.user_id)
    return db_score_list

@router.patch("/score/{score_id}")
def update_score(score_id: int, new_score: schemas.TestEdit, db: Session = Depends(get_db)):
    db_test_record = crud.get_student_score(db, score_id)
    if not db_test_record:
        raise HTTPException(status_code=403, detail="Access Denied")
    db_test_record = crud.update_score_info(db, new_score, score_id)
    return db_test_record

@router.get("/recom")
def get_recommended_unis(m: RegressionModel = Depends(get_ml_model)):
    return m.get_full_list()
