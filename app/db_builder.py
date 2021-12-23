import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session
import os

DB_FILE = "discobandit.db"

def updateTheme():
    theme = dict(main='info', text='secondary')
    return theme
theme = updateTheme()
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
        session["userID"] = request_user
        insert(request_user, request_password)
        print("**** PASS")
        widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space', 'stocks', 'stocks', 'stocks', 'test']
        return render_template('response.html',user = request_user, wdigets = widgets, name = "Logged in", theme = theme)
            # ADD USERID TO THE DB HERE
    print("***** FAIL")
    return render_template('register.html', error = error, theme = theme)
    # return render_template('response.html', user = session.get("userID"))

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
        print(listUsers)
        if (len(listUsers) == 0):
            return False
        return True

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
