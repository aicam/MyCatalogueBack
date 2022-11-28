import pandas as pd
from .model import RegressionModel
# get data in form of pandas dataframe
def get_data(path):
    return pd.read_csv(path)

#
def get_model(path):
    print("Loading dataset....")
    data = get_data(path)
    print("Loading regression model....")
    m = RegressionModel(data)
    print("Model loading finished!")
    return m

