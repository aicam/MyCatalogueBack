from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .funcs import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(50))
    name = Column(String(20))

class University(Base):
    __tablename__ = "university"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True)

class UniversityLabel(Base):
    __tablename__ = "university_scores"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer)
    label_name = Column(String(50))
    label_min = Column(String(50))
    label_mid = Column(String(50))
    label_max = Column(String(50))