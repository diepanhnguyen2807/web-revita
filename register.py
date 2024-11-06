import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'hehehe'
sqldbname = 'db/users.db'


@app.route('/')
def index():
    return render_template('sign-in.html',
                           name_error="",
                           email_error="",
                           phone_number_error="",
                           password_error="",
                           confirm_password_error="",
                           registration_success="")


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    name_error = ""
    email_error = ""
    phone_number_error = ""
    password_error = ""
    confirm_password_error = ""

    # Validate name
    if not name:
        name_error = "Name is required."

    # Validate email
    if not email:
        email_error = "Email is required."
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        email_error = "Invalid email address."
    elif email_exists(email):
        email_error = "Email already in use."

    # Validate phone number
    if not phone_number:
        phone_number_error = "Phone number is required."
    elif not phone_number.isdigit():
        phone_number_error = "Phone number must contain only digits."
    elif phone_number_exists(phone_number):
        phone_number_error = "Phone number already in use."

    # Validate password
    if not password:
        password_error = "Password is required."
    elif password != confirm_password:
        confirm_password_error = "Passwords do not match."

    if name_error or email_error or phone_number_error or password_error or confirm_password_error:
        return render_template('sign-in.html',
                               name_error=name_error,
                               email_error=email_error,
                               phone_number_error=phone_number_error,
                               password_error=password_error,
                               confirm_password_error=confirm_password_error,
                               registration_success="")

    newid = save_to_db(name, email, phone_number, password)
    stroutput = f'Registered: name - {name}, Password - {password}'
    registration_success = "Registration Successful! with id = " + str(newid)
    print(registration_success + stroutput)

    return render_template('sign-in.html',
                           name_error="",
                           email_error="",
                           phone_number_error="",
                           password_error="",
                           confirm_password_error="",
                           registration_success=registration_success + stroutput)


def email_exists(email):
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def phone_number_exists(phone_number):
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE phone_number = ?", (phone_number,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def save_to_db(name, email, phone_number, password):
    id_max = generate_id()
    if id_max > 0:
        id_max += 1
    else:
        id_max = 1
    print(id_max)

    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, name, email, phone_number, password) VALUES (?, ?, ?, ?, ?)",
                (id_max, name, email, phone_number, password))
    conn.commit()
    conn.close()
    return id_max


def generate_id():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = "SELECT MAX(id) FROM users"
    cursor.execute(sqlcommand)
    max_id = cursor.fetchone()[0]
    conn.close()
    return max_id


if __name__ == '__main__':
    app.run(debug=True)
