from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from .funcs import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(50))
    name = Column(String(20))

class UnivInfo(Base):
    __tablename__ = "univ_info"
    uni_id = Column(Integer, primary_key=True, index=True)
    uni_name = Column(String(100))
    min_sat = Column(Integer)
    min_act = Column(Integer)
    capacity = Column(Integer)
    accept_rate = Column(DECIMAL(3,1))
