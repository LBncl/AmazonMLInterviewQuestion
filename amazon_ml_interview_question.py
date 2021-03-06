# -*- coding: utf-8 -*-
"""Amazon ML Interview Question.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MqJk1Wf_dkRMzoR-3A1MQYZqcaV38Bwp
"""

import pandas as pd
import numpy as np
#import sweetviz as sv
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from datetime import datetime
import matplotlib.pyplot as plt

# Read data, supply data types to improve optimisation to stop pandas inferring data types.
headers = ['Price', 'Date of Transfer', 'Property Type', 'Duration', 'Town/City']
dtypes = {'Price': 'int', 'Date of Transfer': 'str', 'Property Type': 'str', 'Town/City': 'str'}
parse_dates = ['Price']
pp_1995_raw = pd.read_csv('pp-1995.csv', header=None, names=headers, dtype=dtypes, parse_dates=parse_dates)

# --- DATA CLEANING START ---
# Convert Town/city column to a categorical variable with 1 representing London and 0 everything else
pp_1995_raw['Town/City'] = pp_1995_raw['Town/City'].map({'LONDON': 1})
pp_1995_raw['Town/City'] = pp_1995_raw['Town/City'].fillna(0)

# remove time component of the datatime variable type and cast to month datatype
pp_1995_raw['Date of Transfer'] = pd.to_datetime(pp_1995_raw['Date of Transfer'])

# factorise columns
pp_1995_raw['Property Type'] = pp_1995_raw['Property Type'].astype('category')
pp_1995_raw['Property Type'] = pp_1995_raw['Property Type'].cat.codes

pp_1995_raw['Duration'] = pp_1995_raw['Duration'].astype('category')
pp_1995_raw['Duration'] = pp_1995_raw['Duration'].cat.codes

pp_1995_mod = pp_1995_raw.drop('Date of Transfer', 1)
pp_1995_mod['Price'] = pp_1995_mod['Price'].astype(int)

y = pp_1995_mod.iloc[:, 0]
X = pp_1995_mod.iloc[:, 1:4]

# View effect of data cleaning
#print(pp_1995_raw.dtypes)
#print(pp_1995_mod.head())

# --- DATA CLEANING END ---

# --- EDA START ---
report = sv.analyze(pp_1995_raw)
report.show_html("Report.html")
# --- EDA END ---

# --- DATA PRE-PROCESSING START ---
# split data into test and train. using the first 80% as training data and the last 20 % as test data.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

# Feature selection
selector = SelectKBest(f_classif, k='all')
selector.fit(X_train, y_train)
scores = selector.pvalues_

X_indices = np.arange(X.shape[-1])

plt.figure(1)
plt.clf()
plt.bar(X_indices, scores, width=0.2)
plt.title("Feature univariate score")
plt.xlabel("Feature number")
plt.ylabel(r"Univariate score")
plt.show()

# --- DATA PRE-PROCESSING END ---

selector.pvalues_

# --- MODEL 1 START ---
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import seaborn as sns

# creating an object of LinearRegression class
LR = LinearRegression()

# fitting the training data
LR.fit(X_train, y_train)

# Apply to test data 
y_prediction =  LR.predict(X_test)

# Compare
pred_df=pd.DataFrame({'Actual Value':y_test,'Predicted Value':y_prediction,'Difference':y_test-y_prediction})

# Evaluation
print(r2_score(y_test, y_prediction))
print(pred_df["Difference"].mean())

# Visualisation
sns.set_theme(color_codes=True)
sns.regplot(x="Difference", y="Predicted Value", data=pred_df);

# --- MODEL 1 END ---

# --- MODEL 2 START ---

# Fitting Random Forest Regression to the dataset
# import the regressor
from sklearn.ensemble import RandomForestRegressor
 
 # create regressor object
regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
 
# fit the regressor with x and y data
regressor.fit(X_train, y_train) 

# Apply to test data 
y_prediction =  regressor.predict(X_test)

# Compare
pred_df=pd.DataFrame({'Actual Value':y_test,'Predicted Value':y_prediction,'Difference':y_test-y_prediction})

# Evaluation
print(r2_score(y_test, y_prediction))
print(pred_df["Difference"].mean())

# Visualisation
sns.set_theme(color_codes=True)
sns.regplot(x="Difference", y="Predicted Value", data=pred_df);


# --- MODEL 2 END ---