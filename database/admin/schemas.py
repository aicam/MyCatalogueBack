from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import datetime

class RoleEnum(str, Enum):
    student = 'student'
    univ = 'univ'
    admin = 'admin'


class UserBase(BaseModel):
    email: str
class AdminCredentials(UserBase):
    password: str
    role: RoleEnum = RoleEnum.admin
class StudentCredentials(UserBase):
    password: str
    role: RoleEnum = RoleEnum.student
class UnivCredentials(UserBase):
    password: str
    role: RoleEnum = RoleEnum.univ
class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class UnivBase(BaseModel):
    uni_name: str
    min_sat: int
    min_act: int
    capacity: int
    accept_rate: float

class Univ(UnivBase):
    uni_id: int
    class Config:
        orm_mode = True
 
class UnivEdit(BaseModel):
    uni_name: Optional[str] = None
    min_sat: Optional[int] = None
    min_act: Optional[int] = None
    capacity: Optional[int] = None
    accept_rate: Optional[float] = None
 
class StudentBase(BaseModel):
    f_name: str
    l_name: str
    sat_score: int
    act_score: int
    gpa: float

class Student(StudentBase):
    user_id: int
    class Config:
        orm_mode = True

class StudentEdit(BaseModel):
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    sat_score: Optional[int] = None
    act_score: Optional[int] = None
    gpa: Optional[float] = None

class AppBase(BaseModel):
    uni_name: str
    app_date: datetime.date
    student_id: int

class Application(AppBase):
    app_id: int
    class Config:
        orm_mode = True
