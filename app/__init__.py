from flask import Flask, render_template, redirect, url_for, request, session
import os

from api import *
from db_builder import validate, check_existence, register, insert, printTable, updateTheme
from db_builder import clearTable, authenticate

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

def logged_in():
    return "username" in session

### NEEDS TO BE REPLACED BY FUNCTION IN DB_BUILDER ###
theme = updateTheme("info","secondary")

symbols = ['DOW', 'NDAQ']
info = stocks_api(symbols)
widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space', 'stocks']# a complete list of all widgets
packages = {}

for widget in widgets:
    packages[widget] = get_api(widget)
@app.route('/')
@app.route("/home")
def home():
    # available widgets:
    # weather, news, recommendations, stocks, fun, sports, space
    # theme based on bootstrap colors [primary, secondary, success, danger, warning, info, light, dark]
    #theme = "dark" # should be replaced by function getting user theme from database


    if logged_in():
        print("LOGGED IN HOME")
        username = session['username']
        # widgets = db_builder.enabledWidgets() # get only the selected widgets from the user's preferences
        theme = updateTheme("danger", "primary") #just for testing
        return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages, username = username, logged_in = logged_in())
    else:
        print("NOT LOGGED IN HOME")
        theme = updateTheme("info", "secondary")
        return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', theme=theme)

@app.route('/user')
def settings():
    return render_template('user.html', name="Log In", theme=theme)

@app.route('/weather')
def weather():
    # ONLY WORKS FOR EST TIME ZONE???
    cities = ['New+York+City', 'Toronto', 'Ontario', 'Sao+Paulo', 'California', 'Mexico+City', 'Miami', 'Cambridge']
    try:
        city = request.args['city']
    except:
        city = "New+York+City"
    info = weather_api(city)
    return render_template('weather.html', name="Weather", theme=theme, info=info, cities=cities)

@app.route('/news')
def news():
    info = news_api()
    return render_template('news.html', name="News", theme=theme, info=info)

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html', name="Recommendations", theme=theme)

@app.route('/stocks')
def stocks():
    return render_template('stocks.html', name="Stocks", info=info, symbols=symbols, theme=theme)

@app.route('/fun')
def fun():
    return render_template('fun.html', name="Fun", theme=theme)

@app.route('/sports')
def sports():
    info = {'sports': sports_api(2021)}
    return render_template('sports.html', name="Sports", theme=theme, packages=info)

@app.route('/space')
def space():
    info = space_api(3)
    return render_template('space.html', name="Space", theme=theme, info=info)

@app.route('/reg1', methods= ["GET", "POST"])
def reg1():
    return render_template("register.html", name = "Reg1", theme = theme)
@app.route('/reg2', methods= ["GET", "POST"])
def reg2():#registers a user
    request_user = request.args['regUser']
    request_password = request.args['regPass']
    print(f"Hello*********, {request_user}")
    print (f"Hello*********, {request_password}")
    # clearTable()
    printTable()
    session["username"] = request_user #puts user into session
    print(f"session length: {len(session)}")
    return register(request_user,request_password) #puts username and pw into database, returns response.html
@app.route("/auth", methods=['GET', 'POST'])
def log():#using the loggin button will enter the user into the sesion
    request_user = request.args['regUser']
    print(f"Hello*********, {request_user}")
    request_password = request.args['regPass']
    print(f"Hello*********, {request_password}")
    # printTable()
    session['username'] = request_user
    return authenticate(request_user,request_password)
    # return render_template('response.html',user = request_user, name = "Logged in", theme = theme)
@app.route("/logout", methods = ["GET","POST"])
def logout():
    print("HITTTING LOG OUT")
    # if len(session) > 0 and len(session.get("userID")) > 0: #If username does exist, remove it from session and return the login page
    #     session.pop("userID")
    return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages)

@app.route('/preference')
def preference():
    userThemes = ['Light', 'Dark', 'test3']
    return render_template('preference.html', userThemes=userThemes, widgets=widgets, name='preference', theme=theme)

@app.route('/preferenceSet')
def preferenceSet():
    return preference()

if __name__ == "__main__":
    app.debug = True
    app.run()
