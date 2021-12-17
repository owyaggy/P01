from flask import Flask, render_template, redirect, url_for, request, session
import os

from db_builder import validate, check_existence, register
app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

def logged_in():
    return session.get('username') is not None

### NEEDS TO BE REPLACED BY FUNCTION IN DB_BUILDER ###
theme="info"

@app.route('/')
@app.route("/home")
def home():
    # available widgets:
    # weather, news, recommendations, stocks, fun, sports, space
    widgets = ['weather', 'news', 'recommendations', 'fun', 'sports', 'space', 'stocks', 'stocks', 'stocks', 'test'] # a complete list of all widgets
    # theme based on bootstrap colors [primary, secondary, success, danger, warning, info, light, dark]
    #theme = "dark" # should be replaced by function getting user theme from database
    if logged_in():
        username = session['username']
        widgets = db_builder.enabledWidgets() # get only the selected widgets from the user's preferences
        return render_template('home.html', name="Home", widgets=widgets, theme=theme)
    else:
        return render_template('home.html', name="Home", widgets=widgets, theme=theme)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', theme=theme)

@app.route('/settings')
def settings():
    return render_template('settings.html', name="Settings", theme=theme)

@app.route('/weather')
def weather():
    return render_template('weather.html', name="Weather", theme=theme)

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
    return render_template('space.html', name="Space", theme=theme)

@app.route('/reg1', methods= ["GET", "POST"])
def reg1():
    return render_template("register.html", name = "Register", theme = theme)
@app.route('/reg2', methods= ["GET", "POST"])
def reg2():
    register("home.html","register.html","regUser","regPass","userID","password","userinfo")


if __name__ == "__main__":
    app.debug = True
    app.run()
