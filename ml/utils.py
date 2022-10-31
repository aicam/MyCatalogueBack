'''
This file provides complementary functions to complete ML
'''
import numpy as np

# Fitness Functions to plot Admission difficulty against student satisfaction.
def fitFunctAdmin(satScore, actScore, admRate):
    score = 0
    if(np.isnan(satScore)):
        score = admRate
    else:
        # Dividing SAT and ACT scores by their global avg
        score = (satScore/1059 * actScore/20) * (1-admRate)
    return score

def fitFunctSatis(compRate, tuition, tolerance):
    score = (compRate * tuition / tolerance)
    return score