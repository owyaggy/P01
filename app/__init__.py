from flask import Flask, render_template, request, session
import os
app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #create random key

@app.route("/") #,methods=['GET', 'POST'])
def disp_loginpage():
    return render_template('child.html')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
