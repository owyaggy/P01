from flask import Flask, render_template, redirect, url_for, request, session
import os
app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/stocks')
def stocks():
    return render_template('stocks.html')

@app.route('/fun')
def fun():
    return render_template('fun.html')

@app.route('/sports')
def sports():
    return render_template('sports.html')

@app.route('/space')
def space():
    return render_template('space.html')

if __name__ == "__main__":
    app.debug = True
    app.run()