from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'hehehe'

@app.route('/')
def index():
    return 'This is home page'


@app.route('/sign-in', methods=['POST'])
def sign_in():
    # Khi nhận dữ liệu từ hành vi post, sau khi nhận dữ liệu
    # từ session sẽ gọi định tuyến sang trang index
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Store 'username' in the session
        obj_user = get_obj_user(email, password)
        if obj_user is not None:
            obj_user = {
                "id": obj_user[0],
                "name": obj_user[1],
                "email": obj_user[2],
                "phone_number": obj_user[3],
                "password": obj_user[4]
            }
            session['current_user'] = obj_user
        return redirect(url_for('index'))
    # Trường hợp mặc định là vào trang login
    return render_template('sign-in.html')

def get_obj_user(email, password):
    result = None;
    sqldbname = 'db/users.db'
    # Khai bao bien de tro toi db
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    # sqlcommand = "Select * from storages where "
    sqlcommand = "Select * from users where email = ? and password = ?"
    cursor.execute(sqlcommand,(email,password))
    # return object
    obj_user = cursor.fetchone()
    if obj_user is not None:
        result = obj_user
    conn.close()
    return result;

if __name__ == '__main__':
    app.run(debug=True)