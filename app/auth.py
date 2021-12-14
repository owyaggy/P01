import sqlite3

DB_file = "discobandit.db"


def register(template_name, username, password, user_ID, user_password database):
    error = "ERROR: "
    error += validate(user_ID, request.args[username])
    error += validate(user_password, request.args[password])
    if (error == "ERROR: "):
        #if userID is valid, store in database
        session[user_ID] = request.args[username]
        insert(database, request.args[username], request.args[password])

        return render_template(template_name,user = request.args[username])
            # ADD USERID TO THE DB HERE

    return render_template(template_name, error = error)
    # return render_template('response.html', user = session.get("userID"))
