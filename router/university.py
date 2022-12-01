from fastapi import APIRouter
from typing import Union
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../parentdirectory')
from database import crud, schemas, scrypt_test
from dependencies import get_db, generate_key

router = APIRouter(
    prefix="/univ"
)

# @router.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     db_user = crud.get_users(db, skip=skip, limit=limit)
#     return db_user

@router.post("/login/")
def login(user: schemas.UnivCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=403, detail="Wrong username or password")
    if scrypt_test.compareHashed(user.password, db_user.hashed_password) == False:
        raise HTTPException(status_code=403, detail="Wrong username or password")
    return {'key': generate_key(user.email)}

@router.post("/add/")
def add_univ(univ: schemas.UnivBase, db: Session = Depends(get_db)):
    return crud.create_univ(db, univ)

@router.get("/list")
def get_univ(skip: Union[int] = 0, limit: Union[int] = 100, db: Session = Depends(get_db)):
    return crud.get_univs(db, skip, limit)

@router.patch("/edit/{uni_id}")
def edit_univ_info(uni_id: int, univ: schemas.UnivEdit, db: Session = Depends(get_db)):
    db_univ = crud.get_univ_by_id(db, uni_id)
    if not db_univ:
        raise HTTPException(status_code=403, detail="Access denied")
    db_univ = crud.update_univ_info(db, univ, uni_id)
    return db_univ

@router.get("/delete/{uni_id}")
def delete_univ(uni_id: int, db: Session = Depends(get_db)):
    crud.delete_university(db, uni_id)
    return {"status": "success"}
