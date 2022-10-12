from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append('../parentdirectory')
from database.admin import schemas, crud
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
    if db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(status_code=403, detail="Wrong username or password")
    return {'key': generate_key(user.email)}

@router.patch("/edit/{uni_id}")
def edit_univ_info(uni_id: int, univ: schemas.UnivEdit, db: Session = Depends(get_db)):
    db_univ = crud.get_univ_by_id(db, uni_id)
    if not db_univ:
        raise HTTPException(status_code=403, detail="Access denied")
    db_univ = crud.update_univ_info(db, univ, uni_id)
    return db_univ
