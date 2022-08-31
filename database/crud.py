from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.AdminUser).filter(models.AdminUser.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.AdminUser).filter(models.AdminUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AdminUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.AdminCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.AdminUser(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
