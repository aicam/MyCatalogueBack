from fastapi import FastAPI
from sqlalchemy.orm import Session

from database.admin import models
from database.admin.funcs import engine
from router import admin
models.Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
