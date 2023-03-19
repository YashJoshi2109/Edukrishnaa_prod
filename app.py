import csv
import re
from sqlalchemy import func
from glob import glob
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
from Te_jobresult import predict_jobrole_Te
from BE_jobresult import predict_jobrole_BE
from cryptography.fernet import Fernet
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session, flash
from traceback import print_tb
from sys import dont_write_bytecode
import sqlite3
import re
import os
import smtplib
import json
import random
from doctest import OutputChecker
from distutils.command.upload import upload
from datetime import date
# import easygui
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from getUserData import *

# from jobresults import list_roles   #importing job roles from jobresults
# from swayam import co_org, co_prof, co_tit, co_url

# imports for results

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smatevvb:r1jWlvwdryGUmyJ2tXViUAb3PlzYnUz7@satao.db.elephantsql.com/smatevvb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

app.secret_key = "hello"

CLIENT_ID = '411974903638-tuco5kc4h5pql62sshrjs7bqoaimn61k.apps.googleusercontent.com'
# Read from a file or environmental variable in a real app
CLIENT_SECRET = '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'
SCOPE = 'https://www.googleapis.com/auth/drive.metadata.readonly'
REDIRECT_URI = 'https://edukrishnaa-production.up.railway.app/'
getRoles = ""

# uname = db.Column(db.String(500))
# uname = db.Column(db.String(500))

# creating a model in user class


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(500))
    lname = db.Column(db.String(500))
    email = db.Column(db.String(500), unique=True)
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(500))
    state = db.Column(db.String(500))
    city = db.Column(db.String(500))
    uname = db.Column(db.String(500))
    password = db.Column(db.String(500))
    re_password = db.Column(db.String(500))
    gender = db.Column(db.String(500))
    quali = db.Column(db.String(500))
    fam_income = db.Column(db.String(500))
    roles = db.Column(db.String(500))
    img = db.Column(db.String(100))
    address = db.Column(db.String(255))
    clg_name = db.Column(db.String(255))
    graduation_year = db.Column(db.Date)
    course = db.Column(db.String(255))
    certificate = db.Column(db.String(255))
    otp = db.Column(db.String(100))

    # valdate =datetime.strptime('1776-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")

# creating a personality ques


class PersonalityQues(db.Model):
    ques_id = db.Column(db.Integer, primary_key=True)
    p_questions = db.Column(db.String(10000))
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    option4 = db.Column(db.String(100))
    domain = db.Column(db.String(100), unique=True)


class Roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(500))
    quote = db.Column(db.String(500))
    explore = db.Column(db.String(3000))
    image = db.Column(db.String(200))


class Results(db.Model):
    res_user_id = db.Column(db.Integer, primary_key=True)
    top_domain = db.Column(db.String(1100))
    small_desc = db.Column(db.String(600))
    opt_roles = db.Column(db.String(1100))


class Recruiter(db.Model):
    req_id = db.Column(db.Integer, primary_key=True)
    co_logo = db.Column(db.String(255))
    co_photo_id = db.Column(db.String(255))
    emp_id = db.Column(db.Integer)
    emp_name = db.Column(db.String(255))
    co_name = db.Column(db.String(255))
    co_email = db.Column(db.String(255))
    co_add1 = db.Column(db.String(255))
    co_city = db.Column(db.String(255))
    co_state = db.Column(db.String(255))
    co_req_designation = db.Column(db.String(255))
    phone = db.Column(db.Integer)
    recruite_password = db.Column(db.String(255))
    industry = db.Column(db.String(255))
    re_password = db.Column(db.String(255))
    role = db.Column(db.String(255))

# creating a techical ques


# class Technical(db.Model):
#     year = db.Column(db.Integer, primary_key=True)
#     t_question = db.Column(db.String(10000))
#     ques_id = db.Column(db.String(100))
#     domain = db.Column(db.String(100))
#     option1 = db.Column(db.String(100))
#     option2 = db.Column(db.String(100))
#     option3 = db.Column(db.String(100))
#     option4 = db.Column(db.String(100))
#     correct_opt = db.Column(db.String(100))

# creating a user_details


# class UserDetails(db.Model):
#     userid = db.Column(db.String(500), primary_key=True)
#     username = db.Column(db.String(500))
#     password = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     age = db.Column(db.Integer)
#     phone_number = db.Column(db.Integer)
#     location = db.Column(db.String)
#     Name = db.Column(db.String(10000))

class JobPost(db.Model):
    jobid = db.Column(db.String(500), primary_key=True)
    co_name = db.Column(db.String(500))
    designation = db.Column(db.String(100))
    job_type = db.Column(db.String(100))
    department = db.Column(db.String(100))
    job_desc1 = db.Column(db.String(500))
    req_skills = db.Column(db.String(100))
    location = db.Column(db.String(100))
    job_link = db.Column(db.String(100))
    job_desc2 = db.Column(db.String(3000))


class Feedback(db.Model):
    f_id = db.Column(db.Integer, primary_key=True)
    f_userid = db.Column(db.String(20))
    f_profile_photo = db.Column(db.String(40))
    f_first_name = db.Column(db.String(40))
    f_last_name = db.Column(db.String(40))
    feedback = db.Column(db.String(3000))
    f_date = db.Column(db.String(100))
    f_time = db.Column(db.String(100))
    f_type = db.Column(db.String(50))


with app.app_context():
    db.create_all()

    db.session.commit()

    print("posgresql users")


@ app.route('/sample', methods=['POST'])
def mlkmd1():
    log1 = request.form['lin11']
    log2 = request.form['lin13']

    return (log1+log2)


@ app.route('/my2home', methods=['GET', 'POST'])
def star1t():
    return render_template("speech.html")


@ app.route('/daynight', methods=['GET', 'POST'])
def daynight():
    return render_template("/log_reg_pro/daynight.html")


@ app.route('/wishes', methods=['GET', 'POST'])
def wishes():
    return render_template("wishes.html")


@ app.route('/start', methods=['GET', 'POST'])
def start():
    return render_template("/startup/startup2.html")


@ app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    return render_template("chatbot.html")


# recruiter routes

@ app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    user = session['recruiter']
    # user1 = session['user']
    getinfo = User.query.first()
    rec_user_data = User.query.all()
    recruiter = Recruiter.query.filter_by(co_email=user).first()
    return render_template("/recruiters/homepage.html", all_user=rec_user_data, data=getinfo, recruiter=recruiter)


@ app.route('/recruiter', methods=['GET', 'POST'])
def recruiter():
    user = session['recruiter']
    getinfo = User.query.first()
    rec_user_data = User.query.all()
    recruiter = Recruiter.query.filter_by(co_email=user).first()
    return render_template("/recruiters/recruiter.html", all_user=rec_user_data, data=getinfo, recruiter=recruiter)


@ app.route('/recruiter/user/<userid>', methods=['GET', 'POST'])
def recruiter_user_page(userid):
    # username1 = session['user']
    user = session['recruiter']
    getinfo = User.query.all()
    getuserid = User.query.filter_by(id=userid).first()
    recruiter = Recruiter.query.filter_by(co_email=user).first()
    getPersonalList, getRoles = getResultData(userid)

    return render_template("/recruiters/rec_user_disp.html", showuser=getuserid, data=getinfo, showresult=getPersonalList, ouputRoles=getRoles, recruiter=recruiter)

# LOGIN route


@ app.route('/login', methods=['GET', 'POST'])
def login():

    if "user1" in session:
        print("user1")
        getVerifyUser = session['user1']
        print("before if verfy")
        if User.query.filter_by(uname=getVerifyUser).first() != None:
            print("after if verify")
            get_verify_details = User.query.filter_by(
                uname=getVerifyUser).first()
            print("before delete")
            temp = get_verify_details.password
            print("temp check", temp)
            # temp2 = get_verify_details.password
            if temp == None:
                print("checking delete")
                db.session.delete(get_verify_details)
                db.session.commit()
                session.pop("user1", None)

    if request.method == "POST":
        user = request.form["email"]
        password = request.form["pass"]
        # randomNumber = random.randint(1000, 9999)
        # print(randomNumber)

        if User.query.filter_by(uname=user).first():
            username = User.query.filter_by(uname=user).first()
            # print("This is username from database ***************************************", username.uname)
            if user == username.uname and password == username.password:
                session["user"] = user
                return redirect(url_for("myhome"))
        else:
            flash("Invalid Username or Password")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            return redirect(url_for("user_profile"))
    return render_template("/log_reg_pro/login.html")


@ app.route('/admin', methods=['POST'])
def admin():
    if request.method == "POST":
        user = request.form["rec_email"]
        password = request.form["rec_pass"]
        # admin = request.form["admin"]
        if Recruiter.query.filter_by(co_email=user).first():
            username = Recruiter.query.filter_by(co_email=user).first()
            # print("This is username from database ***************************************", username.uname)
            if user == username.co_email and password == username.recruite_password:
                session["recruiter"] = user
                return redirect(url_for("homepage"))
        else:
            flash("Invalid Username or Password")
            return redirect(url_for("login"))

            # else:

        #     easygui.msgbox(
        #         "YOU HAVE ENTER WRONG USERNAME OR PASSWORD!", title="LOGIN ERROR")

    else:
        if "user" in session:
            return redirect(url_for("user_profile"))

    return render_template("/log_reg_pro/login.html")

    # if request.method == "POST":
    #     recruiter = request.form["pass"]
    #     rec = request.form["rec"]

    #     username = User.query.filter_by(uname=rec).first()
    #     # print("This is username from database ***************************************", username.uname)
    #     if rec == username.uname & recruiter == username.password:
    #         session["user"] = user
    #         return redirect(url_for("recruiter"))
    #     else:
    #         return ("WARNING username wrong bro")
    # else:
    #     if "user" in session:
    #         return redirect(url_for("user_profile"))


@ app.route('/user')
def user():
    if "user" in session:
        user = session['user']
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))


@ app.route('/googlesign')
def googlesign():
    return render_template("/log_reg_pro/googlesignup.html")


@ app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("recruiter", None)
    return redirect(url_for("login"))


@ app.route('/oauth2callback')
def oauth2callback():
    if 'code' not in request.args:
        auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                    '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
        return redirect(auth_uri)
    else:
        auth_code = Flask.request.args.get('code')
        data = {'code': auth_code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'}
        r = request.post('https://oauth2.googleapis.com/token', data=data)
        Flask.session['credentials'] = r.text
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("/log_reg_pro/registration.html")


@app.route('/recruiter_register', methods=['GET', 'POST'])
def recruiterregister():
    return render_template("/log_reg_pro/recruiter_registeration.html")


@app.route('/myhome', methods=['GET', 'POST'])
def myhome():
    get_feed = Feedback.query.all()
    getuse = ""
    # deleting the session from verify otp
    if "user1" in session:
        print("user1")
        getVerifyUser = session['user1']
        print("before if verfy")
        if User.query.filter_by(uname=getVerifyUser).first() != None:
            print("after if verify")
            get_verify_details = User.query.filter_by(
                uname=getVerifyUser).first()
            print("before delete")
            temp = get_verify_details.password
            print("temp check", temp)
            # temp2 = get_verify_details.password
            if temp == None:
                print("checking delete")
                db.session.delete(get_verify_details)
                db.session.commit()
                session.pop("user1", None)

    if "user" in session:
        getuser = session['user']
        getuse = User.query.filter_by(uname=getuser).first()

    # user = session['user']
    # username = User.query.filter_by(uname=user).first()
    # userhoon = username.uname
    # return redirect(url_for("myhome"))
    # username1 = session['user']
    # getinfo = User.query.filter_by(uname=username1).first()
    return render_template("index.html", get_feed=get_feed, getuse=getuse)

    # return redirect(url_for("myhome"), username.uname)


@ app.route('/404', methods=['GET', 'POST'])
def page404():
    return render_template("404page.html")


@ app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template("/log_reg_pro/aboutus.html")


@ app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    get_feed = Feedback.query.all()
    return render_template("/log_reg_pro/feedback.html", get_feed=get_feed)


@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()
    print("show image", getinfo.img)
    return render_template("/log_reg_pro/user_profile.html", getinfo=getinfo)


@ app.route('/jobopenings', methods=['GET', 'POST'])
def jobopenings():
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()
    recruiter = Recruiter.query.first()
    getJobInfo = JobPost.query.all()

    return render_template("/log_reg_pro/jobopening.html", getinfo=getinfo, post=getJobInfo, recruiter=recruiter)


@ app.route('/recruiter_profile', methods=['GET', 'POST'])
def recruiter_profile():
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()
    return render_template("/log_reg_pro/recruiter_profile.html", getinfo=getinfo)


@ app.route('/taketest', methods=['GET', 'POST'])
def take_test():
    if "user" in session:
        username1 = session['user']
        getinfo = User.query.filter_by(uname=username1).first()
        return render_template("take_test.html", getinfo=getinfo)
    else:
        return render_template("/log_reg_pro/login.html")


# 10th students routes
@ app.route('/taketest-10', methods=['GET', 'POST'])
def take_test_10():
    if "user" in session:
        username1 = session['user']
        getinfo = User.query.filter_by(uname=username1).first()
        return render_template("/tenth/take_test.html", getinfo=getinfo)
    else:
        return redirect(url_for("login"))


@ app.route('/test2-10', methods=['GET', 'POST'])
def test2_10():
    if "user" in session:
        user = session['user']
        addQues = PersonalityQues.query.all()
        getinfo = User.query.filter_by(uname=user).first()
        return render_template("/tenth/test2page.html", getinfo=getinfo)
    else:
        return redirect(url_for("login"))


# python dict


@ app.route('/test', methods=['POST', 'GET'])
def test():
    # numericalValues = ["Mostly Disagree" ,
    #                    "Slightly Disagree", "Slightly Agree", "Mostly Agree"]

    # personalities=['linguistic{}','musical{}','bodily{}','logical{}','spatial{}','interpersonal{}','intrapersonal{}','naturalistic{}']

    # if request.method == "POST":
    #     scoreList = []
    #     scoreChoco = 0
    #     score = 0
    #     form = request.form.get("form1")
    #     sum = 0

    #     for i in personalities:
    #         score=0
    #         for j in range(1,6):
    #             choco = request.form.get((i.format(j)))

    #     # for j in range(1, 6):
    #     #     choco = request.form.get("linguistic{}".format(j))
    #     #     print("choco ",choco)

    #             if choco in numericalValues:
    #                 score+=numericalValues.index(choco)+1

    #         print(score,"  ",i)
    #         scoreList.append(score)
    # print(scoreList)

    # roles = predict_jobrole([scoreList])
    # print(roles)
    return redirect(url_for('results_10'))


@app.route('/results_10', methods=['GET', 'POST'])
def results_10():
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()
    getRoles = Roles.query.all()

    scoreList = []
    numericalValues = ["Mostly Disagree",
                       "Slightly Disagree", "Slightly Agree", "Mostly Agree"]

    personalities = ['linguistic{}', 'musical{}', 'bodily{}', 'logical{}',
                     'spatial{}', 'interpersonal{}', 'intrapersonal{}', 'naturalistic{}']

    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

        for i in personalities:
            score = 0
            for j in range(1, 6):
                choco = request.form.get((i.format(j)))

        # for j in range(1, 6):
        #     choco = request.form.get("linguistic{}".format(j))
        #     print("choco ",choco)

                if choco in numericalValues:
                    score += numericalValues.index(choco)+1

            print(score, "  ", i)
            scoreList.append(score)
    print(scoreList)

    roles = predict_jobrole([scoreList])
    print(roles)
    new_list = [item.strip() for item in roles]

    my_dict = {"Linguistic": 0, "Musical": 0, "Bodily": 0, "Logical": 0,
               "Spatial": 0, "Interpersonal": 0, "Intrapersonal": 0, "Naturalist": 0}

    per_list = ["Linguistic", "Musical", "Bodily", "Logical",
                "Spatial", "Interpersonal", "Intrapersonal", "Naturalist"]

    final_dict = dict(zip(per_list, scoreList))
    print("printing filled dictionary : ", final_dict)

    perc_dict = {}
    for key, val in final_dict.items():
        perc_dict[key] = round(val/20 * 100, 2)

    sorted_dict = dict(
        sorted(perc_dict.items(), key=lambda x: x[1], reverse=True))

    my_list = list(sorted_dict.items())
    print("soreted list", my_list)

# Job description code starts here
    descRoles = []
    desccopy = []
    roles = [item.strip() for item in roles]
    for i in roles:
        print("printing roles plz", i)
        inI = str(i)
        print(type(i))
        print(i)
        # temp = Roles.query.filter_by(roles=inI).first()
        tempting = Roles.query.filter_by(roles=i).first()
        # tempting = Roles.query.order_by(inI).all()
        print("printing the temp variable", tempting)
        descRoles.append(tempting.image)
        desccopy.append(tempting.quote)
        img_dict = list(zip(roles, descRoles, desccopy))
        print("getting quotes", descRoles)

    # creating list
    personality_list = list(sorted_dict.keys())
    temp_score = list(sorted_dict.values())
    score_values = [str(x) for x in temp_score]
    storeResult(personality_list, score_values, roles, )

    return render_template("/tenth/resultpage.html", roles=new_list, mylist=my_list, getinfo=getinfo, descRoles=descRoles, img_dict=img_dict)


@app.route('/results_10/<roleid>', methods=['GET', 'POST'])
def role_page(roleid):
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()
    getRoles = Roles.query.filter_by(roles=roleid).first()
    # Scrap_Internshala("https://internshala.com", roleid, "mumbai")
    return render_template("/tenth/Astronomer_page.html", getRoles=getRoles, getinfo=getinfo)
    # return render_template("/tenth/Astronomer_page.html", getRoles=getRoles, com=int_company, tit=int_title, loc=int_loc, link=int_link, getinfo=getinfo)


# @app.route('/results_10/Dancer', methods=['GET', 'POST'])
# def dancer():
#     username1 = session['user']
#     # Scrap_Internshala("https://internshala.com", roleid, "mumbai")
#     return render_template("/tenth/Astronomer_page.html")


@ app.route('/add_feed', methods=['GET', 'POST'])
def add_feedback():
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()

    review_text = request.form['review_text']
    # Textual month, day and year
    today = date.today()
    current_date = today.strftime("%B %d, %Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    feed_type = "Regular User"

    adddata = Feedback(f_userid=getinfo.id, f_profile_photo=getinfo.img, f_first_name=getinfo.fname, f_last_name=getinfo.lname, feedback=review_text, f_date=current_date,
                       f_time=current_time, f_type=feed_type)

    db.session.add(adddata)

    db.session.commit()

    return redirect("/")


@ app.route('/add_recruiter_feed', methods=['GET', 'POST'])
def add_recruiter_feedback():
    username1 = session['recruiter']
    getinfo = Recruiter.query.filter_by(co_email=username1).first()

    review_text = request.form['review_text']
    # Textual month, day and year
    today = date.today()
    current_date = today.strftime("%B %d, %Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    feed_type = "Recruiter"

    adddata = Feedback(f_userid=getinfo.req_id, f_profile_photo=getinfo.co_photo_id, f_first_name=getinfo.emp_name, f_last_name=getinfo.co_name, feedback=review_text, f_date=current_date,
                       f_time=current_time, f_type=feed_type)

    db.session.add(adddata)

    db.session.commit()

    return redirect("/homepage")


@ app.route('/Astronomer_page', methods=['GET', 'POST'])
def Astronomer_page():
    return render_template("/tenth/Astronomer_page.html")


@ app.route('/Data_science')
def Music_Teacher_page():
    return render_template("/tenth/music_teacher.html",)


# 12th students routes
@ app.route('/taketest-12', methods=['GET', 'POST'])
def take_test_12():
    if "user" in session:
        username1 = session['user']
        getinfo = User.query.filter_by(uname=username1).first()
        return render_template("/twelve/take_test.html", getinfo=getinfo)
    else:
        return redirect(url_for("login"))


@ app.route('/test1-12', methods=['GET', 'POST'])
def test1_12():
    return render_template("/twelve/test1.html")


@ app.route('/test2-12', methods=['GET', 'POST'])
def test2_12():
    return render_template("/twelve/test2page.html")


@ app.route('/test3-12', methods=['GET', 'POST'])
def take3_12():
    return render_template("/twelve/test3page.html")


@ app.route('/results-12', methods=['GET', 'POST'])
def results_12():
    return render_template("/twelve/resultpage.html")


# UG PG students routes
@ app.route('/taketest-up', methods=['GET', 'POST'])
def take_test_up():
    if "user" in session:
        username1 = session['user']
        getinfo = User.query.filter_by(uname=username1).first()
        return render_template("/ug-pg/take_test.html", getinfo=getinfo)
    else:
        return redirect(url_for("login"))


@ app.route('/se', methods=['GET', 'POST'])
def test1_se():
    return render_template("/ug-pg/se/test1_se.html")


@ app.route('/test2-se', methods=['GET', 'POST'])
def test2_se():
    return render_template("/ug-pg/se/test2_se.html")


@ app.route('/test1-te', methods=['GET', 'POST'])
def test1_te():
    return render_template("/ug-pg/te/test1_te.html")


@ app.route('/te', methods=['GET', 'POST'])
def te():
    return render_template("/ug-pg/te/third_year.html")


@ app.route('/be', methods=['GET', 'POST'])
def be():
    return render_template("/ug-pg/be/Fourth.html")


@ app.route('/test2-te', methods=['GET', 'POST'])
def test2_te():
    return render_template("/ug-pg/te/test2_te.html")


@ app.route('/results_be', methods=['GET', 'POST'])
def results_up():
    # session detiails
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()

    scoreList = []
    numericalValues = ["Mostly Disagree",
                       "Slightly Disagree", "Slightly Agree", "Mostly Agree"]

    personalities = ['logical{}', 'spatial{}',
                     'interpersonal{}', 'intrapersonal{}']

    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

        for i in personalities:
            score = 0
            for j in range(1, 6):
                choco = request.form.get((i.format(j)))

                if choco in numericalValues:
                    score += numericalValues.index(choco)+1

            print(score, "  ", i)
            scoreList.append(score)
            perScore = scoreList

    ans = [0, 1]
    mcqId = ['web{}', 'aiml{}', 'iot{}', 'nim{}', 'sec{}', 'pm{}']
    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

        for i in mcqId:
            score = 0
            for j in range(1, 7):
                getAns = request.form.get((i.format(j)))
                # print(type(getAns))
                print(j, i, " get ans ", getAns)
                temp = int(getAns)
                if temp in ans:
                    score += ans.index(temp)+1
                    tempScore = score-6

            print(tempScore, "  ", i)
            scoreList.append(tempScore)
            # scoreList.append(mcqList)

    print("this is MCQ test  ", scoreList)
    roles = predict_jobrole_BE([scoreList])
    print(roles)
    roles = [item.strip() for item in roles]

    # Sorting of personality scores
    per_list = ["Logical", "Spatial", "Interpersonal", "Intrapersonal"]

    final_dict = dict(zip(per_list, perScore))
    print("printing filled dictionary : ", final_dict)

    perc_dict = {}
    for key, val in final_dict.items():
        perc_dict[key] = round(val/20 * 100, 2)

    sorted_dict = dict(
        sorted(perc_dict.items(), key=lambda x: x[1], reverse=True))

    # Storing in the database
    my_list = list(sorted_dict.items())
    print("soreted list", my_list)
    personality_list = list(sorted_dict.keys())
    score_values = list(sorted_dict.values())
    score_values = [str(x) for x in score_values]
    storeResult(personality_list, score_values, roles)

    # Job description and image code starts here
    descRoles = []
    desccopy = []
    roles = [item.strip() for item in roles]
    for i in roles:
        print("printing roles plz", i)
        inI = str(i)
        print(type(i))
        print(i)
        # temp = Roles.query.filter_by(roles=inI).first()
        tempting = Roles.query.filter_by(roles=i).first()
        # tempting = Roles.query.order_by(inI).all()
        print("printing the temp variable", tempting)
        descRoles.append(tempting.image)
        desccopy.append(tempting.quote)
        img_dict = list(zip(roles, descRoles, desccopy))
        print("getting quotes", descRoles)

    # creating list to add into db
    personality_list = list(sorted_dict.keys())
    temp_score = list(sorted_dict.values())
    score_values = [str(x) for x in temp_score]
    storeResult(personality_list, score_values, roles, )

    return render_template("/ug-pg/be/result_be.html",  roles=roles, mylist=my_list, getinfo=getinfo, img_dict=img_dict)


@ app.route('/results-se', methods=['GET', 'POST'])
def results_se():
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()

    scoreList = []
    numericalValues = ["Mostly Disagree",
                       "Slightly Disagree", "Slightly Agree", "Mostly Agree"]

    personalities = ['logical{}', 'spatial{}',
                     'interpersonal{}', 'intrapersonal{}', 'linguistic{}', 'musical{}', 'bodily{}', 'naturalistic{}']

    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

        for i in personalities:
            score = 0
            for j in range(1, 6):
                choco = request.form.get((i.format(j)))

                if choco in numericalValues:
                    score += numericalValues.index(choco)+1

            print(score, "  ", i)
            scoreList.append(score)
            perScore = scoreList
    mcqList = []
    ans = [0, 1]
    mcqId = ['CP{}', 'DM{}', 'CH{}']
    store_dict = {}
    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

        for i in mcqId:
            score = 0
            for j in range(1, 7):
                getAns = request.form.get((i.format(j)))
                # print(type(getAns))
                print(j, i, " get ans ", getAns)
                temp = int(getAns)
                if temp in ans:
                    score += ans.index(temp)+1
                    tempScore = score-6
            if i == 'CH{}':
                temp_char = "Computer Hardware"
            elif i == 'CP{}':
                temp_char = "C"
            elif i == 'DM{}':
                temp_char = "Data mining and storage"

            store_dict[temp_char] = tempScore
            print(tempScore, "  ", i)
            print("MY dictionary - ", store_dict)
            scoreList.append(tempScore)
            # scoreList.append(mcqList)

    print("this is MCQ test  ", scoreList)

    # Getting the key with maximum value
    Key_max = max(zip(store_dict.values(), store_dict.keys()))[1]
    print("Key max value", Key_max)

    key_value = store_dict[Key_max]
    if key_value <= 3:
        Key_max = "other"

    data1 = pd.read_csv("SE.csv")
    df_new = data1[data1['domain'] == f'{Key_max}']
    print(df_new)
    sub_domain = df_new.iloc[0][1]
    se_roles = df_new.iloc[0][2]
    print("sub domain", sub_domain)
    print("se roles", se_roles)
    se_roles = list(se_roles.split(","))
    roles = se_roles
    # Job description and image code starts here
    descRoles = []
    desccopy = []
    for i in se_roles:
        print("printing roles plz", i)
        inI = str(i)
        print(type(i))
        print(i)
        # temp = Roles.query.filter_by(roles=inI).first()
        tempting = Roles.query.filter_by(roles=i).first()
        # tempting = Roles.query.order_by(inI).all()
        print("printing the temp variable", tempting)
        descRoles.append(tempting.image)
        desccopy.append(tempting.quote)
        img_dict = list(zip(se_roles, descRoles, desccopy))
        print("getting quotes", descRoles)

    # converting to percentage personality
    per_list = ["Linguistic", "Musical", "Bodily", "Logical",
                "Spatial", "Interpersonal", "Intrapersonal", "Naturalist"]

    final_dict = dict(zip(per_list, scoreList))
    print("printing filled dictionary : ", final_dict)

    perc_dict = {}
    for key, val in final_dict.items():
        perc_dict[key] = round(val/20 * 100, 2)

    sorted_dict = dict(
        sorted(perc_dict.items(), key=lambda x: x[1], reverse=True))

    # creating list
    personality_list = list(sorted_dict.keys())
    temp_score = list(sorted_dict.values())
    score_values = [str(x) for x in temp_score]
    storeResult(personality_list, score_values, se_roles, )

    my_list = list(sorted_dict.items())
    print("soreted list", my_list)

    # # Storing in the database
    # my_list = list(sorted_dict.items())
    # print("soreted list", my_list)
    # personality_list = list(sorted_dict.keys())
    # score_values = list(sorted_dict.values())
    # score_values = [str(x) for x in score_values]
    # storeResult(personality_list, score_values, roles)

    return render_template("/ug-pg/se/result_se.html", mylist=my_list, sub=sub_domain, img_dict=img_dict, getinfo=getinfo)


@ app.route('/results-te', methods=['GET', 'POST'])
def results_te():
    # return render_template("/ug-pg/te/testing.py")
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()

    scoreList = []
    numericalValues = ["Mostly Disagree",
                       "Slightly Disagree", "Slightly Agree", "Mostly Agree"]

    personalities = ['logical{}', 'spatial{}',
                     'interpersonal{}', 'intrapersonal{}']

    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

        for i in personalities:
            score = 0
            for j in range(1, 6):
                choco = request.form.get((i.format(j)))

                if choco in numericalValues:
                    score += numericalValues.index(choco)+1

            print(score, "  ", i)
            scoreList.append(score)
            perScore = scoreList
    mcqList = []
    ans = [0, 1]
    mcqId = ['NIM{}', 'web{}', 'AI{}']
    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

        for i in mcqId:
            score = 0
            for j in range(1, 7):
                getAns = request.form.get((i.format(j)))
                # print(type(getAns))
                print(j, i, " get ans ", getAns)
                temp = int(getAns)
                if temp in ans:
                    score += ans.index(temp)+1
                    tempScore = score-6

            print(tempScore, "  ", i)
            scoreList.append(tempScore)
            # scoreList.append(mcqList)

    print("this is MCQ test  ", scoreList)
    roles = predict_jobrole_Te([scoreList])
    print(roles)
    roles = [item.strip() for item in roles]

    # roles1 = roles.pop(0)

    my_dict = {"Logical": 0, "Spatial": 0,
               "Interpersonal": 0, "Intrapersonal": 0}

    per_list = ["Logical", "Spatial", "Interpersonal", "Intrapersonal"]

    final_dict = dict(zip(per_list, perScore))
    print("printing filled dictionary : ", final_dict)

    perc_dict = {}
    for key, val in final_dict.items():
        perc_dict[key] = round(val/20 * 100, 2)

    sorted_dict = dict(
        sorted(perc_dict.items(), key=lambda x: x[1], reverse=True))

    # Storing in the database
    my_list = list(sorted_dict.items())
    print("soreted list", my_list)
    personality_list = list(sorted_dict.keys())
    score_values = list(sorted_dict.values())
    score_values = [str(x) for x in score_values]
    storeResult(personality_list, score_values, roles)

    # Job description and image code starts here
    descRoles = []
    desccopy = []
    roles = [item.strip() for item in roles]
    for i in roles:
        print("printing roles plz", i)
        inI = str(i)
        print(type(i))
        print(i)
        # temp = Roles.query.filter_by(roles=inI).first()
        tempting = Roles.query.filter_by(roles=i).first()
        # tempting = Roles.query.order_by(inI).all()
        print("printing the temp variable", tempting)
        descRoles.append(tempting.image)
        desccopy.append(tempting.quote)
        img_dict = list(zip(roles, descRoles, desccopy))
        print("getting quotes", descRoles)

    # creating list to add into db
    personality_list = list(sorted_dict.keys())
    temp_score = list(sorted_dict.values())
    score_values = [str(x) for x in temp_score]
    storeResult(personality_list, score_values, roles, )

    return render_template("/ug-pg/te/result_te.html", roles=roles, mylist=my_list, getinfo=getinfo, img_dict=img_dict)


@app.route('/results_te/<roleid>', methods=['GET', 'POST'])
def role_page1(roleid):
    username1 = session['user']
    getinfo = User.query.filter_by(uname=username1).first()
    getRoles = Roles.query.filter_by(roles=roleid).first()
    # Scrap_Internshala("https://internshala.com", roleid, "mumbai")
    return render_template("/tenth/Astronomer_page.html", getRoles=getRoles, getinfo=getinfo)


@ app.route('/data-science-up', methods=['GET', 'POST'])
def science_up():
    return render_template("/ug-pg/be/data_science.html", com=int_company, tit=int_title, loc=int_loc, link=int_link)
    # co_org= co_org, co_prof=co_prof, co_tit=co_tit, co_url=co_url

# pop up / out section


@ app.route('/popup', methods=['GET', 'POST'])
def popup():
    return render_template("/ug-pg/popup.html")


@ app.route('/popup1', methods=['GET', 'POST'])
def popup1():
    return render_template("/ug-pg/endpopup.html")

# for 10th tenth students


@ app.route('/popup-10', methods=['GET', 'POST'])
def popup10():
    return render_template("/tenth/popup.html")


@ app.route('/popout-10', methods=['GET', 'POST'])
def popout10():
    return render_template("/tenth/endpopup.html")

# for se students


@ app.route('/popup-se', methods=['GET', 'POST'])
def popupse():
    return render_template("/ug-pg/se/popup.html")


@ app.route('/popout-se', methods=['GET', 'POST'])
def popoutse():
    return render_template("/ug-pg/se/endpopup.html")


@ app.route('/results', methods=['GET', 'POST'])
def resultpage():
    return render_template("/ug-pg/resultpage.html")  # look afterwards


@ app.route('/data-analyst', methods=['GET', 'POST'])
def recommend1():
    return render_template("/ug-pg/be/Data_analyst.html")


@ app.route('/')
def home():
    get_feed = Feedback.query.all()
    # deleting the session from verify otp
    getuse = ""
    if "user1" in session:
        print("user1")
        getVerifyUser = session['user1']
        print("before if verfy")
        if User.query.filter_by(uname=getVerifyUser).first() != None:
            print("after if verify")
            get_verify_details = User.query.filter_by(
                uname=getVerifyUser).first()
            print("before delete")
            temp = get_verify_details.password
            print("temp check", temp)
            # temp2 = get_verify_details.password
            if temp == None:
                print("checking delete")
                db.session.delete(get_verify_details)
                db.session.commit()
                session.pop("user1", None)

    if "user" in session:
        getuser = session['user']
        getuse = User.query.filter_by(uname=getuser).first()

    return render_template("index.html", get_feed=get_feed, getuse=getuse)


@ app.route('/resume_1')
def resume():
    getUsername = session['user']
    getinfo = User.query.filter_by(uname=getUsername).first()
    # result = Roles.query.filter_by(role_id=id).first()

    return render_template("/log_reg_pro/resume_1.html", getinfo=getinfo)


# @app.route('/add1', methods=['POST'])
# def addpost1():

#     check = request.form['check']


#     check = reqest.form['check']

# @app.route('/add', methods=['POST'])
# def addpost():
#     check = request.form['check']
#     return ("done")


@ app.route('/womenstartup')
def womenstartup():
    return render_template("women.html")

# @app.route('/adding',methods=['GET','POST'])
# def add():
#     fname = request.form['firstname']
#     return ("fname")


# @app.route('/test', methods=['POST'])
# def test():
#     output = request.get_json()
#     print(output)  # This is the output that was stored in the JSON within the browser
#     print(type(output))
#     # this converts the json output to a python dictionary
#     result = json.loads(output)
#     print(result)  # Printing the new dictionary
#     print(type(result))  # this shows the json converted as a python dictionary
#     return result

# app.config['PROFILE_IMAGE'] = "static\\assets\img"
# app.config['FILE_STORE'] = "static\\assets\certificate"


@ app.route('/update', methods=['GET', 'POST'])
def updatepost():
    # upload_image = request.files['file']
    # if upload_image.filename != '':
    #     user = session['user']
    #     filepath = os.path.join(
    #         app.config['PROFILE_IMAGE'], upload_image.filename)
    #     upload_image.save(filepath)
    #     con = sqlite3.connect("db.sqlite3")
    #     cur = con.cursor()
    #     admin = User.query.filter_by(uname=user).first()
    #     admin.img = upload_image.filename
    # cur.execute(
    #     "UPDATE User SET img='upload_image.filename' WHERE uname = ")
    # cur.execute("INSERT INTO User(img)VALUES(?)", (upload_image.filename,))
    # db.session.commit()
    # con.commit()
    # print("Image File Uploaded Successfully")
    # adddata = User(img=upload_image.filename)

    # e_name = name.encode()
    email = request.form['update_email']
    if email != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        admin.email = email
        db.session.commit()
        print("Updated Email Uploaded Successfully")

    # e_lname = lname.encode()
    address = request.form['update_address']
    if address != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        admin.address = address
        db.session.commit()
        print("Address Uploaded Successfully")
    # e_email = email.encode()
    city = request.form['update_city']
    if city != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        admin.city = city
        db.session.commit()
        print("City update Uploaded Successfully")
    # e_age = age.encode()
    state = request.form['update_state']
    if state != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        admin.state = state
        db.session.commit()
        print("Updated state Uploaded Successfully")
    # e_phone = phone.encode()
    phone = request.form['update_phone']
    if phone != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        admin.phone = phone
        db.session.commit()
        print("Updated phone Uploaded Successfully")
    # e_uname = uname.encode()
    college_name = request.form['update_college_name']
    if college_name != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        admin.clg_name = college_name
        db.session.commit()
        print("Updated College Uploaded Successfully")

    # certificate = request.files['certificate']
    # if certificate.filename != '':
    #     user = session['user']
    #     filepath = os.path.join(
    #         app.config['FILE_STORE'], certificate.filename)
    #     upload_image.save(filepath)
    #     con = sqlite3.connect("db.sqlite3")
    #     cur = con.cursor()
    #     admin = User.query.filter_by(uname=user).first()
    #     admin.certificate = certificate.filename
    #     db.session.commit()
    #     print("Certificate File Uploaded Successfully")

    graduation_year = request.form['graduation_year']
    if graduation_year != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        date_time_str = datetime.strptime(str(graduation_year), "%Y-%m-%d")
        admin.graduation_year = date_time_str
        db.session.commit()
        print("Updated graduation_year Uploaded Successfully")

    course = request.form['course']
    if course != '':
        user = session['user']
        admin = User.query.filter_by(uname=user).first()
        admin.course = course
        db.session.commit()
        print("Updated course Uploaded Successfully")

    print("************************UPDATED INFORMATION********",  email,
          city, state, address, phone, college_name, graduation_year, course)

    return redirect(url_for("user_profile"))


app.config['RECRUITER'] = "static\\assets\certificate"
app.config['COMPANY_LOGO'] = "static\\assets\company_logo"


@ app.route('/recruite', methods=['GET', 'POST'])
def recruite():
    # emp_photo = request.files['emp_photo']
    # if emp_photo.filename != '':
    #     global co_photo_id
    #     filepath = os.path.join(
    #         app.config['RECRUITER'], emp_photo.filename)
    #     emp_photo.save(filepath)
    #     co_photo_id = emp_photo.filename

    # cur.execute(
    #     "UPDATE User SET img='upload_image.filename' WHERE uname = ")
    # cur.execute("INSERT INTO User(img)VALUES(?)", (upload_image.filename,))
    # con.commit()
    # print("recruiter image File Uploaded Successfully")
    # adddata = User(img=upload_image.filename)

    # e_name = name.encode()
    email = request.form['co_email']

    # e_lname = lname.encode()
    address = request.form['co_add1']

    emp_name = request.form['emp_name']

    # e_email = email.encode()
    city = request.form['co_city']

    # e_age = age.encode()
    state = request.form['co_state']

    # e_phone = phone.encode()
    # phone = request.form['phone']

    # e_uname = uname.encode()
    company_name = request.form['co_name']

    # certificate = request.files['co_logo']
    # if certificate.filename != '':
    #     global co_logo
    #     filepath = os.path.join(
    #         app.config['RECRUITER'], certificate.filename)
    #     certificate.save(filepath)
    #     co_logo = certificate.filename
    #     print("co_logo File Uploaded Successfully")

    password = request.form['password1']

    co_req_designation = request.form['co_req_designation']

    course = request.form['industry']

    repass = request.form['password2']
    emp_id = request.form['emp_id']
    role = "Admin"

    # check email already exists
    if Recruiter.query.filter_by(co_email=email).first() == None:
        pass
    else:
        temp_email = Recruiter.query.filter_by(co_email=email).first()
        if email == temp_email.co_email:
            flash("Email already exsists.")
            return render_template("/log_reg_pro/recruiter_registeration.html")

    if password == repass:
        flag = 0
        while True:
            if (len(password) < 7):
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[_@$&#]", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                flag = 0
                flash("Valid Password")
                break

        if flag == -1:
            flash("*Please enter a valid password or password does not match!")
            return render_template("/log_reg_pro/recruiter_registeration.html")
    else:
        flash("Password does not match.")
        return render_template("/log_reg_pro/recruiter_registeration.html")

    # print("************************UPDATED INFORMATION********",  email,
    #       city, state, address, phone, college_name, course)

    adddata = Recruiter(co_photo_id=None, re_password=repass, co_email=email, industry=course, co_state=state, emp_name=emp_name, emp_id=emp_id,
                        phone=None, co_city=city, recruite_password=password, co_logo=None, co_add1=address, co_name=company_name, co_req_designation=co_req_designation, role=role)

    db.session.add(adddata)

    db.session.commit()

    return redirect(url_for("login"))


@ app.route('/add', methods=['POST'])
def addpost():
    name = request.form['name']
    # e_name = name.encode()
    lname = request.form['lastname']
    # e_lname = lname.encode()
    email = request.form['email']
    # e_email = email.encode()
    dob = request.form['dob']
    # e_age = age.encode()
    phone = request.form['phone']

    state = request.form['state']
    # e_phone = phone.encode()
    city = request.form['city']
    # e_city = city.encode()
    uname = request.form['uname']
    # e_uname = uname.encode()
    # password1 = request.form['password1']
    # password2 = request.form['password2']
    # pass1 = password1.encode()
    gender = request.form['gender']
    account = request.form['account']
    income = request.form['income']
    # roles = request.form['roles']

    if User.query.filter_by(email=email).first() == None:
        pass
    else:
        temp_email = User.query.filter_by(email=email).first()

        if email == temp_email.email:
            flash("Email already exsists.")
            # return redirect(url_for("/"))
            return render_template("/log_reg_pro/registration.html")

    # key = Fernet.generate_key()  # Storeeee thissss key or get if you already have it
    # f = Fernet(key)
    date_time_str = datetime.strptime(str(dob), "%Y-%m-%d")
    if gender == 'Male':
        profile = 'male_preview.jpg'

    elif gender == 'Female':
        profile = 'female_preview.jpg'

    today = date.today()
    age = today.year - date_time_str.year - \
        ((today.month, today.day) < (date_time_str.month, date_time_str.day))

    print("************************REGISTRATION INFO********",  state,
          city, uname, dob, date_time_str, age, gender, account, income)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    otp = str(random.randint(1000, 9999))
    print(otp, type(otp))

    finalotp = "To register yourself in Edukrishna, Please find the below OTP and complete the verification. YOUR OTP IS " + \
        otp+". Do not share this OTP with anyone - Team Edukrishnaa"
# randomnew = "OTP ", randomNumber

    server.starttls()
    server.login('edukrishnaa45@gmail.com', 'aqortlzicgoozauq')
    server.sendmail('yashjosh7486@gmail.com', email,
                    finalotp)
    print("*********Mail sent !*********")

    adddata = User(fname=name, lname=lname, email=email, dob=date_time_str, age=age,
                   phone=phone, state=state, city=city, uname=uname, gender=gender, quali=account, fam_income=income, roles="User",
                   address=None, clg_name=None, graduation_year=None, course=None, certificate=None, otp=otp, img=profile)

    db.session.add(adddata)

    db.session.commit()

    session["user1"] = uname

    return render_template("/log_reg_pro/OtpVerify.html")


@ app.route('/verifyotp', methods=['POST'])
def verifyotp():
    checkotp = request.form['verify']
    pass1 = request.form['password1']
    pass2 = request.form['password2']
    flag = 0
    username1 = session['user1']
    getinfo = User.query.filter_by(uname=username1).first()

    while True:
        if (len(pass1) < 7):
            flag = -1
            break
        elif not re.search("[a-z]", pass1):
            flag = -1
            break
        elif not re.search("[A-Z]", pass1):
            flag = -1
            break
        elif not re.search("[0-9]", pass1):
            flag = -1
            break
        elif not re.search("[_@$&#]", pass1):
            flag = -1
            break
        elif re.search("\s", pass1):
            flag = -1
            break
        else:
            flag = 0
            flash("Valid Password")
            break

    if flag == -1:
        flash("Please enter a valid password or password does not match!")
        return render_template("/log_reg_pro/OtpVerify.html")

    if pass1 == pass2:
        if checkotp == getinfo.otp and pass1 == pass2:
            getinfo.password = pass1
            getinfo.re_password = pass2
            db.session.commit()
            session.pop('user1', None)
            return redirect(url_for("login"))
        else:
            db.session.delete(getinfo)
            # commit (or flush)
            db.session.commit()
            session.pop('user1', None)
            return redirect(url_for("register"))
    else:
        flash("Password Do Not Match! Try Again")
        return render_template("/log_reg_pro/OtpVerify.html")


# Calcuating Age with help of DOB
# born = User.dob
# # Printing date to just check in cmd
# print("Born :", born)
# # Identify given date as date month and year
# born = datetime.strptime(User.dob, "%d/%m/%Y").date()
# # Get today's date
# today = date.today()
# # actual formula
# print("Age :",
#       today.year - born.year - ((today.month,
#                                  today.day) < (born.month,
#                                                born.day)))
# date_str = str(User.age)
# date_object = datetime.strptime(date_str, '%d-%m-%Y').date()
# print(type(date_object))
# print(date_object)  # printed in default formatting
# print("***********Username********")
# birthdate = date_object
# today = date.today()
# age = today.year - birthdate.year - \
#     ((today.month, today.day) < (birthdate.month, birthdate.day))
# print("His/Her age is :", age)


@app.route('/jobpost')
def jobpost():
    return render_template("/recruiters/jobpost.html")


@app.route('/addjobpost', methods=['POST'])
def addjobpost():
    jobid = request.form['jobid']
    co_name = request.form['co_name']
    designation = request.form['designation']
    job_type = request.form['job_type']
    department = request.form['department']
    job_description = request.form['job_description']
    req_skills = request.form['req_skills']
    location = request.form['location']
    job_link = request.form['job_link']

    # getRecData = getSessionDetailsRecruiterr

    addJobPost = JobPost(jobid=jobid, co_name=co_name, designation=designation, job_type=job_type, department=department,
                         job_desc1=job_description, req_skills=req_skills, location=location, job_link=job_link, job_desc2=None)

    db.session.add(addJobPost)
    db.session.commit()
    return redirect("/homepage")


# ekbaar run karke de le pranav ye wala
@app.route('/personality', methods=['GET', 'POST'])
def searchpersonlity():
    personality = request.args.get("personality")
    user = session['recruiter']
    results = Results.query.filter(
        Results.top_domain.startswith(personality)).all()  # yeh mast work ho raha hain
    get_ids = []
    for i in results:
        get_currentline = i;
        temp = re.findall(r'\d+', str(get_currentline))
        get_ids.append(int(temp[0]))
    print("this is only ids", get_ids)
    # output bhi aa raha hain
    # yeh kaise logic laagana hain bro ? # yeh page main transfer karege hum chalega onces recruiter clicks on that card fir dusra ek page bane ka jarut nahi.
    get_name =[]
    get_email=[]
    get_phone = []
    get_img = []
    for i in get_ids:
        i = str(i)
        print("print i ",i)
        if User.query.filter_by(id=i).first() != None:
            user_info = User.query.filter_by(id=i).first()  
            get_name.append(user_info.fname)
            get_email.append(user_info.email)
            get_phone.append(user_info.phone)
            get_img.append(user_info.img)
        else:
            pass


    all_data = list(zip(get_ids,get_name, get_email, get_phone, get_img))

    getinfo = User.query.all()
    rec_user_data = User.query.all()
    recruiter = Recruiter.query.filter_by(co_email=user).first()
    print(personality)
    return render_template("/recruiters/personality.html", all_user=all_data, data=getinfo, recruiter=recruiter, personality=personality)


# @ app.route('/add', methods=['POST'])
# def addpost():
#     name = request.form['name']
#     e_name = name.encode()
#     lname = request.form['lastname']
#     e_lname = lname.encode()
#     email = request.form['email']
#     e_email = email.encode()
#     age = request.form['age']
#     e_age = age.encode()
#     phone = request.form['phone']
#     e_phone = phone.encode()
#     city = request.form['city']
#     e_city = city.encode()
#     uname = request.form['uname']
#     e_uname = uname.encode()
#     password1 = request.form['password1']
#     pass1 = password1.encode()

#     key = Fernet.generate_key()  # Store this key or get if you already have it
#     f = Fernet(key)

#     p_name = f.encrypt(e_name)
#     p_email = f.encrypt(e_email)
#     p_age = f.encrypt(e_age)

#     print("NAME : - ")
#     print(p_name)
#     print("EMAIL : - ")
#     print(p_email)
#     print("AGE : - ")
#     print(p_age)

#     # adddata = User(fname=name,lname=lname, email=email, age=age,phone=phone,city=city, uname=uname, password=password1)

#     # db.session.add(adddata)
#     # db.session.commit()

#     return render_template('DONE!!')


# if __name__ == '__main__':
#     app.run(debug=True)

#     adddata = User(fname=name,lname=lname, email=email, age=age,phone=phone,city=city, uname=uname, password=password1)

#     db.session.add(adddata)
#     db.session.commit()

#     return ("zala re baba")

#     return ("DONE re")

@app.errorhandler(404)
def not_found():
    """Page not found Pleaseee contact us via Email."""
    return make_response(
        render_template("404page.html"),
        404
    )


@app.errorhandler(400)
def bad_request():
    """Bad request Please contacttt us via Email."""
    return make_response(
        render_template("404page.html"),
        400
    )


@app.errorhandler(500)
def server_error():
    """Internal server error Pleeeease contact us via Email."""
    return make_response(
        render_template("400page.html"),
        500
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
    # app.run(debug=True)
