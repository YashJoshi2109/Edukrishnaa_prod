import csv
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import pickle
from internscrap import int_company, int_link, int_loc, int_title
from internscrap import Scrap_Internshala
from sqlalchemy.orm import relationship
from datetime import datetime, date
from test import linguistic_calc
from jobresults import predict_jobrole
from cryptography.fernet import Fernet
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session
from traceback import print_tb
from sys import dont_write_bytecode
import sqlite3
import re
import os
import json
from doctest import OutputChecker
from distutils.command.upload import upload
from datetime import date
from app import *


def getSessionDetails():
    get_username = session['user']
    getuserinfo = User.query.filter_by(uname=get_username).first()
    return getuserinfo


def storeResult(personality_list, score_values, roles):
    # new_per_list = per_list
    # new_scoreList = scoreList
    # new_roles = roles

    getuserinfo = getSessionDetails()
    check_result = Results.query.filter_by(res_user_id=getuserinfo.id).first()
    if check_result != None:
        db.session.delete(check_result)
        db.session.commit()
        insert_record(personality_list, score_values, roles, getuserinfo)
    else:
        insert_record(personality_list, score_values, roles, getuserinfo)


def insert_record(personality_list, score_values, roles, getuserinfo):
    # creating empty strings
    personal_opt_list = ""
    get_roles = ""
    score_list = ""

    # adding , at the end of the elements
    db_per_list = list(map(lambda ls: ls+",", personality_list))
    db_roles = list(map(lambda ls: ls+",", roles))
    db_score_list = list(map(lambda ls: ls+",", score_values))
    
    # converting to string
    personal_opt_list = personal_opt_list.join(db_per_list)
    get_roles = get_roles.join(db_roles)
    score_list = score_list.join(db_score_list)

    current_userid = getuserinfo.id

    addResult = Results(res_user_id=current_userid, top_domain=personal_opt_list,
                        small_desc=score_list, opt_roles=get_roles)
    db.session.add(addResult)

    db.session.commit()


def getResultData(userid):
    getresult = Results.query.filter_by(res_user_id=userid).first()
    getPersonalList = getresult.top_domain.split(",")
    getRoles = getresult.opt_roles.split(",")
    return getPersonalList, getRoles
