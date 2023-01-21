import pickle
from unittest import result
from urllib import request
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pandas as pd
import csv


def predict_jobrole(lst):

    data1 = pd.read_csv("SSC .csv")

    with open('model_pkl', 'rb') as f:
        lr = pickle.load(f)
    prediction = lr.predict(lst)

    print(lst)

    set_no = prediction[0]
    print(set_no)
    df_new = data1[data1['Set No'] == f'{set_no}']
    print(df_new)
    string_roles = df_new.iloc[0][1]
    list_roles = string_roles.split(',')

    return list_roles



