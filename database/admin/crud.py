from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.SystemUser).filter(models.SystemUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.SystemUser).filter(models.SystemUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SystemUser).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.AdminCredentials):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.SystemUser(email=user.email, hashed_password=fake_hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

''' University '''
def get_univs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UnivInfo).offset(skip).limit(limit).all()

def get_univ_by_id(db: Session, uni_id: int):
    return db.query(models.UnivInfo).filter(models.UnivInfo.uni_id == uni_id).first()

def get_univ(db: Session, name: str):
    return db.query(models.SystemUser).filter(models.UnivInfo.uni_name == name).first()
def create_univ(db: Session, univ: schemas.UnivBase):
    curr_univ = get_univ(db, univ.uni_name)
    if curr_univ:
        return {"status": "exist"}
    db_univ = models.UnivInfo(uni_name=univ.uni_name, min_sat=univ.min_sat, min_act=univ.min_act,
                              capacity=univ.capacity, accept_rate=univ.accept_rate)
    db.add(db_univ)
    db.commit()
    db.refresh(db_univ)
    return db_univ


def update_univ_info(db: Session, univ: schemas.UnivEdit, uni_id: int):
    db_uni = db.query(models.UnivInfo).filter(models.UnivInfo.uni_id == uni_id).first()
    univ_data = univ.dict(exclude_unset=True)
    for key, value in univ_data.items():
        setattr(db_uni, key, value)
    db.add(db_uni)
    db.commit()
    db.refresh(db_uni)
    return db_uni

# new functions
def get_profile(db: Session, user_id:int):
    return db.query(models.StudentInfo).filter(models.StudentInfo.user_id == user_id).first()

def get_student_apps(db: Session, user_id: int):
    return db.query(models.StudentApplications).filter(models.StudentApplications.user_id == user_id)

def update_student_info(db: Session, student: schemas.StudentEdit, user_id: int):
    db_student = get_profile(db, user_id)
    student_data = student.dict(exclude_unset=True)
    for key,value in student_data.items():
        setattr(db_student, key, value)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def new_application(db: Session, app: schemas.AppBase):
    db_new_app = models.StudentApplications(uni_name = app.uni_name, app_date = app.app_date, student_id = app.student_id)
    db.add(db_new_app)
    db.commit()
    db.refresh(db_new_app)
    return db_new_app
