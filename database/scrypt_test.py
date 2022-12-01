from hashlib import scrypt
import os

def genSalt():
	salt = os.urandom(16)
	return salt

def getHashed(password, salt):
	pw = password
	hashed = scrypt(pw, n=64, r=8, p=1, salt=salt, dklen=44)
	return hashed

def compareHashed(password, saltHash):
	salt = saltHash[:16]
	inputHash = getHashed(password, salt)
	return inputHash == saltHash[16:]

