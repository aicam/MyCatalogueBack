from hashlib import sha384


def getHashed(password):
	return sha384(password.encode()).hexdigest()[:18]

def compareHashed(password, truePass):
	inputHash = getHashed(password)
	return inputHash == truePass

