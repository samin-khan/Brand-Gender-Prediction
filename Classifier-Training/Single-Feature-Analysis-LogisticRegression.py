import pandas as pd
import numpy as np
import operator
import time
import pickle
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression

# =========== HUMAN NAME LOGISTIC REGRESSION ANALYSIS =================
human_data = 'human_data.csv'
dfCompact = pd.DataFrame.from_csv(human_data)

"""LOOCV ANALYSIS"""
# Change parameter depending on target feature
# dfLooTest = dfCompact.drop(["dataID"], axis=1).sample(frac=1) # Uncomment if dataID column exists
dfLooTest = dfCompact.drop(["Name"], axis=1).sample(frac=1) 

# Timing LOOCV runtime
t0 = time.time()
all_analysis = [("Feature", "Overall Accuracy", "Male Accuracy", "Female Accuracy", "Runtime")]
short_analysis = [("Feature", "Overall Accuracy")]

for feature in dfLooTest.columns[1:]:
    # Uses Leave One Out Cross Validation (LOOCV) to estimate how training model would do on predicting external data
    loo = KFold(n_splits=5)
    dfTest = dfLooTest[['Gender', feature]]
    x = dfTest.drop(['Gender'], axis=1).as_matrix()
    y = dfTest[['Gender']].as_matrix().ravel()
    
    t01 = time.time()
    
    male_total = 0
    correct_male = 0
    female_total = 0
    correct_female = 0
 
    name_index = 0
    for train_index, test_index in loo.split(x):
        model = LogisticRegression()        
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        model.fit(x_train, y_train)
        # Create a for loop to iterate over the 10th of the set being validated
        # Must account for randomizing when indexing the name for reporting predictions.
        for t_index in range(len(y_test)):
            prediction = model.predict(x_test[t_index])
            if y_test[t_index] == [0]:
                male_total += 1
                correct_male += 1 if prediction == y_test[t_index] else 0
            else:
                female_total += 1
                correct_female += 1 if prediction == y_test[t_index] else 0
            name_index += 1
    overallAcc = (correct_male + correct_female) / (male_total + female_total)
    maleAcc = correct_male / male_total
    femaleAcc = correct_female / female_total

    t1 = time.time()
    runtime = t1 - t01
    
    all_analysis.append((feature, overallAcc, maleAcc, femaleAcc, runtime))

dfAnalysis = pd.DataFrame(all_analysis)    
dfAnalysis.to_csv("single_analysis.csv")

