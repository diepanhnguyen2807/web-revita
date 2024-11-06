import sqlite3
from flask import (Flask, render_template,
                   request, redirect,
                   session, url_for)
app = Flask(__name__)
app.secret_key = 'hehehe'

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return (f', {username} ơi! '
                f'<a href="/logout">Logout</a>')
    return 'Welcome! Have a nice day ^^ <a href="/login">Login</a>'
def check_exists(username, password):
    result = False
    sqldbname = 'db/website.db'
    conn = sqlite3.connect((sqldbname))
    cursor = conn.cursor()
    sqlcommand = "Select * from user where name = '"+username+"' and password = '"+password+"'"
    cursor.execute(sqlcommand)
    data = cursor.fetchall()
    print(type(data))
    if len(data)>0:
        result = True
    conn.close()
    return result

@app.route('/sign-in', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if check_exists(email, password):
            session['email'] = email
        return redirect(url_for('home'))
    return render_template('sign-in.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5002)