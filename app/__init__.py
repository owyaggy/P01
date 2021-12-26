from flask import Flask, render_template, redirect, url_for, request, session
import os

from api import *
from db_builder import validate, check_existence, register, insert, printTable, updateTheme
from db_builder import clearTable, authenticate
app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

def logged_in():
    return session.get('username') is not None

### NEEDS TO BE REPLACED BY FUNCTION IN DB_BUILDER ###
theme = updateTheme("info","secondary")

@app.route('/')
@app.route("/home")
def home():
    # available widgets:
    # weather, news, recommendations, stocks, fun, sports, space
    widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space', 'stocks', 'stocks', 'stocks', 'test'] # a complete list of all widgets
    # theme based on bootstrap colors [primary, secondary, success, danger, warning, info, light, dark]
    #theme = "dark" # should be replaced by function getting user theme from database
    packages = { # add new packages here
        'nasa': nasa_apod(),
        'weather': weather_api('New+York+City'),
        'news': nytimes_api()
    }
    if logged_in():
        username = session['username']
        # widgets = db_builder.enabledWidgets() # get only the selected widgets from the user's preferences
        theme = updateTheme("success", "secondary") #just for testing
        return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages, username = session['username'])
    else:
        theme = updateTheme("info", "secondary")
        return render_template('home.html', name="Home", widgets=widgets, theme=theme, packages=packages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', theme=theme)

@app.route('/settings')
def settings():
    return render_template('settings.html', name="Settings", theme=theme)

@app.route('/weather')
def weather():
    cities = ['New+York+City', 'Los+Angeles', 'Chicago', 'Boston', 'London', 'Beijing', 'Moscow', 'Toronto', 'Mexico+City', 'Tokyo', 'Shanghai', 'Delhi', 'Sao+Paulo']
    try:
        city = request.args['city']
        print(city)
    except:
        city = "New York City"
    print()
    print()
    print()
    print(city)
    info = weather_api(city)
    return render_template('weather.html', name="Weather", theme=theme, info=info, cities=cities)

@app.route('/news')
def news():
    return render_template('news.html', name="News", theme=theme)

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html', name="Recommendations", theme=theme)

@app.route('/stocks')
def stocks():
    return render_template('stocks.html', name="Stocks", theme=theme)

@app.route('/fun')
def fun():
    return render_template('fun.html', name="Fun", theme=theme)

@app.route('/sports')
def sports():
    return render_template('sports.html', name="Sports", theme=theme)

@app.route('/space')
def space():
    info = nasa_apod(3)
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
    widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space', 'stocks', 'stocks', 'stocks', 'test']
    request_user = request.args['regUser']
    print(f"Hello*********, {request_user}")
    request_password = request.args['regPass']
    print(f"Hello*********, {request_password}")
    printTable()
    return authenticate(request_user,request_password)
    # return render_template('response.html',user = request_user, name = "Logged in", theme = theme)

if __name__ == "__main__":
    app.debug = True
    app.run()
