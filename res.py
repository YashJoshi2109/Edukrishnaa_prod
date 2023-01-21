
# import pickle
# from unittest import result
# from urllib import request
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
# import pandas as pd
# import csv
# from unittest import result
# from flask import Flask, render_template, request, redirect, url_for
# app = Flask(__name__)

# data1=pd.read_csv("SSC .csv")


# # data = [[int(Linguistic),int(Musical),int(Bodily),int(Logical_Mathematical),int(Spatial_Visualization),int(Interpersonal),int(Intrapersonal),int(Naturalist)]]
# data=[[14,13,16,13,8,18,19,19]] # set 31
#     # data=[[16,7,6,18,5,17,6,8]] set31
#     # data=[[14,13,16,18,8,18,6,10]] set16
#     # data=[[14,13,16,13,8,18,19,19]] set16

# with open('model_pkl', 'rb') as f:
#     lr = pickle.load(f)
# prediction = lr.predict(data)

# set_no = prediction[0]
# print(set_no)
# df_new = data1[data1['Set No'] == f'{set_no}']
# print(df_new)
# string_roles=df_new.iloc[0][1]

# list_roles=string_roles.split(',')




# # @app.route('/ind' ,methods=['GET', 'POST'])
# # def index():
# #     result=request.form.get("result4")
# #     return render_template("\tenth\test2page.html")


# data2= result
# print(data2)


