'''
This file provides complementary functions to complete ML
'''
import numpy as np
import scipy
import math

# Fitness Functions to plot Admission difficulty against student satisfaction.
def fitFuncAdmin(satScore, actScore, admRate):
    score = 0
    if(np.isnan(satScore)):
        score = admRate
    else:
        # Dividing SAT and ACT scores by their global avg
        score = (satScore/1059 * actScore/20) * (1-admRate)
    return score

def fitFuncSatis(compRate, tuition, tolerance):
    score = (compRate * tuition / tolerance)
    return score

def closestPoint(stuPointX, stuPointY, adminStats, stuStats, uniPoints):
    ckdtree = scipy.spatial.cKDTree(np.column_stack([adminStats, stuStats]))
    closest = ckdtree.data[ckdtree.query([stuPointX, stuPointY])[1]]
    uniIDSearchDict = {ID: (x,y) for ID, x, y in uniPoints}
    closestId = list(uniIDSearchDict.keys())[list(uniIDSearchDict.values()).index((closest[0],closest[1]))]
    return closestId

def pointWithinCircle(data, uniPoints):
    closestPointsID = []

    for ID, x, y in uniPoints:
        if (square.contains_point((x,y))):
            if ( math.sqrt(math.pow((x - studentPointX),2))+math.pow((y - studentPointY),2) <= 0.1):
                closestPointsID.append(ID)

    result = []
    for uniID in closestPointsID:
        result.append((uniID, data["INSTNM"].values[uniID]))
    return result