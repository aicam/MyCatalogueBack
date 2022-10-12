from fastapi import APIRouter, Request, Response
from fastapi import Depends, HTTPException
from fastapi.routing import APIRoute
import time
from typing import Callable
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append('../parentdirectory')
from database.admin import schemas, crud
from dependencies import get_db, generate_key


class AdminMiddleWare(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler

router = APIRouter(
    prefix="/admin",
    route_class=AdminMiddleWare
)
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.AdminCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/univ/", response_model=List[schemas.Univ])
def read_univ(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_univ = crud.get_univs(db, skip=skip, limit=limit)
    return all_univ

@router.post("/login/")
def login(user: schemas.AdminCredentials, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=403, detail="Wrong username or password")
    if db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(status_code=403, detail="Wrong username or password")
    if db_user.role != user.role:
        raise HTTPException(status_code=403, detail="Wrong username or password")
    return {'key': generate_key(user.email)}
