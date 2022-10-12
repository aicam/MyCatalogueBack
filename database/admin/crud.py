from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.SystemUser).filter(models.SystemUser.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.SystemUser).filter(models.SystemUser.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SystemUser).offset(skip).limit(limit).all()

def get_univ(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UnivInfo).offset(skip).limit(limit).all()

def get_univ_by_id(db: Session, uni_id: int):
    return db.query(models.UnivInfo).filter(models.UnivInfo.uni_id == uni_id).first()

def update_univ_info(db: Session, univ: schemas.UnivEdit, uni_id:int):
    db_uni = get_univ_by_id(db, uni_id)
    univ_data = univ.dict(exclude_unset=True)
    for key,value in univ_data.items():
        setattr(db_uni, key, value)
    db.add(db_uni)
    db.commit()
    db.refresh(db_uni)
    return db_uni


def create_user(db: Session, user: schemas.AdminCredentials):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.SystemUser(email=user.email, hashed_password=fake_hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
