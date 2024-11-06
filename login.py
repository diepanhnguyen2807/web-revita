import sqlite3

from flask import (Flask, render_template,
                   request, redirect,
                   session, url_for, jsonify)
app = Flask(__name__)
app.secret_key = 'hehehe'

# @app.route('/')
# def index():
#     if 'username' in session:
#         username = session['username']
#         return (f', {username} ơi! '
#                 f'<a href="/logout">Logout</a>')
#     return 'Welcome! Have a nice day ^^ <a href="/login">Login</a>'
# def check_exists(username, password):
#     result = False
#     sqldbname = 'db/website.db'
#     conn = sqlite3.connect((sqldbname))
#     cursor = conn.cursor()
#     sqlcommand = "Select * from user where name = '"+username+"' and password = '"+password+"'"
#     cursor.execute(sqlcommand)
#     data = cursor.fetchall()
#     print(type(data))
#     if len(data)>0:
#         result = True
#     conn.close()
#     return result

# @app.route('/sign-in', methods=['GET','POST'])
# def sign_in():
#     email = request.form['email']
#     password = request.form['password']
#
#     conn = sqlite3.connect('db/user.db')
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM user WHERE email = ? AND password = ?", (email, password,))
#     user = cur.fetchone()
#     conn.close()
#
#     if user:
#         user_dict = {'id': user[0],
#                      'name': user[1],
#                      'email': user[3],
#                      'phone_number': user[4],
#                      'password': user[5]}
#         return jsonify(user_dict)
#     else: return "User not found!", 404


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('db/users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'phone_number': user[3],
                'password': user[4]
            }
            return jsonify(user_dict)
        else: return "User not found!", 404
    return render_template('sign-in.html')


# Ktra kết nối với db
# @app.route('/users',methods=['GET'])
# def get_users():
#     conn = sqlite3.connect('db/user.db')
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
#
#     users_list = []
#     for user in users:
#         users_list.append({
#             "id": user[0],
#             "name": user[1],
#             'email': user[2],
#             'phone_number': user[3],
#             'password': user[4]
#         })
#
#     conn.close()
#     return jsonify(users_list)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)