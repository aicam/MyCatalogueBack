from pydantic import BaseModel

class AdminBase(BaseModel):
    email: str
class AdminCreate(AdminBase):
    password: str
class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True