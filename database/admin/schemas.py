from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

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
