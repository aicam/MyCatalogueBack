import pandas as pd
from model import OLSModel

# get data in form of pandas dataframe
def get_data(path):
    return pd.read_csv(path).dropna()

#
def get_pred_func(path):
    m = OLSModel(get_data(path))

