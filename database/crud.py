from sqlalchemy.orm import Session

from database import models, schemas, scrypt_funcs


def get_user(db: Session, user_id: int):
    return db.query(models.SystemUser).filter(models.SystemUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.SystemUser).filter(models.SystemUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SystemUser).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.AdminCredentials):
    hashed = scrypt_funcs.getHashed(user.password)
    db_user = models.SystemUser(email=user.email, hashed_password=hashed, role=user.role, university_name=user.university_name)
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
    found = db.query(models.StudentInfo).filter(models.StudentInfo.user_id == user_id).first()
    if found:
        return found
    sample = models.StudentInfo(user_id=user_id)
    db.add(sample)
    db.commit()
    return sample

def get_student_apps(db: Session, student_id: int):
    return db.query(models.StudentApplications).filter(models.StudentApplications.student_id == student_id).all()

def get_uni_apps(db: Session, uni_name: str):
    all_apps = db.query(models.StudentApplications).filter(models.StudentApplications.uni_name == uni_name).all()
    apps_conv = []
    for app in all_apps:
        student_info = db.query(models.StudentInfo).filter(models.StudentInfo.user_id == app.student_id).first()
        apps_conv.append({
            "uni_name": uni_name,
            "date_applied": app.app_date,
            "student": student_info,
            "full_name": student_info.f_name + ' ' + student_info.l_name,
            "app_id": app.app_id,
            "approved": app.approved
        })
    return apps_conv
def get_student_scores(db: Session, student_id: int):
    return db.query(models.TestScores).filter(models.TestScores.student_id == student_id).all()

def get_student_score(db: Session, score_id: int):
    return db.query(models.TestScores).filter(models.TestScores.score_id == score_id).first()

# new update methods
def update_student_info(db: Session, student: schemas.StudentEdit, user_id: int):
    db_student = get_profile(db, user_id)
    db_student.gpa = student.gpa
    db_student.f_name = student.f_name
    db_student.l_name = student.l_name
    db_student.act_score = student.act_score
    db_student.sat_score = student.sat_score
    db_student.ethnicity = student.ethnicity
    db_student.sex = student.sex
    db.commit()
    return db_student


def new_application(db: Session, app: schemas.AppBase):
    db_new_app = models.StudentApplications(uni_name = app.uni_name, app_date = app.app_date, student_id = app.student_id)
    db.add(db_new_app)
    db.commit()
    db.refresh(db_new_app)
    return db_new_app

def new_test_score(db: Session, score: schemas.TestBase):
    db_new_score = models.TestScores(test_name = score.test_name, t_score = score.t_score, student_id = score.student_id)
    db.add(db_new_score)
    db.commit()
    db.refresh(db_new_score)
    return db_new_score

def update_score_info(db: Session, score: schemas.TestEdit, score_id: int):
    db_score = get_student_score(db, score_id)
    score_data = score.dict(exclude_unset=True)
    for key,value in score_data.items():
        setattr(db_score, key, value)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

# delete functions
def delete_university(db: Session, id: int):
    db_uni = db.query(models.UnivInfo).filter(models.UnivInfo.uni_id == id).first()
    db.delete(db_uni)
    db.commit()

def delete_user(db: Session, id: int):
    db_user = db.query(models.SystemUser).filter(models.SystemUser.id == id).first()
    db.delete(db_user)
    db.commit()

def approve_app(db: Session, id: int):
    db_app = db.query(models.StudentApplications).filter(models.StudentApplications.app_id == id).first()
    db_app.approved = True
    db.commit()