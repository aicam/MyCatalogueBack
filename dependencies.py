from database.database import SessionLocal
import database

def get_db():
    dbCon = SessionLocal()
    try:
        yield dbCon
    finally:
        dbCon.close()