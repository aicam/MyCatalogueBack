import pandas as pd
from .model import RegressionModel

# TODO: add dataset path to environment variable
data = pd.read_csv("ml/dataset/UseableDataDraft1.csv")
#
def get_model():
    m = RegressionModel(data)
    return m

