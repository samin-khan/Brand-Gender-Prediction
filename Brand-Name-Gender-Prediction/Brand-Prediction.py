import pandas as pd
import numpy as np

from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

from openpyxl import load_workbook
import operator
import pickle
import time
import math

human_data = 'human_data.csv'
dfCompact = pd.DataFrame.from_csv(human_data)

# ========= Logistic Regression and Random Forest Classifier =============
"""LOOCV ANALYSIS"""
# Change parameter depending on target feature
dfLooNames = dfCompact.drop(["dataID"], axis=1)
dfLooTest = dfLooNames.drop(["Name"], axis=1)

x = dfLooTest.drop(['Gender'], axis=1).as_matrix()
y = dfLooTest[['Gender']].as_matrix().ravel()
    
model_LR = LogisticRegression()        
model_LR.fit(x, y)

model_RF = RandomForestClassifier()
model_RF.fit(x, y)

# ========= Logistic Regression Vowel Ending Classifier =============

dfVowelTest = dfLooTest[["Gender", "VowelEnding? (a, e, i, o, u,y)"]]
x = dfVowelTest.drop(['Gender'], axis=1).as_matrix()
y = dfVowelTest[['Gender']].as_matrix().ravel()

model_vowel_end = LogisticRegression()        
model_vowel_end.fit(x, y)

# Making lists containing predictions from each classifier
dfBrands = pd.DataFrame.from_csv('brand_name_coded.csv')

predict_LR = [("Name", "Category", "Gender")]
predict_RF = [("Name", "Category", "Gender")]
predict_vowel = [("Name", "Category", "Gender")]

for i in range(len(dfBrands.index)):
    name = dfBrands.iloc[i][0]
    category = dfBrands.iloc[i][1]
    feature_vector = dfBrands.iloc[i][2:]
    vowel_feature = dfBrands.iloc[i][11]
    predict_LR.append((name, category, model_LR.predict(feature_vector)[0]))
    predict_RF.append((name, category, model_RF.predict(feature_vector)[0]))
    predict_vowel.append((name, category, model_vowel_end.predict(vowel_feature)[0]))

# Generating lists for predictions depending on which classifiers predicted the same
all_agree = [("Name", "Category", "Gender")]
differ_1 = [("Name", "Category")]
majority = [("Name", "Category", "Gender")]

for i in range(1, len(predict_LR)):
    if predict_LR[i] == predict_RF[i] == predict_vowel[i]:
        all_agree.append(predict_LR[i])
    else:
        differ_1.append(predict_LR[i][:2])
    if predict_LR[i] == predict_RF[i]:
        majority.append(predict_LR[i])
    else:
        majority.append(predict_vowel[i])

# Generate csvs
pd.DataFrame(all_agree).to_csv("all_agreed.csv")
pd.DataFrame(differ_1).to_csv("one_differs.csv") 
pd.DataFrame(majority).to_csv("majority_brand_predictions.csv") 

