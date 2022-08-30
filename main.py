from fastapi import FastAPI
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
