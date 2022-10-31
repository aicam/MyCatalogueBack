from ml.main import get_model

path = "./ml/dataset/UseableDataDraft1.csv"

print("Model is loading...")
m = get_model(path)
print("Model loaded")

## check if prints the satisfaction rate
print(m.predict_satis({"SAT_AVG": 10, "ACTCMMID": 10}))

