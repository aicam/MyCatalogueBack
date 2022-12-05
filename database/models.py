from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, Date, BINARY
from sqlalchemy.orm import relationship

from .funcs import Base


class SystemUser(Base):
    __tablename__ = "system_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(1000))
    role = Column(String(10))
    university_name = Column(String(200))

class UnivInfo(Base):
    __tablename__ = "univ_info"
    uni_id = Column(Integer, primary_key=True, index=True)
    uni_name = Column(String(100))
    min_sat = Column(Integer)
    min_act = Column(Integer)
    capacity = Column(Integer)
    accept_rate = Column(DECIMAL(3,1))

class StudentInfo(Base):
    __tablename__ = "student_info"
    id = Column(Integer, primary_key=True, index = True)
    f_name = Column(String(30))
    l_name = Column(String(30))
    sat_score = Column(Integer)
    act_score = Column(Integer)
    gpa = Column(DECIMAL(2,1))
    ethnicity = Column(String(30))
    sex = Column(String(2))
    user_id = Column(Integer, ForeignKey("system_users.id"))

# table to store university application for student ids
class StudentApplications(Base):
    __tablename__ = "student_apps"
    app_id = Column(Integer, primary_key=True, index = True)
    uni_name = Column(String(100))
    app_date = Column(Date)
    student_id = Column(Integer, ForeignKey("student_info.user_id"))
    approved = Column(Boolean, default=False)


# table to store additional test_scores for student ids
class TestScores(Base):
    __tablename__ = "test_scores"
    score_id = Column(Integer, primary_key=True, index = True)
    test_name = Column(String(30))
    t_score = Column(Integer)
    student_id = Column(Integer, ForeignKey("student_info.user_id"))
