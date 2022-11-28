import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.path as p
import matplotlib.patches as patches
import statsmodels.api as sm
import math
import scipy.spatial


class RegressionModel:

    def __init__(self, data):
        self.data = data

    # sample student
    # Four Year, Hispanic, Psychology, 3.8 GPA, 1090 SAT, 24 ACT, Male, TuitionTolerance, AcceptanceThreshold
    # s = ['4',     'HISP',   'CIP42',    '3.8',    1090,    24,    'M',       1,                  0.1]

    # Fitness Functions to plot Admission difficulty against student satisfaction.
    @staticmethod
    def fitFunctAdmin(satScore, actScore, admRate):
        score = 0
        if (np.isnan(satScore)):
            score = admRate
        else:
            # Dividing SAT and ACT scores by their global avg
            score = (satScore / 1059 * actScore / 20) * (1 - admRate)
        return score

    @staticmethod
    def fitFunctSatis(compRate, tuition, tolerance):
        score = (compRate * tuition / tolerance)
        return score

    @staticmethod
    def closestPoint(stuPointX, stuPointY, adminStats, stuStats, uniPoints):
        closestId = 0
        ckdtree = scipy.spatial.cKDTree(np.column_stack([adminStats, stuStats]))
        closest = ckdtree.data[ckdtree.query([stuPointX, stuPointY])[1]]
        # uniPoints = list(uniPoints)
        uniIDSearchDict = {ID: (x, y) for ID, x, y in uniPoints}
        # print(uniIDSearchDict)
        closestId = list(uniIDSearchDict.keys())[list(uniIDSearchDict.values()).index((closest[0], closest[1]))]
        return closestId
        # print(data.loc[[closestId]])


    def pointWithinCircle(self, studentPointX, studentPointY, uniPoints, radius, square):
        # get nearest points in a circle around student point
        closestPointsID = []
        lowestPoint = ("", 100)
        for ID, x, y in uniPoints:
            # First check if point lies in square to reduce calculation time
            if (square.contains_point((x, y))):
                distance = math.sqrt(math.pow(abs(x - studentPointX), 2)) + math.pow(abs(y - studentPointY), 2)
                if (distance <= radius):
                    if (lowestPoint[1] > distance):
                        lowestPoint = (ID, distance)
                    closestPointsID.append((ID, distance))

        result = []
        for uniID, dist in closestPointsID:
            result.append((uniID, self.data["INSTNM"].values[uniID], round(dist, 3) * 1000))
        return result, lowestPoint


    def get_full_list(self, s=None):
        data = self.data
        # Variable to store University Names
        if s is None:
            s = ['4', 'HISP', 'CIP42', '3.8', 1090, 24, 'M', 1, 0.1]
        uni_names = data["INSTNM"]

        # Variable to store the sat and act scores
        sat_act_scores = data[["SAT_AVG", "ACTCMMID"]]

        # Variables ot store the Admin rate and tuition fees
        adminRate = data["ADM_RATE"]
        tuition = data["TUITIONFEE_IN"]

        # Variable to store all fields of study
        fields = data.iloc[0:, 7:197]

        # Variable to store ethnicity information
        races = data.iloc[0:, 197:]

        # Get the appropriate fields and race data for the student
        studentRace = races["C150_" + s[0] + "_" + s[1]]
        # print(singleRace)

        fieldIndex = fields.columns.get_loc(s[2] + "CERT1")
        studentFields = fields.iloc[0:, fieldIndex:fieldIndex + 5]

        # Combine all the dataframes into one

        viable_schools = sat_act_scores.join(adminRate)
        viable_schools = viable_schools.join(tuition)
        viable_schools = viable_schools.join(studentRace)
        viable_schools = viable_schools.join(studentFields)

        # Filter any schools without values in nessesary indexes
        dropIdxs = []
        for idx, row in viable_schools.iterrows():
            # Delete any rows that don't have an admission rate, tuition fee, or Completion Rate for Hispanics
            if (np.isnan(row['ADM_RATE']) or np.isnan(row['TUITIONFEE_IN']) or np.isnan(row["C150_" + s[0] + "_" + s[1]])):
                dropIdxs.append(idx)

            # Delete any rows that have a 0 or NaN in all field columns
            elif ((row[s[2] + "CERT1"] == 0.0 or np.isnan(row[s[2] + "CERT1"])) and (
                    row[s[2] + "CERT2"] == 0.0 or np.isnan(row[s[2] + "CERT2"])) and
                  (row[s[2] + "ASSOC"] == 0.0 or np.isnan(row[s[2] + "ASSOC"])) and (
                          row[s[2] + "CERT4"] == 0.0 or np.isnan(row[s[2] + "CERT4"])) and
                  (row[s[2] + "BACHL"] == 0.0 or np.isnan(row[s[2] + "BACHL"]))):
                dropIdxs.append(idx)

        viable_schools = viable_schools.drop(dropIdxs)

        # Go through all the viable schools and get the admission difficulty and student "satisfaction rate"
        adminDif = []  # Lower numbers mean easier to be admitted
        stuSatis = []  # lower numbers mean lower student satisfaction for university

        # Temp Lists to normalize values and keep track University IDs
        uniID = []
        adminTempList = []
        satisTempList = []

        # UniCoordinates = {} # Dictionary to store corrdinates of university to find point closest to user preference

        for idx, row in viable_schools.iterrows():
            valA = self.fitFunctAdmin(row['SAT_AVG'], row['ACTCMMID'], row['ADM_RATE'])
            valB = self.fitFunctSatis(row["C150_" + s[0] + "_" + s[1]], row['TUITIONFEE_IN'], 1)
            if (not (np.isnan(valA)) and not (np.isnan(valB))):
                uniID.append(idx)
                adminTempList.append(valA)
                satisTempList.append(valB)

        for val in adminDif:
            if (np.isnan(val)):
                print("BadA")

        for val in stuSatis:
            if (np.isnan(val)):
                print("BadB")

        # Have likelyhood of admission paired against student statisfaction (of filtered options)
        # Normalize values to facilate finding nearest points
        adminDif = [float(i) / max(adminTempList) for i in adminTempList]
        stuSatis = [float(i) / max(satisTempList) for i in satisTempList]

        # Zip Admission Difficulty, student Satisfaction, and University ID statistics together
        uniCoordinates = list(zip(uniID, adminDif, stuSatis))
        adminDif = pd.Series(adminDif)
        stuSatis = pd.Series(stuSatis)

        # Add a constant. Essentially, we are adding a new column (equal in lenght to x), which consists only of 1s
        x = sm.add_constant(adminDif)
        # Fit the model, according to the OLS (ordinary least squares) method with a dependent variable y
        # and an idependent x
        results = sm.OLS(stuSatis, x).fit()
        coeffs = results.params

        # Define the regression equation
        yhat = coeffs[0] * adminDif + coeffs['const']

        # Get the point of the student's GPA / SAT scores
        studentPointY = coeffs[0] * self.fitFunctAdmin(s[4], s[5], 0) + coeffs['const']
        # print(studentPointY)
        # print(studentPointX)

        # Normalize Y Point
        studentPointY = float(studentPointY) / max(adminTempList)
        studentPointX = (studentPointY - coeffs['const']) / coeffs[0]

        # Draw circle around student point
        distance_threshold = s[8]

        square = p.Path([(studentPointX + 0.1, studentPointY + 0.1),
                         (studentPointX - 0.1, studentPointY + 0.1),
                         (studentPointX - 0.1, studentPointY - 0.1),
                         (studentPointX + 0.1, studentPointY - 0.1), ])

        closeUniGroup, closestUni = self.pointWithinCircle(studentPointX, studentPointY, uniCoordinates, distance_threshold,
                                                      square)

        return closeUniGroup


