import statsmodels.api as sm
from utils import fitFunctAdmin, fitFunctSatis


class OLSModel(sm.OLS):

    def __init__(self, data, **kwargs):
        self.coeffs = None
        X = [fitFunctAdmin(x['SAT_AVG'], x['ACTCMMID'], x['ADM_RATE']) for x in data]
        y = [fitFunctSatis(row['C150_4_HISP'], row['TUITIONFEE_IN'], 1) for row in data]
        super().__init__(y, X, kwargs)

    def train(self):
        self.coeffs = self.fit().params

    def predict_satis(self, x):
        ## TODO: pass the real value of admission rate instead of 0
        return self.coeffs[0] * fitFunctAdmin(x['SAT_AVG'], x['ACTCMMID'], 0) + self.coeffs['const']