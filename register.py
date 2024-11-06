import sqlite3
from http.cookiejar import debug

from flask import Flask, render_template, request, redirect, url_for
import json

from jinja2.compiler import generate

from login import sign_in

app = Flask(__name__)
app.secret_key = 'hehehe'
sqldbname = 'db/users.db'

@app.route('/')
def index():
    return render_template('sign-in.html',
                           username_error="",
                           email_error="",
                           phone_number_error="",
                           password_error="",
                           registration_success="")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    phone_number = request.form['phone_number']
    password = request.form['password']
    username_error = ""; email_error = ""; phone_number_error=""; password_error = ""
    if not username: username_error = "Username is required."
    if not password: password_error = "Password is required."
    if username_error or password_error:
        return render_template('sign-in.html', username_error=username_error, password_error=password_error, registration_success="")
    newid = SaveToDB(username, email, phone_number,password)
    stroutput = f'Registered: Username - {username}, Password - {password}'
    registration_success = "Registration Successful! with id = " + str(newid)
    print(registration_success+stroutput)
    return render_template('sign-in.html',
                           password_error="",username_error="",
                           registration_success=registration_success+stroutput)


def SaveToDB(name,email,phone_number,password):
    id_max = generateID()
    if id_max>0:
        id_max=id_max+1
    else:
        id_max=1
    print(id_max)
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("INSERT INTO users "
                "(id, name, email, phone_number, password) VALUES (?, ?, ?, ?)"
                ,(id_max, name, email, phone_number,password))
    conn.commit()
    conn.close()
    return id_max
def generateID():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = "SELECT Max(id) from users"
    cursor.execute(sqlcommand)
    max_id = cursor.fetchone()[0]
    return max_id;

if __name__ == '__main__':
    app.run(debug=True)