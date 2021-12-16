import sqlite3

DB_file = "discobandit.db"


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
    time INTEGER):"""
    )
    db.commit()
    db.close()

def register(template_name, username, password, user_ID, user_password, database):
    error = "ERROR: "
    error += validate(user_ID, request.args[username])
    error += validate(user_password, request.args[password])
    if (error == "ERROR: "):
        #if userID and password is valid, store in database
        session[user_ID] = request.args[username]
        insert(database, request.args[username], request.args[password])

        return render_template(template_name,user = request.args[username])
            # ADD USERID TO THE DB HERE

    return render_template(template_name, error = error)
    # return render_template('response.html', user = session.get("userID"))

#not useful rn
# def insert(table_name, username, password): #insert user and password into table
#     with sqlite3.connect(DB_FILE) as db:
#             #open if file exists, otherwise create
#             c = db.cursor()
#             c.execute("INSERT INTO " + table_name + "(username,password) VALUES (?,?)",(username,password) )
#             db.commit()
#             msg = "Record successfully added"
