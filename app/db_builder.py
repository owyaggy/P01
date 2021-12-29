import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session
import os
from api import *

DB_FILE = "discobandit.db"

def updateTheme(c,t):
    theme = dict(main=c, text =t)
    return theme
theme = updateTheme("info", "secondary")
def createTables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS userinfo (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    theme TEXT,
    weather INTEGER,
    news INTEGER,
    book INTEGER,
    stock INTEGER,
    facts INTEGER,
    space INTEGER,
    sports INTEGER,
    time INTEGER);"""
    )
    db.commit()
    db.close()

def register(request_user,request_password):
    error = "ERROR: "
    error += validate("userID", request_user)
    error += validate("password", request_password)
    if (error == "ERROR: "):
        #if userID is valid, store in database
        # session["userID"] = request_user
        insert(request_user, request_password)
        print("**** Sucessionfully registered")
        widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space', 'stocks', 'stocks', 'stocks', 'test']
        return render_template('response.html',user = request_user, wdigets = widgets, name = "Logged in", theme = theme)
            # ADD USERID TO THE DB HERE
    print("***** Registration failed")
    return render_template('register.html', error = error, theme = theme)
    # return render_template('response.html', user = session.get("userID"))

def authenticate(user,password): #looggin in
    response = "TRY AGAIN: "
    if password == "" or password == " " or password == None:
            response += " Username or password cannot be blank"
    if(check_existence('username', user) == False or check_existence('password', password) == False): #checks for password
        response += "incorrect username or password"
    #checks if user exists and password matches user
    if(response == "TRY AGAIN: "):
        # session['userID'] = user
        packages = { # add new packages here
        'nasa': nasa_apod(),
        'weather': weather_api('New+York+City'),
        'news': nytimes_api()
        }
        theme = updateTheme("danger", "primary") #just for testing

        widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space', 'stocks', 'stocks', 'stocks', 'test']
        # return render_template('response.html',user = user, wdigets = widgets, name = "Logged in", theme = theme)
        return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages, username = user)
        #returns home page with modified theme, kind of scuffed and bad code as of now
    else:
        return render_template('login.html', login_fail = response) #Else, return the response telling you what's wrong
def validate(name, value):
    error_message = ""
    if name == "userID":
        if value == "" or value == " " or value == None:
            error_message += " | Username cannot be blank"
        if check_existence("username", value):
            error_message += " | Username already exists"
        if len(value) > 50:
            error_message += " | Username cannot exceed 50 characters"
    if name == "password":
        if len(value) > 50:
            error_message += " | Password must only have between 8 and 50 characters"
        # if(value != request.args['pass']):
        #     error_message += " | Passwords must match"
    if error_message == "":
        return "";
    else:
        return error_message + " |"

def check_existence(c_name, value):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT " + c_name + " FROM userinfo WHERE " +c_name + " LIKE '%" + value + "%';")
        listUsers = c.fetchall()
        # print(f"Hello*****, {listUsers}")
        if (len(listUsers) == 0):
            return False
        return True
def loggin():
    return true
createTables()


#not useful rn
def insert(username,password): #insert user and password into table
    with sqlite3.connect(DB_FILE) as db:
            #open if file exists, otherwise create
            c = db.cursor()
            # c.execute("INSERT INTO " + table_name + "(username) VALUES (?)",(value,) )
            c.execute("INSERT INTO userinfo (username,password) VALUES (?,?)",(username,password) )
            db.commit()
            msg = "Record successfully added"
#prints table for testing
def printTable():
    with sqlite3.connect(DB_FILE) as db:
            #open if file exists, otherwise create
            c = db.cursor()
            c.execute("SELECT * FROM userinfo")
            print(c.fetchall())
def clearTable():
    with sqlite3.connect(DB_FILE) as db:
            #open if file exists, otherwise create
            c = db.cursor()
            c.execute("DELETE from userinfo;")
            db.commit()
