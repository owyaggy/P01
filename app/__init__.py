from flask import Flask, render_template, request, session
import os
app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

from app import routes

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
