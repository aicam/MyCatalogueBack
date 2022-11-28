from database.funcs import SessionLocal
from cryptography.fernet import Fernet
from ml.main import get_model
import os
dataset_path = "ml/dataset/UseableDataDraft1.csv"
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

def get_ml_model():
    m = get_model()
    return m