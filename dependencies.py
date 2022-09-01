from database.admin.funcs import SessionLocal
from cryptography.fernet import Fernet
import os

server_key = os.environ['SERVER_KEY']
fernet = Fernet(server_key.encode())

def generate_key(info: str):
    return fernet.encrypt(info.encode())

def decrypt_key(enc: str):
    return fernet.decrypt(enc.encode())
def get_db():
    dbCon = SessionLocal()
    try:
        yield dbCon
    finally:
        dbCon.close()